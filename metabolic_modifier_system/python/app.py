import sys
from pathlib import Path

import pandas as pd
import streamlit as st

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
    st.dataframe(df, use_container_width=True, hide_index=True)


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

show_table(
    "BODY / ADIPOSITY",
    [
        row("Height", f"{patient['height_cm']:.0f}", "cm"),
        row("Weight", f"{patient['weight_kg']:.1f}", "kg"),
        row("Waist circumference", f"{patient['waist_cm']:.0f}", "cm", levels["waist"]),
        row("BMI", f"{results['bmi']:.2f}", "kg/m²", levels["bmi"]),
        row("Waist/height ratio", f"{results['waist_height_ratio']:.2f}", "ratio", levels["waist_height"]),
    ],
)

show_table(
    "GLUCOSE–INSULIN AXIS",
    [
        row("Fasting glucose", f"{patient['fasting_glucose']:.2f}", "mmol/L", levels["fasting_glucose"]),
        row("Fasting insulin", f"{patient['fasting_insulin']:.2f}", "mIU/L", levels["fasting_insulin"]),
        row("C-peptide", f"{patient['c_peptide']:.2f}", "nmol/L", levels["c_peptide"]),
        row("HbA1c", f"{patient['hba1c']:.0f}", "mmol/mol", levels["hba1c"]),
        row("Estimated average glucose", f"{results['eAG']:.2f}", "mmol/L"),
        row("HOMA-IR", f"{results['homa_ir']:.2f}", "index", levels["homa_ir"]),
        row("QUICKI", f"{results['quicki']:.3f}", "index", levels["quicki"]),
        row("TyG index", f"{results['tyg_index']:.2f}", "index", levels["tyg"]),
        row("TyG-BMI", f"{results['tyg_bmi']:.2f}", "index"),
        row("TyG-waist", f"{results['tyg_waist']:.2f}", "index"),
        row("Insulin/glucose ratio", f"{results['insulin_glucose_ratio']:.2f}", "ratio"),
        row("C-peptide/glucose ratio", f"{results['c_peptide_glucose_ratio']:.3f}", "ratio"),
        row("Insulin/C-peptide ratio", f"{results['insulin_c_peptide_ratio']:.2f}", "ratio"),
    ],
)

show_table(
    "LIPID / ATHEROGENIC AXIS",
    [
        row("Total cholesterol", f"{patient['total_cholesterol']:.2f}", "mmol/L", levels["total_cholesterol"]),
        row("LDL cholesterol", f"{patient['ldl']:.2f}", "mmol/L", levels["ldl"]),
        row("HDL cholesterol", f"{patient['hdl']:.2f}", "mmol/L", levels["hdl"]),
        row("Triglycerides", f"{patient['triglycerides']:.2f}", "mmol/L", levels["triglycerides"]),
        row("Non-HDL cholesterol", f"{results['non_hdl']:.2f}", "mmol/L", levels["non_hdl"]),
        row("Remnant cholesterol", f"{results['remnant']:.2f}", "mmol/L", levels["remnant"]),
        row("TG/HDL ratio", f"{results['tg_hdl_ratio']:.2f}", "ratio", levels["tg_hdl"]),
        row("Total/HDL ratio", f"{results['total_hdl_ratio']:.2f}", "ratio", levels["total_hdl"]),
        row("LDL/HDL ratio", f"{results['ldl_hdl_ratio']:.2f}", "ratio", levels["ldl_hdl"]),
    ],
)

show_table(
    "BLOOD PRESSURE / HEMODYNAMICS",
    [
        row("Blood pressure", f"{patient['systolic_bp']:.0f}/{patient['diastolic_bp']:.0f}", "mmHg", levels["blood_pressure"]),
        row("Pulse pressure", f"{results['pulse_pressure']:.0f}", "mmHg", levels["pulse_pressure"]),
        row("Mean arterial pressure", f"{results['map']:.1f}", "mmHg", levels["map"]),
    ],
)

met_syn = calculate_metabolic_syndrome_components(patient, results)
burden = calculate_metabolic_burden_score(patient, results)
ir_summary = summarise_insulin_resistance_pattern(patient, results)
athero_summary = summarise_atherogenic_dyslipidaemia(patient, results)

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
st.dataframe(summary_df, use_container_width=True, hide_index=True)

with st.expander("Raw results dictionary"):
    st.json(results)
