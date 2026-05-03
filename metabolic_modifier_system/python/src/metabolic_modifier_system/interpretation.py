def interpret_value(value, reference_table):
    for level in reference_table["levels"]:
        lower = level["min"]
        upper = level["max"]

        if (lower is None or value >= lower) and (upper is None or value < upper):
            return level

    return None


def interpret_blood_pressure(sbp, dbp, reference_table):
    matched_level = None

    for level in reference_table["levels"]:
        match_mode = level.get("match")

        if match_mode == "below_and":
            if sbp < level["sbp_max"] and dbp < level["dbp_max"]:
                matched_level = level

        if match_mode == "threshold_or":
            if sbp >= level["sbp_min"] or dbp >= level["dbp_min"]:
                matched_level = level

    return matched_level


def interpret_waist(waist_cm, sex, reference_table):
    normalized_sex = _normalize_sex(sex)

    if normalized_sex is None:
        return reference_table["missing_sex_interpretation"]

    for level in reference_table["levels"]:
        if level["sex"] != normalized_sex:
            continue

        lower = level["min"]
        upper = level["max"]

        if (lower is None or waist_cm >= lower) and (upper is None or waist_cm < upper):
            return level

    return None


def _normalize_sex(sex):
    if sex is None:
        return None

    normalized = str(sex).strip().lower()

    if normalized in {"male", "man", "m", "masculine"}:
        return "male"

    if normalized in {"female", "kvinna", "k", "f", "woman", "w"}:
        return "female"

    return None
