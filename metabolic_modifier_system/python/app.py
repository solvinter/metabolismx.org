import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from metabolic_modifier_system.laboratory_results_views.classic_lab_view import render_classic_lab_view
from metabolic_modifier_system.laboratory_results_views.metabolismx_lab_view import render_metabolismx_lab_view

CURRENT_DIR = Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from metabolic_modifier_system.lab_exploration import calculate_expanded_labs
from metabolic_modifier_system.interpretation import (
    interpret_value,
    interpret_blood_pressure,
    interpret_waist,
)
from metabolic_modifier_system.reference_values import *
from metabolic_modifier_system.summary_models import (
    calculate_metabolic_syndrome_components,
    calculate_metabolic_burden_score,
    summarise_insulin_resistance_pattern,
    summarise_atherogenic_dyslipidaemia,
)


def interval_text(level):
    lower = level.get("min")
    upper = level.get("max")

    if lower is None and upper is None:
        return ""
    if lower is None:
        return f"<{upper}"
    if upper is None:
        return f">={lower}"
    return f"{lower}–{upper}"


def row(marker, value, unit="", level=None):
    if level is None:
        return {
            "Marker": marker,
            "Result": value,
            "Unit": unit,
            "Reference / range": "",
            "Interpretation": "",
        }

    return {
        "Marker": marker,
        "Result": value,
        "Unit": unit,
        "Reference / range": interval_text(level),
        "Interpretation": level["label"],
    }


def show_table(title, rows):
    st.subheader(title)
    df = pd.DataFrame(rows)
    display_dataframe(df, hide_index=True)


def display_dataframe(df: pd.DataFrame, *, hide_index: bool = True, **kwargs):
    """Render a dataframe trying width="stretch" first, falling back to use_container_width.

    Some Streamlit versions don't accept width="stretch"; to respect your request we try it
    and gracefully fall back to the previous behavior.
    """
    try:
        # Try the user-requested style first
        st.dataframe(df, width="stretch", hide_index=hide_index, **kwargs)
    except TypeError:
        # Fallback to the previous supported API
        st.dataframe(df, use_container_width=True, hide_index=hide_index, **kwargs)


st.set_page_config(page_title="MetabolismX Lab Explorer", layout="wide")

st.title("MetabolismX Lab Explorer")
st.caption("Deterministic prototype: raw values → calculated markers → reference ranges → interpretations.")

st.sidebar.header("Patient input")

patient = {
    "name": st.sidebar.text_input("Name", "Test Testsson"),
    "sex": st.sidebar.selectbox("Sex", ["male", "female"], index=0),

    "height_cm": st.sidebar.number_input("Height cm", value=178.0),
    "weight_kg": st.sidebar.number_input("Weight kg", value=94.0),
    "waist_cm": st.sidebar.number_input("Waist cm", value=104.0),

    "systolic_bp": st.sidebar.number_input("Systolic BP", value=138.0),
    "diastolic_bp": st.sidebar.number_input("Diastolic BP", value=86.0),

    "fasting_glucose": st.sidebar.number_input("Fasting glucose mmol/L", value=5.8),
    "fasting_insulin": st.sidebar.number_input("Fasting insulin mIU/L", value=14.0),
    "c_peptide": st.sidebar.number_input("C-peptide nmol/L", value=0.95),
    "hba1c": st.sidebar.number_input("HbA1c mmol/mol", value=39.0),

    "total_cholesterol": st.sidebar.number_input("Total cholesterol mmol/L", value=5.4),
    "ldl": st.sidebar.number_input("LDL mmol/L", value=3.3),
    "hdl": st.sidebar.number_input("HDL mmol/L", value=1.0),
    "triglycerides": st.sidebar.number_input("Triglycerides mmol/L", value=2.1),
}

results = calculate_expanded_labs(patient)

