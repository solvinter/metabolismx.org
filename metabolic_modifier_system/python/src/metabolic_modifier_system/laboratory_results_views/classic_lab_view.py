import pandas as pd
from typing import Optional, Dict, Any


def _interval_text(level: Dict[str, Any]) -> str:
    if level is None:
        return ""
    lower = level.get("min")
    upper = level.get("max")
    if lower is None and upper is None:
        return ""
    if lower is None:
        return f"<{upper}"
    if upper is None:
        return f">={lower}"
    return f"{lower}–{upper}"


def _row(marker: str, value: Any, unit: str = "", level: Optional[Dict[str, Any]] = None):
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
        "Reference / range": _interval_text(level),
        "Interpretation": level.get("label", ""),
    }


def render_classic_lab_view(patient: dict, results: dict, levels: Optional[dict] = None, summaries: Optional[dict] = None) -> pd.DataFrame:
    """
    Render a classic lab-style DataFrame.

    Unified signature: (patient, results, levels=None, summaries=None)

    Uses raw values from `patient` where appropriate (fasting_glucose, hba1c, ldl, hdl,
    triglycerides, blood pressure).

    Returns a pandas.DataFrame (rows) — caller (app.py) will display it.
    """
    if levels is None:
        levels = {}

    rows = []

    # BODY
    height = patient.get('height_cm')
    rows.append(_row("Height", f"{height:.0f}" if height is not None else "", "cm"))

    weight = patient.get('weight_kg')
    rows.append(_row("Weight", f"{weight:.1f}" if weight is not None else "", "kg"))

    waist = patient.get('waist_cm')
    rows.append(_row("Waist circumference", f"{waist:.0f}" if waist is not None else "", "cm", levels.get('waist')))

    bmi = results.get('bmi')
    rows.append(_row("BMI", f"{bmi:.2f}" if bmi is not None else "", "kg/m²", levels.get('bmi')))

    # GLUCOSE / INSULIN
    fg = patient.get('fasting_glucose')
    rows.append(_row("Fasting glucose", f"{fg:.2f}" if fg is not None else "", "mmol/L", levels.get('fasting_glucose')))

    fi = patient.get('fasting_insulin')
    rows.append(_row("Fasting insulin", f"{fi:.2f}" if fi is not None else "", "mIU/L", levels.get('fasting_insulin')))

    cpep = patient.get('c_peptide')
    rows.append(_row("C-peptide", f"{cpep:.2f}" if cpep is not None else "", "nmol/L", levels.get('c_peptide')))

    hba1c = patient.get('hba1c')
    rows.append(_row("HbA1c", f"{hba1c:.0f}" if hba1c is not None else "", "mmol/mol", levels.get('hba1c')))

    eag = results.get('eAG')
    rows.append(_row("Estimated average glucose", f"{eag:.2f}" if eag is not None else "", "mmol/L"))

    homa = results.get('homa_ir')
    rows.append(_row("HOMA-IR", f"{homa:.2f}" if homa is not None else "", "index", levels.get('homa_ir')))

    quicki = results.get('quicki')
    rows.append(_row("QUICKI", f"{quicki:.3f}" if quicki is not None else "", "index", levels.get('quicki')))

    # LIPIDS — prefer patient raw values
    total = patient.get('total_cholesterol')
    rows.append(_row("Total cholesterol", f"{total:.2f}" if total is not None else "", "mmol/L", levels.get('total_cholesterol')))

    ldl = patient.get('ldl')
    rows.append(_row("LDL cholesterol", f"{ldl:.2f}" if ldl is not None else "", "mmol/L", levels.get('ldl')))

    hdl = patient.get('hdl')
    rows.append(_row("HDL cholesterol", f"{hdl:.2f}" if hdl is not None else "", "mmol/L", levels.get('hdl')))

    tg = patient.get('triglycerides')
    rows.append(_row("Triglycerides", f"{tg:.2f}" if tg is not None else "", "mmol/L", levels.get('triglycerides')))

    rows.append(_row("Non-HDL cholesterol", f"{results.get('non_hdl'):.2f}" if results.get('non_hdl') is not None else "", "mmol/L", levels.get('non_hdl')))
    rows.append(_row("Remnant cholesterol", f"{results.get('remnant'):.2f}" if results.get('remnant') is not None else "", "mmol/L", levels.get('remnant')))

    # HEMODYNAMICS — use patient BP
    sbp = patient.get('systolic_bp')
    dbp = patient.get('diastolic_bp')
    bp_val = f"{sbp:.0f}/{dbp:.0f}" if (sbp is not None and dbp is not None) else ""
    rows.append(_row("Blood pressure", bp_val, "mmHg", levels.get('blood_pressure')))
    pp = results.get('pulse_pressure')
    rows.append(_row("Pulse pressure", f"{pp:.0f}" if pp is not None else "", "mmHg", levels.get('pulse_pressure')))
    mapv = results.get('map')
    rows.append(_row("Mean arterial pressure", f"{mapv:.1f}" if mapv is not None else "", "mmHg", levels.get('map')))

    df = pd.DataFrame(rows)
    return df
