import pandas as pd
from typing import Dict, Any, Optional


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


def render_metabolismx_lab_view(patient: dict, results: dict, levels: Optional[dict] = None, summaries: Optional[dict] = None) -> pd.DataFrame:
    """
    MetabolismX view renderer with unified signature.

    Does not expect interpretation strings inside results; uses `levels` dict for interpretation labels.

    Returns a pandas.DataFrame (pure data builder).
    """
    if levels is None:
        levels = {}

    rows = []

    # Add a compact set of markers emphasizing MetabolismX-specific metrics
    rows.append(_row("BMI", f"{results.get('bmi'):.2f}" if results.get('bmi') is not None else "", "kg/m²", levels.get('bmi')))
    rows.append(_row("Waist/height ratio", f"{results.get('waist_height_ratio'):.2f}" if results.get('waist_height_ratio') is not None else "", "ratio", levels.get('waist_height')))

    rows.append(_row("HOMA-IR", f"{results.get('homa_ir'):.2f}" if results.get('homa_ir') is not None else "", "index", levels.get('homa_ir')))
    rows.append(_row("QUICKI", f"{results.get('quicki'):.3f}" if results.get('quicki') is not None else "", "index", levels.get('quicki')))
    rows.append(_row("TyG index", f"{results.get('tyg_index'):.2f}" if results.get('tyg_index') is not None else "", "index", levels.get('tyg')))

    rows.append(_row("TG/HDL ratio", f"{results.get('tg_hdl_ratio'):.2f}" if results.get('tg_hdl_ratio') is not None else "", "ratio", levels.get('tg_hdl')))
    rows.append(_row("Total/HDL ratio", f"{results.get('total_hdl_ratio'):.2f}" if results.get('total_hdl_ratio') is not None else "", "ratio", levels.get('total_hdl')))
    rows.append(_row("LDL/HDL ratio", f"{results.get('ldl_hdl_ratio'):.2f}" if results.get('ldl_hdl_ratio') is not None else "", "ratio", levels.get('ldl_hdl')))
import pandas as pd
from typing import Dict, Any, Optional


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


def render_metabolismx_lab_view(patient: dict, results: dict, levels: Optional[dict] = None, summaries: Optional[dict] = None) -> pd.DataFrame:
    """
    MetabolismX view renderer with unified signature.

    Does not expect interpretation strings inside results; uses `levels` dict for interpretation labels.

    Returns a pandas.DataFrame (pure data builder).
    """
    if levels is None:
        levels = {}

    rows = []

    # Add a compact set of markers emphasizing MetabolismX-specific metrics
    rows.append(_row("BMI", f"{results.get('bmi'):.2f}" if results.get('bmi') is not None else "", "kg/m²", levels.get('bmi')))
    rows.append(_row("Waist/height ratio", f"{results.get('waist_height_ratio'):.2f}" if results.get('waist_height_ratio') is not None else "", "ratio", levels.get('waist_height')))

    rows.append(_row("HOMA-IR", f"{results.get('homa_ir'):.2f}" if results.get('homa_ir') is not None else "", "index", levels.get('homa_ir')))
    rows.append(_row("QUICKI", f"{results.get('quicki'):.3f}" if results.get('quicki') is not None else "", "index", levels.get('quicki')))
    rows.append(_row("TyG index", f"{results.get('tyg_index'):.2f}" if results.get('tyg_index') is not None else "", "index", levels.get('tyg')))

    rows.append(_row("TG/HDL ratio", f"{results.get('tg_hdl_ratio'):.2f}" if results.get('tg_hdl_ratio') is not None else "", "ratio", levels.get('tg_hdl')))
    rows.append(_row("Total/HDL ratio", f"{results.get('total_hdl_ratio'):.2f}" if results.get('total_hdl_ratio') is not None else "", "ratio", levels.get('total_hdl')))
    rows.append(_row("LDL/HDL ratio", f"{results.get('ldl_hdl_ratio'):.2f}" if results.get('ldl_hdl_ratio') is not None else "", "ratio", levels.get('ldl_hdl')))

    # blood pressure metrics
    bp_level = levels.get('blood_pressure')
    sbp = patient.get('systolic_bp')
    dbp = patient.get('diastolic_bp')
    bp_val = f"{sbp:.0f}/{dbp:.0f}" if (sbp is not None and dbp is not None) else ""
    rows.append(_row("Blood pressure", bp_val, "mmHg", bp_level))
    rows.append(_row("Pulse pressure", f"{results.get('pulse_pressure'):.0f}" if results.get('pulse_pressure') is not None else "", "mmHg", levels.get('pulse_pressure')))

    df = pd.DataFrame(rows)
    return df