# Interpretations
levels = {
    "bmi": interpret_value(results["bmi"], BMI),
    "waist": interpret_waist(patient["waist_cm"], patient.get("sex"), WAIST_CIRCUMFERENCE),
    "waist_height": interpret_value(results["waist_height_ratio"], WAIST_HEIGHT_RATIO),

    "fasting_glucose": interpret_value(patient["fasting_glucose"], FASTING_GLUCOSE),
    "fasting_insulin": interpret_value(patient["fasting_insulin"], FASTING_INSULIN),
    "c_peptide": interpret_value(patient["c_peptide"], C_PEPTIDE),
    "hba1c": interpret_value(patient["hba1c"], HBA1C),
    "homa_ir": interpret_value(results["homa_ir"], HOMA_IR),
    "quicki": interpret_value(results["quicki"], QUICKI),
    "tyg": interpret_value(results["tyg_index"], TYG_INDEX),

    "total_cholesterol": interpret_value(patient["total_cholesterol"], TOTAL_CHOLESTEROL),
    "ldl": interpret_value(patient["ldl"], LDL_CHOLESTEROL),
    "hdl": interpret_value(patient["hdl"], HDL),
    "triglycerides": interpret_value(patient["triglycerides"], TRIGLYCERIDES),
    "non_hdl": interpret_value(results["non_hdl"], NON_HDL_CHOLESTEROL),
    "remnant": interpret_value(results["remnant"], REMNANT_CHOLESTEROL),
    "tg_hdl": interpret_value(results["tg_hdl_ratio"], TG_HDL_RATIO),
    "total_hdl": interpret_value(results["total_hdl_ratio"], TOTAL_HDL_RATIO),
    "ldl_hdl": interpret_value(results["ldl_hdl_ratio"], LDL_HDL_RATIO),

    "blood_pressure": interpret_blood_pressure(patient["systolic_bp"], patient["diastolic_bp"], BLOOD_PRESSURE),
    "pulse_pressure": interpret_value(results["pulse_pressure"], PULSE_PRESSURE),
    "map": interpret_value(results["map"], MEAN_ARTERIAL_PRESSURE),
}

st.header(f"Expanded lab list: {patient['name']}")

# Compute shared summaries once so each view can use them.
met_syn = calculate_metabolic_syndrome_components(patient, results)
burden = calculate_metabolic_burden_score(patient, results)
ir_summary = summarise_insulin_resistance_pattern(patient, results)
athero_summary = summarise_atherogenic_dyslipidaemia(patient, results)

# Pack summaries into a single dict passed to each renderer.
summaries = {
    "metabolic_syndrome": met_syn,
    "burden": burden,
    "insulin_resistance": ir_summary,
    "atherogenic_dyslipidaemia": athero_summary,
}

# Provide multiple views via tabs. The render functions are imported at top of the file.
tab1, tab2, tab3, tab4 = st.tabs([
    "Klassisk labb",
    "MetabolismX",
    "SCORE2",
    "Modifierad SCORE",
])

with tab1:
    # Classic lab view should accept unified signature and may return a DataFrame.
    try:
        df = render_classic_lab_view(patient, results, levels=levels, summaries=summaries)
        if df is not None:
            display_dataframe(df, hide_index=True)
    except Exception as e:
        st.error(f"Error rendering classic lab view: {e}")

with tab2:
    try:
        df = render_metabolismx_lab_view(patient, results, levels=levels, summaries=summaries)
        if df is not None:
            display_dataframe(df, hide_index=True)
    except Exception as e:
        st.error(f"Error rendering MetabolismX view: {e}")

with tab3:
    st.write("SCORE2 pending")

with tab4:
    st.write("MetabolismX modifier pending")

st.subheader("METABOLISM X SUMMARY")
summary_df = pd.DataFrame(
    [
        {"Summary": "Metabolic syndrome components", "Result": f"{met_syn['component_count']}/5"},
        {"Summary": "Meets 3-of-5 criterion", "Result": "yes" if met_syn["meets_3_of_5"] else "no"},
        {"Summary": "Metabolic burden score", "Result": f"{burden['score']} ({burden['level']})"},
        {"Summary": "Insulin resistance pattern", "Result": ir_summary["summary"]},
        {"Summary": "Atherogenic dyslipidaemia pattern", "Result": athero_summary["summary"]},
    ]
)
display_dataframe(summary_df, hide_index=True)

with st.expander("Raw results dictionary"):
    st.json(results)
