"""MetabolismX v0.1 heuristic summary models.

These functions combine already calculated markers into transparent,
rule-based pattern summaries. They are not diagnostic criteria, treatment
recommendations or validated risk engines.
"""


def calculate_metabolic_syndrome_components(patient, results):
    components = {
        "waist": _has_elevated_waist(patient.get("waist_cm"), patient.get("sex")),
        "triglycerides": patient["triglycerides"] >= 1.7,
        "hdl": _has_low_hdl(patient["hdl"], patient.get("sex")),
        "blood_pressure": patient["systolic_bp"] >= 130 or patient["diastolic_bp"] >= 85,
        "fasting_glucose": patient["fasting_glucose"] >= 5.6,
    }
    component_count = sum(components.values())

    return {
        "component_count": component_count,
        "meets_3_of_5": component_count >= 3,
        "components": components,
    }


def calculate_metabolic_burden_score(patient, results):
    drivers = []

    _add_driver(drivers, results["waist_height_ratio"] >= 0.5, "waist/height ratio >=0.5")
    _add_driver(drivers, patient["triglycerides"] >= 1.7, "triglycerides >=1.7 mmol/L")
    _add_driver(drivers, _has_low_hdl(patient["hdl"], patient.get("sex")), "low HDL")
    _add_driver(drivers, results["tg_hdl_ratio"] >= 2.0, "TG/HDL ratio >=2.0")
    _add_driver(drivers, patient["fasting_insulin"] >= 10, "fasting insulin >=10 mIU/L")
    _add_driver(drivers, results["homa_ir"] >= 2.5, "HOMA-IR >=2.5")
    _add_driver(drivers, patient["fasting_glucose"] >= 5.6, "fasting glucose >=5.6 mmol/L")
    _add_driver(
        drivers,
        patient["systolic_bp"] >= 130 or patient["diastolic_bp"] >= 80,
        "blood pressure >=130/80 mmHg",
    )

    score = len(drivers)

    return {
        "score": score,
        "level": _burden_level(score),
        "drivers": drivers,
    }


def summarise_insulin_resistance_pattern(patient, results):
    supporting_markers = []

    _add_driver(supporting_markers, patient["fasting_insulin"] >= 10, "fasting insulin >=10 mIU/L")
    _add_driver(supporting_markers, results["homa_ir"] >= 2.5, "HOMA-IR >=2.5")
    _add_driver(supporting_markers, results["tg_hdl_ratio"] >= 2.0, "TG/HDL ratio >=2.0")
    _add_driver(supporting_markers, results["tyg_index"] >= 9.0, "TyG index >=9.0")
    _add_driver(supporting_markers, results["waist_height_ratio"] >= 0.5, "waist/height ratio >=0.5")
    _add_driver(supporting_markers, patient["fasting_glucose"] >= 5.6, "fasting glucose >=5.6 mmol/L")

    signal = _pattern_signal(len(supporting_markers))

    summaries = {
        "low": "Low insulin resistance signal in the current rule set.",
        "moderate": "Moderate insulin resistance pattern; several markers suggest metabolic load.",
        "high": "High insulin resistance pattern; multiple glucose-insulin, lipid and adiposity markers align.",
    }

    return {
        "signal": signal,
        "summary": summaries[signal],
        "supporting_markers": supporting_markers,
    }


def summarise_atherogenic_dyslipidaemia(patient, results):
    supporting_markers = []

    _add_driver(supporting_markers, patient["triglycerides"] >= 1.7, "triglycerides >=1.7 mmol/L")
    _add_driver(supporting_markers, _has_low_hdl(patient["hdl"], patient.get("sex")), "low HDL")
    _add_driver(supporting_markers, results["tg_hdl_ratio"] >= 2.0, "TG/HDL ratio >=2.0")
    _add_driver(supporting_markers, results["non_hdl"] >= 3.4, "non-HDL cholesterol >=3.4 mmol/L")
    _add_driver(supporting_markers, results["remnant"] >= 0.8, "remnant cholesterol >=0.8 mmol/L")

    signal = _pattern_signal(len(supporting_markers))

    summaries = {
        "low": "Low atherogenic dyslipidaemia signal in the current rule set.",
        "moderate": "Moderate atherogenic dyslipidaemia pattern; several lipid markers are unfavourable.",
        "high": "High atherogenic dyslipidaemia pattern; triglyceride-rich and apoB-related burden markers align.",
    }

    return {
        "signal": signal,
        "summary": summaries[signal],
        "supporting_markers": supporting_markers,
    }


def _add_driver(drivers, condition, label):
    if condition:
        drivers.append(label)


def _burden_level(score):
    if score <= 1:
        return "low"
    if score <= 3:
        return "moderate"
    if score <= 5:
        return "high"
    return "very high"


def _pattern_signal(marker_count):
    if marker_count >= 4:
        return "high"
    if marker_count >= 2:
        return "moderate"
    return "low"


def _has_elevated_waist(waist_cm, sex):
    normalized_sex = _normalize_sex(sex)

    if waist_cm is None or normalized_sex is None:
        return False

    if normalized_sex == "male":
        return waist_cm >= 94

    return waist_cm >= 80


def _has_low_hdl(hdl, sex):
    normalized_sex = _normalize_sex(sex)

    if normalized_sex == "male":
        return hdl < 1.0

    if normalized_sex == "female":
        return hdl < 1.3

    return False


def _normalize_sex(sex):
    if sex is None:
        return None

    normalized = str(sex).strip().lower()

    if normalized in {"male", "man", "m", "masculine"}:
        return "male"

    if normalized in {"female", "kvinna", "k", "f", "woman", "w"}:
        return "female"

    return None
