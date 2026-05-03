"""
MetabolismX reference values and interpretation templates.

Purpose:
- Keep calculation logic separate from interpretation.
- Allow the API/report layer to display only the relevant interpretation.
- Store richer context than classic lab reference intervals.
"""

TRIGLYCERIDES = {
    "label": "Triglycerides",
    "unit": "mmol/L",
    "type": "raw_lab_value",
    "metabolismx_concept": "hepatic VLDL output / insulin resistance / energy surplus signal",
    "levels": [
        {
            "id": "optimal",
            "min": None,
            "max": 1.0,
            "label": "Optimal",
            "short_interpretation": "Favourable fasting triglyceride level.",
            "clinical_context": (
                "Low fasting triglycerides generally suggest favourable hepatic lipid handling, "
                "especially when HDL is preserved and insulin markers are low."
            ),
        },
        {
            "id": "near_optimal_early_drift",
            "min": 1.0,
            "max": 1.5,
            "label": "Near optimal / early drift",
            "short_interpretation": "Usually acceptable, but may represent early metabolic drift in context.",
            "clinical_context": (
                "Interpret together with waist, HDL, fasting insulin, glucose and TyG. "
                "This range may still be benign in an otherwise metabolically healthy person."
            ),
        },
        {
            "id": "metabolic_signal",
            "min": 1.5,
            "max": 2.3,
            "label": "Metabolic signal",
            "short_interpretation": "Suggests metabolic stress, especially with low HDL or high insulin markers.",
            "clinical_context": (
                "This range may reflect increased hepatic VLDL output and is commonly seen in insulin-resistant "
                "or energy-surplus states. Alcohol intake, diet, thyroid disease and medication should be considered."
            ),
        },
        {
            "id": "high_dysregulation",
            "min": 2.3,
            "max": 5.6,
            "label": "High / dysregulation",
            "short_interpretation": "Clear triglyceride elevation.",
            "clinical_context": (
                "This suggests significant lipid/metabolic dysregulation. Consider insulin resistance, hepatic fat, "
                "alcohol intake, high refined carbohydrate intake, diabetes, hypothyroidism and secondary causes."
            ),
        },
        {
            "id": "very_high_pancreatitis_risk",
            "min": 5.6,
            "max": None,
            "label": "Very high / pancreatitis risk",
            "short_interpretation": "Very high triglycerides; pancreatitis risk becomes clinically relevant.",
            "clinical_context": (
                "This level should prompt clinical assessment for severe hypertriglyceridaemia and secondary causes. "
                "Risk of pancreatitis rises at very high levels."
            ),
        },
    ],
}


HDL = {
    "label": "HDL cholesterol",
    "unit": "mmol/L",
    "type": "raw_lab_value",
    "metabolismx_concept": "HDL context marker / reverse cholesterol transport / triglyceride-rich lipoprotein flux",
    "levels": [
        {
            "id": "low_hdl_metabolic_risk_signal",
            "min": None,
            "max": 1.0,
            "label": "Low HDL / metabolic risk signal",
            "short_interpretation": "Low HDL can support an insulin-resistant lipid pattern.",
            "clinical_context": (
                "HDL should not be interpreted as isolated 'good cholesterol'. Low HDL is most informative when "
                "triglycerides, TG/HDL ratio, insulin markers, waist or TyG also suggest metabolic dysregulation."
            ),
        },
        {
            "id": "borderline_context_dependent",
            "min": 1.0,
            "max": 1.3,
            "label": "Borderline / context dependent",
            "short_interpretation": "Intermediate HDL; interpretation depends on the broader metabolic pattern.",
            "clinical_context": (
                "This range may be acceptable in a favourable metabolic context, but becomes more concerning when "
                "triglycerides are elevated, TG/HDL ratio is high, waist is increased or insulin resistance markers are present."
            ),
        },
        {
            "id": "favourable_context_dependent",
            "min": 1.3,
            "max": 2.0,
            "label": "Favourable range, if metabolic context is also favourable",
            "short_interpretation": "Generally favourable HDL range when TG and insulin markers are also favourable.",
            "clinical_context": (
                "HDL concentration is not the same as HDL function. This range is most reassuring when triglycerides, "
                "TG/HDL ratio, glucose, insulin markers, waist and TyG are also favourable."
            ),
        },
        {
            "id": "high_hdl_interpret_cautiously",
            "min": 2.0,
            "max": None,
            "label": "High HDL / interpret cautiously",
            "short_interpretation": "High HDL is not automatically protective.",
            "clinical_context": (
                "Very high HDL should be interpreted cautiously because HDL concentration does not necessarily reflect "
                "HDL function or overall cardiometabolic risk. Interpret with triglycerides, TG/HDL ratio, insulin markers, "
                "waist, TyG and the clinical risk profile."
            ),
        },
    ],
}


TOTAL_CHOLESTEROL = {
    "label": "Total cholesterol",
    "unit": "mmol/L",
    "type": "raw_lab_value",
    "metabolismx_concept": "broad cholesterol pool / crude lipid summary marker",
    "levels": [
        {
            "id": "favourable_broad_range",
            "min": None,
            "max": 5.0,
            "label": "Favourable broad range",
            "short_interpretation": "Broadly favourable total cholesterol range.",
            "clinical_context": (
                "Total cholesterol is a crude marker and should not be interpreted alone. Break down into LDL, HDL, "
                "non-HDL, remnant cholesterol, triglycerides and total cardiovascular risk context."
            ),
        },
        {
            "id": "moderate_context_dependent",
            "min": 5.0,
            "max": 6.0,
            "label": "Moderate / context dependent",
            "short_interpretation": "Moderate total cholesterol; interpretation depends on fractions and risk.",
            "clinical_context": (
                "This range can be benign or concerning depending on LDL, HDL, non-HDL, triglycerides, remnant cholesterol "
                "and total risk. Total cholesterol alone is insufficient."
            ),
        },
        {
            "id": "elevated",
            "min": 6.0,
            "max": 7.0,
            "label": "Elevated",
            "short_interpretation": "Elevated total cholesterol.",
            "clinical_context": (
                "Elevated total cholesterol should be resolved into atherogenic and non-atherogenic components. "
                "Interpret with LDL, non-HDL, ApoB if available, HDL, triglycerides and risk context."
            ),
        },
        {
            "id": "high_total_cholesterol",
            "min": 7.0,
            "max": None,
            "label": "High total cholesterol",
            "short_interpretation": "High total cholesterol burden.",
            "clinical_context": (
                "High total cholesterol can indicate substantial lipid burden, but the clinical meaning depends on LDL, "
                "non-HDL, ApoB if available, HDL, triglycerides, familial context and total cardiovascular risk."
            ),
        },
    ],
}


LDL_CHOLESTEROL = {
    "label": "LDL cholesterol",
    "unit": "mmol/L",
    "type": "raw_lab_value",
    "metabolismx_concept": "causal atherogenic apoB-containing particle cholesterol marker",
    "levels": [
        {
            "id": "very_low_intensive_prevention_range",
            "min": None,
            "max": 1.8,
            "label": "Very low / intensive prevention range",
            "short_interpretation": "Very low LDL range, often seen in intensive prevention contexts.",
            "clinical_context": (
                "LDL is a causal atherogenic risk factor, but LDL target should be determined by total cardiovascular risk, "
                "metabolic context, prior disease and guideline framework."
            ),
        },
        {
            "id": "favourable_depending_on_risk_context",
            "min": 1.8,
            "max": 2.6,
            "label": "Favourable depending on risk context",
            "short_interpretation": "Favourable LDL range for many contexts, but risk-dependent.",
            "clinical_context": (
                "This LDL range can be favourable, but may still be above target in high-risk or very-high-risk contexts. "
                "Interpret with SCORE2/PREVENT, diabetes status, metabolic phenotype, non-HDL and ApoB if available."
            ),
        },
        {
            "id": "moderate_context_dependent",
            "min": 2.6,
            "max": 3.0,
            "label": "Moderate / context dependent",
            "short_interpretation": "Moderate LDL level; context determines concern.",
            "clinical_context": (
                "Interpret with total risk and metabolic risk modifiers. Insulin resistance, high TG/HDL, high non-HDL "
                "or remnant cholesterol may justify a stricter LDL interpretation."
            ),
        },
        {
            "id": "elevated_prevention_discussion_range",
            "min": 3.0,
            "max": 4.0,
            "label": "Elevated / prevention discussion range",
            "short_interpretation": "Elevated LDL burden.",
            "clinical_context": (
                "This level supports a prevention discussion in the right clinical context. MetabolismX should not set treatment "
                "targets alone; interpret with total risk, metabolic phenotype, family history and other atherogenic markers."
            ),
        },
        {
            "id": "high_ldl_burden",
            "min": 4.0,
            "max": None,
            "label": "High LDL burden",
            "short_interpretation": "High LDL cholesterol burden.",
            "clinical_context": (
                "High LDL is a strong atherogenic signal. Assess total risk, familial patterns, ApoB/non-HDL if available "
                "and metabolic context. LDL target remains risk-dependent."
            ),
        },
    ],
}


NON_HDL_CHOLESTEROL = {
    "label": "Non-HDL cholesterol",
    "unit": "mmol/L",
    "type": "calculated_marker",
    "metabolismx_concept": "cholesterol in all atherogenic apoB-containing particles",
    "levels": [
        {
            "id": "favourable",
            "min": None,
            "max": 2.6,
            "label": "Favourable",
            "short_interpretation": "Favourable non-HDL cholesterol burden.",
            "clinical_context": (
                "Non-HDL represents cholesterol in all atherogenic apoB-containing particles. It is especially useful when "
                "triglycerides are elevated or LDL alone may understate atherogenic burden."
            ),
        },
        {
            "id": "moderate_context_dependent",
            "min": 2.6,
            "max": 3.4,
            "label": "Moderate / context dependent",
            "short_interpretation": "Moderate non-HDL burden; context determines significance.",
            "clinical_context": (
                "Interpret with LDL, triglycerides, remnant cholesterol, ApoB if available, diabetes/metabolic phenotype "
                "and total cardiovascular risk."
            ),
        },
        {
            "id": "elevated_atherogenic_cholesterol_burden",
            "min": 3.4,
            "max": 4.1,
            "label": "Elevated atherogenic cholesterol burden",
            "short_interpretation": "Elevated cholesterol burden in atherogenic particles.",
            "clinical_context": (
                "This suggests increased atherogenic particle cholesterol, particularly relevant with high triglycerides, "
                "metabolic syndrome, diabetes risk or high TG/HDL."
            ),
        },
        {
            "id": "high_atherogenic_cholesterol_burden",
            "min": 4.1,
            "max": None,
            "label": "High atherogenic cholesterol burden",
            "short_interpretation": "High non-HDL cholesterol burden.",
            "clinical_context": (
                "High non-HDL indicates high cholesterol burden across atherogenic particles. Interpret with LDL, remnants, "
                "ApoB if available and total/metabolic risk context."
            ),
        },
    ],
}


REMNANT_CHOLESTEROL = {
    "label": "Remnant cholesterol",
    "unit": "mmol/L",
    "type": "calculated_marker",
    "metabolismx_concept": "triglyceride-rich remnant particle cholesterol proxy",
    "levels": [
        {
            "id": "favourable",
            "min": None,
            "max": 0.5,
            "label": "Favourable",
            "short_interpretation": "Favourable calculated remnant cholesterol signal.",
            "clinical_context": (
                "Remnant cholesterol is a calculated proxy for cholesterol in triglyceride-rich remnant particles. "
                "Interpret with triglycerides and data quality for LDL measurement or calculation."
            ),
        },
        {
            "id": "intermediate_context_dependent",
            "min": 0.5,
            "max": 0.8,
            "label": "Intermediate / context dependent",
            "short_interpretation": "Intermediate remnant signal.",
            "clinical_context": (
                "This range becomes more meaningful when triglycerides, TG/HDL, insulin resistance markers, waist or TyG "
                "also suggest triglyceride-rich lipoprotein dysregulation."
            ),
        },
        {
            "id": "elevated_remnant_signal",
            "min": 0.8,
            "max": 1.2,
            "label": "Elevated remnant signal",
            "short_interpretation": "Elevated remnant cholesterol signal.",
            "clinical_context": (
                "Elevated remnant cholesterol can support an atherogenic, triglyceride-rich lipoprotein pattern. Interpret "
                "with triglycerides, non-HDL, ApoB if available and metabolic phenotype."
            ),
        },
        {
            "id": "high_remnant_signal",
            "min": 1.2,
            "max": None,
            "label": "High remnant signal",
            "short_interpretation": "High calculated remnant cholesterol signal.",
            "clinical_context": (
                "High remnant cholesterol suggests substantial cholesterol in triglyceride-rich remnant particles. "
                "Interpret cautiously if LDL is calculated and triglycerides are high."
            ),
        },
    ],
}


FASTING_GLUCOSE = {
    "label": "Fasting glucose",
    "unit": "mmol/L",
    "type": "raw_lab_value",
    "metabolismx_concept": "achieved fasting glucose level / glucose regulation result variable",
    "levels": [
        {
            "id": "low_fasting_glucose_context_required",
            "min": None,
            "max": 4.0,
            "label": "Low fasting glucose / clinical context required",
            "short_interpretation": "Low fasting glucose; requires clinical and sampling context.",
            "clinical_context": (
                "Low fasting glucose should not be interpreted in isolation. Consider symptoms, fasting duration, "
                "medications, alcohol, illness and whether insulin or C-peptide are appropriate for the glucose level."
            ),
        },
        {
            "id": "optimal_fasting_range",
            "min": 4.0,
            "max": 5.0,
            "label": "Optimal fasting range",
            "short_interpretation": "Favourable achieved fasting glucose level.",
            "clinical_context": (
                "This glucose range is generally favourable, but normal fasting glucose can coexist with high fasting insulin "
                "or compensatory hyperinsulinaemia. Interpret with fasting insulin, HOMA-IR, C-peptide, TG/HDL, waist and TyG."
            ),
        },
        {
            "id": "high_normal_early_metabolic_drift_possible",
            "min": 5.0,
            "max": 5.6,
            "label": "High-normal / early metabolic drift possible",
            "short_interpretation": "High-normal fasting glucose; early drift is possible in context.",
            "clinical_context": (
                "This may still be within a non-diagnostic range, but becomes more meaningful when fasting insulin, "
                "HOMA-IR, C-peptide, TG/HDL, waist or TyG also suggest metabolic load."
            ),
        },
        {
            "id": "impaired_fasting_glucose_prediabetes_range",
            "min": 5.6,
            "max": 7.0,
            "label": "Impaired fasting glucose / prediabetes range",
            "short_interpretation": "Fasting glucose is in an ADA-style prediabetes range.",
            "clinical_context": (
                "Fasting glucose in this range can indicate impaired fasting glucose, but should be interpreted with HbA1c, "
                "repeat testing or other diagnostic methods as clinically appropriate. It may represent later-stage dysregulation "
                "compared with earlier compensatory hyperinsulinaemia."
            ),
        },
        {
            "id": "diabetes_range_requires_confirmation",
            "min": 7.0,
            "max": None,
            "label": "Diabetes range / requires clinical confirmation",
            "short_interpretation": "Fasting glucose is in the diabetes diagnostic range, requiring confirmation.",
            "clinical_context": (
                "A diabetes-range fasting glucose is not diagnosed by MetabolismX alone. It requires clinical confirmation, "
                "usually with repeat testing or another diagnostic method, unless clinical criteria allow otherwise."
            ),
        },
    ],
}


HBA1C = {
    "label": "HbA1c",
    "unit": "mmol/mol",
    "type": "raw_lab_value",
    "metabolismx_concept": "longer-term glycaemic exposure / glucose history without insulin cost",
    "levels": [
        {
            "id": "low_context_required",
            "min": None,
            "max": 31.0,
            "label": "Low / clinical context required",
            "short_interpretation": "Low HbA1c; requires clinical and haematological context.",
            "clinical_context": (
                "HbA1c reflects longer-term glycaemic exposure, but low values can be misleading in altered red cell "
                "turnover, anaemia, pregnancy, haemoglobin variants or other contexts. Interpret with fasting glucose "
                "and fasting insulin."
            ),
        },
        {
            "id": "favourable_glycaemic_exposure",
            "min": 31.0,
            "max": 39.0,
            "label": "Favourable glycaemic exposure",
            "short_interpretation": "Favourable longer-term glycaemic exposure.",
            "clinical_context": (
                "This range is generally reassuring for glycaemic exposure, but HbA1c does not show insulin cost. "
                "Compare with fasting glucose, fasting insulin, HOMA-IR and the broader metabolic pattern."
            ),
        },
        {
            "id": "high_normal_early_drift",
            "min": 39.0,
            "max": 42.0,
            "label": "High-normal / early drift",
            "short_interpretation": "Early upward glycaemic drift may be present.",
            "clinical_context": (
                "This range can signal early glycaemic drift in MetabolismX, especially when fasting insulin, HOMA-IR, "
                "TG/HDL, waist or TyG also suggest metabolic load. Interpret with local diagnostic frameworks."
            ),
        },
        {
            "id": "prediabetes_range",
            "min": 42.0,
            "max": 48.0,
            "label": "Prediabetes range",
            "short_interpretation": "HbA1c is in a prediabetes-style risk range.",
            "clinical_context": (
                "This range indicates increased glycaemic exposure and should be interpreted with fasting glucose, "
                "fasting insulin and clinical context. HbA1c can be misleading in altered red cell turnover, pregnancy, "
                "haemoglobin variants and related conditions."
            ),
        },
        {
            "id": "diabetes_range_requires_confirmation",
            "min": 48.0,
            "max": None,
            "label": "Diabetes range / requires clinical confirmation",
            "short_interpretation": "HbA1c is in the diabetes diagnostic range, requiring confirmation.",
            "clinical_context": (
                "A diabetes-range HbA1c is not diagnosed by MetabolismX alone. If classic symptoms are absent, clinical "
                "confirmation with repeat testing or another diagnostic method is required."
            ),
        },
    ],
}


BMI = {
    "label": "BMI",
    "unit": "kg/m2",
    "type": "calculated_marker",
    "metabolismx_concept": "crude body size marker / adiposity context marker",
    "levels": [
        {
            "id": "low_bmi_context_required",
            "min": None,
            "max": 18.5,
            "label": "Low BMI / context required",
            "short_interpretation": "Low BMI; clinical and body-composition context required.",
            "clinical_context": (
                "BMI is a crude body-size marker and does not distinguish fat mass, lean mass or fat distribution. "
                "Interpret with waist circumference, waist/height ratio and the metabolic profile."
            ),
        },
        {
            "id": "usual_reference_range",
            "min": 18.5,
            "max": 25.0,
            "label": "Usual reference range",
            "short_interpretation": "BMI is within the usual reference range.",
            "clinical_context": (
                "This range can still coexist with visceral adiposity or metabolic dysregulation. Interpret with waist, "
                "waist/height ratio, TG/HDL, insulin markers and blood pressure."
            ),
        },
        {
            "id": "overweight_range",
            "min": 25.0,
            "max": 30.0,
            "label": "Overweight range",
            "short_interpretation": "BMI is in the overweight range.",
            "clinical_context": (
                "This is a body-size signal, not a diagnosis of metabolic health. Interpret with waist circumference, "
                "waist/height ratio and laboratory markers of insulin resistance."
            ),
        },
        {
            "id": "obesity_range",
            "min": 30.0,
            "max": None,
            "label": "Obesity range",
            "short_interpretation": "BMI is in the obesity range.",
            "clinical_context": (
                "This can support a cardiometabolic load pattern, but BMI alone is insufficient. Interpret with visceral "
                "adiposity markers, blood pressure, glucose-insulin markers and atherogenic lipid profile."
            ),
        },
    ],
}


WAIST_CIRCUMFERENCE = {
    "label": "Waist circumference",
    "unit": "cm",
    "type": "raw_anthropometric_marker",
    "metabolismx_concept": "visceral adiposity / central cardiometabolic load signal",
    "missing_sex_interpretation": {
        "id": "requires_sex_specific_interpretation",
        "label": "Requires sex-specific interpretation",
        "short_interpretation": "Waist circumference requires sex-specific thresholds.",
        "clinical_context": (
            "Waist circumference is a practical marker of visceral adiposity, but interpretation requires sex-specific "
            "thresholds. Interpret with BMI, waist/height ratio, insulin resistance markers and lipid profile."
        ),
    },
    "levels": [
        {
            "id": "male_favourable",
            "sex": "male",
            "min": None,
            "max": 94.0,
            "label": "Favourable waist circumference",
            "short_interpretation": "Male waist circumference below the elevated threshold.",
            "clinical_context": (
                "Interpret with BMI, waist/height ratio, TG/HDL, fasting insulin, HOMA-IR, TyG and blood pressure."
            ),
        },
        {
            "id": "male_elevated",
            "sex": "male",
            "min": 94.0,
            "max": 102.0,
            "label": "Elevated waist circumference",
            "short_interpretation": "Elevated male waist circumference; visceral adiposity signal.",
            "clinical_context": (
                "Elevated waist circumference can support a central adiposity and insulin resistance pattern, especially "
                "with high TG/HDL, TyG, fasting insulin or blood pressure."
            ),
        },
        {
            "id": "male_high",
            "sex": "male",
            "min": 102.0,
            "max": None,
            "label": "High waist circumference",
            "short_interpretation": "High male waist circumference; strong visceral adiposity signal.",
            "clinical_context": (
                "High waist circumference strengthens a cardiometabolic load pattern when insulin, glucose, lipids or "
                "blood pressure are also unfavourable."
            ),
        },
        {
            "id": "female_favourable",
            "sex": "female",
            "min": None,
            "max": 80.0,
            "label": "Favourable waist circumference",
            "short_interpretation": "Female waist circumference below the elevated threshold.",
            "clinical_context": (
                "Interpret with BMI, waist/height ratio, TG/HDL, fasting insulin, HOMA-IR, TyG and blood pressure."
            ),
        },
        {
            "id": "female_elevated",
            "sex": "female",
            "min": 80.0,
            "max": 88.0,
            "label": "Elevated waist circumference",
            "short_interpretation": "Elevated female waist circumference; visceral adiposity signal.",
            "clinical_context": (
                "Elevated waist circumference can support a central adiposity and insulin resistance pattern, especially "
                "with high TG/HDL, TyG, fasting insulin or blood pressure."
            ),
        },
        {
            "id": "female_high",
            "sex": "female",
            "min": 88.0,
            "max": None,
            "label": "High waist circumference",
            "short_interpretation": "High female waist circumference; strong visceral adiposity signal.",
            "clinical_context": (
                "High waist circumference strengthens a cardiometabolic load pattern when insulin, glucose, lipids or "
                "blood pressure are also unfavourable."
            ),
        },
    ],
}


WAIST_HEIGHT_RATIO = {
    "label": "Waist/height ratio",
    "unit": "ratio",
    "type": "calculated_marker",
    "metabolismx_concept": "central adiposity scaled to body size / cardiometabolic load marker",
    "levels": [
        {
            "id": "favourable",
            "min": None,
            "max": 0.5,
            "label": "Favourable",
            "short_interpretation": "Favourable waist/height ratio.",
            "clinical_context": (
                "A waist/height ratio below 0.5 is generally favourable. Interpret with waist circumference, BMI, "
                "insulin resistance markers and lipid profile."
            ),
        },
        {
            "id": "elevated_cardiometabolic_risk_signal",
            "min": 0.5,
            "max": 0.6,
            "label": "Elevated cardiometabolic risk signal",
            "short_interpretation": "Elevated waist/height ratio; central adiposity signal.",
            "clinical_context": (
                "This range can indicate increased visceral adiposity and cardiometabolic load, especially with elevated "
                "fasting insulin, HOMA-IR, TG/HDL, TyG or blood pressure."
            ),
        },
        {
            "id": "high_cardiometabolic_risk_signal",
            "min": 0.6,
            "max": None,
            "label": "High cardiometabolic risk signal",
            "short_interpretation": "High waist/height ratio; strong central adiposity signal.",
            "clinical_context": (
                "A high waist/height ratio strengthens the interpretation of visceral adiposity and metabolic load. "
                "Interpret with the full glucose-insulin, lipid and blood pressure profile."
            ),
        },
    ],
}


C_PEPTIDE = {
    "label": "C-peptide",
    "unit": "nmol/L",
    "type": "raw_lab_value",
    "metabolismx_concept": "endogenous insulin secretion / beta-cell output / compensation signal",
    "levels": [
        {
            "id": "low_endogenous_insulin_secretion_context_required",
            "min": None,
            "max": 0.3,
            "label": "Low endogenous insulin secretion / clinical context required",
            "short_interpretation": "Low C-peptide; clinical context is required.",
            "clinical_context": (
                "C-peptide reflects endogenous insulin secretion and must be interpreted with glucose and insulin. "
                "Low C-peptide with high glucose may suggest insufficient insulin secretion and requires clinical assessment."
            ),
        },
        {
            "id": "lower_to_usual_fasting_range",
            "min": 0.3,
            "max": 0.7,
            "label": "Lower to usual fasting range",
            "short_interpretation": "Lower-to-usual endogenous insulin output in fasting context.",
            "clinical_context": (
                "Interpret with simultaneous glucose, insulin and fasting status. C-peptide interpretation depends on "
                "sampling context and kidney function."
            ),
        },
        {
            "id": "higher_endogenous_output_possible_compensation",
            "min": 0.7,
            "max": 1.2,
            "label": "Higher endogenous insulin output / possible compensation",
            "short_interpretation": "May reflect higher beta-cell output or compensation.",
            "clinical_context": (
                "Higher C-peptide with normal or high-normal glucose can reflect compensatory beta-cell output. Interpret "
                "with fasting insulin, HOMA-IR, TG/HDL, waist and TyG."
            ),
        },
        {
            "id": "high_endogenous_output_metabolic_load_signal",
            "min": 1.2,
            "max": None,
            "label": "High endogenous insulin output / metabolic load signal",
            "short_interpretation": "High C-peptide can support a metabolic load pattern.",
            "clinical_context": (
                "High C-peptide can reflect increased endogenous insulin secretion, insulin resistance or reduced renal "
                "clearance. Interpret with glucose, insulin, kidney function, fasting status and the broader metabolic profile."
            ),
        },
    ],
}


FASTING_INSULIN = {
    "label": "Fasting insulin",
    "unit": "mIU/L",
    "type": "raw_lab_value",
    "metabolismx_concept": "metabolic load / compensatory hyperinsulinaemia / insulin resistance signal",
    "levels": [
        {
            "id": "low_insulin_sensitive_pattern",
            "min": None,
            "max": 5.0,
            "label": "Low / insulin-sensitive pattern",
            "short_interpretation": "Low fasting insulin, often compatible with low metabolic insulin demand.",
            "clinical_context": (
                "Fasting insulin must be interpreted with fasting glucose, HOMA-IR, C-peptide, TG/HDL, waist and TyG. "
                "A low value may be favourable in the right context, but interpretation changes if glucose is elevated "
                "or beta-cell function is clinically uncertain."
            ),
        },
        {
            "id": "favourable_usual_fasting_range",
            "min": 5.0,
            "max": 10.0,
            "label": "Favourable / usual fasting range",
            "short_interpretation": "Usually compatible with moderate fasting insulin demand.",
            "clinical_context": (
                "This range is generally reassuring when fasting glucose, HOMA-IR, C-peptide, TG/HDL, waist and TyG "
                "are also favourable. Fasting insulin is more volatile than glucose and depends on standardised fasting sampling."
            ),
        },
        {
            "id": "early_hyperinsulinaemia_metabolic_load_signal",
            "min": 10.0,
            "max": 15.0,
            "label": "Early hyperinsulinaemia / metabolic load signal",
            "short_interpretation": "May suggest increased insulin demand before glucose becomes abnormal.",
            "clinical_context": (
                "A normal fasting glucose with insulin in this range can indicate compensatory hyperinsulinaemia. "
                "Interpret with HOMA-IR, C-peptide, TG/HDL, waist, TyG and repeated or standardised sampling context."
            ),
        },
        {
            "id": "clear_hyperinsulinaemia_insulin_resistance_signal",
            "min": 15.0,
            "max": 25.0,
            "label": "Clear hyperinsulinaemia / insulin resistance signal",
            "short_interpretation": "Clear signal of increased metabolic insulin demand.",
            "clinical_context": (
                "High fasting insulin is not a diabetes diagnosis, but it can indicate compensation for insulin resistance, "
                "especially when HOMA-IR, TG/HDL, waist, glucose or TyG are also elevated."
            ),
        },
        {
            "id": "marked_hyperinsulinaemia_high_metabolic_load",
            "min": 25.0,
            "max": None,
            "label": "Marked hyperinsulinaemia / high metabolic load",
            "short_interpretation": "Markedly elevated fasting insulin; high metabolic load signal.",
            "clinical_context": (
                "This level should be interpreted cautiously and in clinical context. It may reflect substantial compensation, "
                "reduced insulin clearance, assay differences or sampling conditions. It should be assessed with fasting glucose, "
                "HOMA-IR, C-peptide, TG/HDL, waist, TyG and the broader clinical profile."
            ),
        },
    ],
}


HOMA_IR = {
    "label": "HOMA-IR",
    "unit": "index",
    "type": "calculated_marker",
    "metabolismx_concept": "fasting-state insulin resistance estimate / insulin cost of glucose control",
    "levels": [
        {
            "id": "insulin_sensitive_low_metabolic_load",
            "min": None,
            "max": 1.0,
            "label": "Insulin-sensitive / low metabolic load",
            "short_interpretation": "Low HOMA-IR, compatible with low fasting insulin-glucose load.",
            "clinical_context": (
                "HOMA-IR is a model-based estimate, not a direct measurement. A low value is most meaningful when fasting "
                "glucose, fasting insulin, C-peptide, TG/HDL, waist and TyG are also favourable."
            ),
        },
        {
            "id": "favourable_usual_range",
            "min": 1.0,
            "max": 2.0,
            "label": "Favourable / usual range",
            "short_interpretation": "Usually compatible with a favourable fasting insulin-glucose relationship.",
            "clinical_context": (
                "This range is generally reassuring in context. HOMA-IR requires fasting glucose and fasting insulin, "
                "and should be interpreted with C-peptide, TG/HDL, waist and TyG."
            ),
        },
        {
            "id": "borderline_early_insulin_resistance_signal",
            "min": 2.0,
            "max": 2.5,
            "label": "Borderline / early insulin resistance signal",
            "short_interpretation": "May suggest early fasting-state insulin resistance.",
            "clinical_context": (
                "This range can indicate early metabolic load, especially when fasting insulin is elevated or TG/HDL, "
                "waist or TyG also suggest insulin resistance. Cutoffs vary between populations."
            ),
        },
        {
            "id": "insulin_resistance_signal",
            "min": 2.5,
            "max": 4.0,
            "label": "Insulin resistance signal",
            "short_interpretation": "Suggests increased insulin cost for fasting glucose control.",
            "clinical_context": (
                "Elevated HOMA-IR can occur before fasting glucose reaches the diabetes range. Interpret with fasting insulin, "
                "fasting glucose, C-peptide, TG/HDL, waist and TyG. This is not a diagnostic criterion."
            ),
        },
        {
            "id": "marked_insulin_resistance_high_metabolic_load",
            "min": 4.0,
            "max": None,
            "label": "Marked insulin resistance / high metabolic load",
            "short_interpretation": "Markedly elevated fasting insulin-glucose load.",
            "clinical_context": (
                "This level suggests high fasting-state metabolic load, but HOMA-IR remains a model-based estimate rather "
                "than a direct clamp measurement. Interpret with the full metabolic profile and population context."
            ),
        },
    ],
}


QUICKI = {
    "label": "QUICKI",
    "unit": "index",
    "type": "calculated_marker",
    "metabolismx_concept": "inverse insulin sensitivity estimate from fasting insulin and glucose",
    "levels": [
        {
            "id": "favourable_insulin_sensitivity_pattern",
            "min": 0.36,
            "max": None,
            "label": "Favourable insulin sensitivity pattern",
            "short_interpretation": "Higher QUICKI, generally compatible with better insulin sensitivity.",
            "clinical_context": (
                "QUICKI is model-based and not a direct clamp measurement. It uses fasting insulin and glucose, with "
                "glucose in mg/dL and insulin in uU/mL internally. Interpret with HOMA-IR, fasting insulin and fasting glucose."
            ),
        },
        {
            "id": "intermediate",
            "min": 0.33,
            "max": 0.36,
            "label": "Intermediate",
            "short_interpretation": "Intermediate QUICKI; context determines significance.",
            "clinical_context": (
                "This range should be interpreted with HOMA-IR, fasting insulin, fasting glucose, C-peptide, TG/HDL, "
                "waist and TyG."
            ),
        },
        {
            "id": "insulin_resistance_signal",
            "min": 0.30,
            "max": 0.33,
            "label": "Insulin resistance signal",
            "short_interpretation": "Lower QUICKI suggests reduced insulin sensitivity.",
            "clinical_context": (
                "A low QUICKI can support an insulin resistance pattern when HOMA-IR, fasting insulin, TG/HDL, waist "
                "or TyG are also unfavourable. It remains a model-based estimate."
            ),
        },
        {
            "id": "marked_insulin_resistance_signal",
            "min": None,
            "max": 0.30,
            "label": "Marked insulin resistance signal",
            "short_interpretation": "Markedly low QUICKI; strong reduced insulin sensitivity signal.",
            "clinical_context": (
                "This level suggests a stronger insulin resistance signal, but QUICKI should not be interpreted alone. "
                "Assess with HOMA-IR, fasting insulin, fasting glucose and the broader metabolic profile."
            ),
        },
    ],
}


TYG_INDEX = {
    "label": "TyG index",
    "unit": "index",
    "type": "calculated_marker",
    "metabolismx_concept": "triglyceride-glucose link / insulin resistance and VLDL-glucose metabolism signal",
    "levels": [
        {
            "id": "favourable_pattern",
            "min": None,
            "max": 8.5,
            "label": "Favourable pattern",
            "short_interpretation": "Favourable triglyceride-glucose pattern.",
            "clinical_context": (
                "TyG links glucose handling with triglyceride-rich lipoprotein metabolism. A favourable value is most "
                "reassuring when TG, HDL, fasting insulin, HOMA-IR, waist and BMI are also favourable."
            ),
        },
        {
            "id": "intermediate_early_metabolic_drift",
            "min": 8.5,
            "max": 9.0,
            "label": "Intermediate / early metabolic drift",
            "short_interpretation": "Intermediate TyG; early metabolic drift is possible.",
            "clinical_context": (
                "Interpret with triglycerides, HDL, fasting insulin, HOMA-IR, waist and BMI. Cutoffs vary between studies "
                "and populations."
            ),
        },
        {
            "id": "insulin_resistance_metabolic_signal",
            "min": 9.0,
            "max": 9.5,
            "label": "Insulin resistance / metabolic signal",
            "short_interpretation": "Suggests a triglyceride-glucose metabolic risk pattern.",
            "clinical_context": (
                "TyG uses glucose and triglycerides in mg/dL internally. A value in this range can support an insulin "
                "resistance pattern, especially with high TG/HDL, elevated fasting insulin or increased waist."
            ),
        },
        {
            "id": "strong_metabolic_dysregulation_signal",
            "min": 9.5,
            "max": None,
            "label": "Strong metabolic dysregulation signal",
            "short_interpretation": "Strong triglyceride-glucose dysregulation signal.",
            "clinical_context": (
                "This level suggests stronger metabolic dysregulation linking glycaemia and triglyceride/VLDL metabolism. "
                "Interpret with TG, HDL, fasting insulin, HOMA-IR, waist, BMI and the clinical risk profile."
            ),
        },
    ],
}


LDL_HDL_RATIO = {
    "label": "LDL/HDL ratio",
    "unit": "ratio",
    "type": "calculated_marker",
    "metabolismx_concept": "context ratio for LDL burden relative to HDL concentration",
    "levels": [
        {
            "id": "favourable_ratio",
            "min": None,
            "max": 2.0,
            "label": "Favourable ratio",
            "short_interpretation": "Favourable LDL/HDL ratio.",
            "clinical_context": (
                "LDL/HDL ratio is a context marker, not a primary treatment target. Interpret with LDL, non-HDL, ApoB "
                "if available, triglycerides and total risk."
            ),
        },
        {
            "id": "intermediate",
            "min": 2.0,
            "max": 3.0,
            "label": "Intermediate",
            "short_interpretation": "Intermediate LDL/HDL ratio.",
            "clinical_context": (
                "Interpret as a communication and context marker. It should not override LDL, non-HDL, ApoB or total "
                "cardiovascular risk assessment."
            ),
        },
        {
            "id": "elevated_ratio",
            "min": 3.0,
            "max": 4.0,
            "label": "Elevated ratio",
            "short_interpretation": "Elevated LDL/HDL ratio.",
            "clinical_context": (
                "An elevated ratio can support an atherogenic lipid pattern, especially with high non-HDL, high TG/HDL "
                "or metabolic risk markers."
            ),
        },
        {
            "id": "high_ratio",
            "min": 4.0,
            "max": None,
            "label": "High ratio",
            "short_interpretation": "High LDL/HDL ratio.",
            "clinical_context": (
                "High LDL/HDL ratio suggests an unfavourable lipid balance, but remains secondary to LDL/non-HDL/ApoB "
                "and total risk context."
            ),
        },
    ],
}


TOTAL_HDL_RATIO = {
    "label": "Total/HDL ratio",
    "unit": "ratio",
    "type": "calculated_marker",
    "metabolismx_concept": "broad cholesterol balance ratio / risk communication marker",
    "levels": [
        {
            "id": "favourable_ratio",
            "min": None,
            "max": 3.5,
            "label": "Favourable ratio",
            "short_interpretation": "Favourable total/HDL ratio.",
            "clinical_context": (
                "Total/HDL ratio can support risk communication, but it is not a primary treatment target. Interpret "
                "with LDL, non-HDL, triglycerides, remnant cholesterol and total risk."
            ),
        },
        {
            "id": "intermediate_context_dependent",
            "min": 3.5,
            "max": 5.0,
            "label": "Intermediate / context dependent",
            "short_interpretation": "Intermediate total/HDL ratio.",
            "clinical_context": (
                "This ratio depends heavily on the composition of total cholesterol and HDL. Break down into LDL, HDL, "
                "non-HDL, remnants and triglycerides."
            ),
        },
        {
            "id": "elevated_ratio",
            "min": 5.0,
            "max": 6.0,
            "label": "Elevated ratio",
            "short_interpretation": "Elevated total/HDL ratio.",
            "clinical_context": (
                "An elevated ratio can support an unfavourable lipid pattern, particularly when non-HDL, LDL, TG/HDL "
                "or remnant cholesterol are also elevated."
            ),
        },
        {
            "id": "high_ratio",
            "min": 6.0,
            "max": None,
            "label": "High ratio",
            "short_interpretation": "High total/HDL ratio.",
            "clinical_context": (
                "High total/HDL ratio is an unfavourable context marker. It should be interpreted with direct lipid fractions, "
                "atherogenic particle burden and total risk."
            ),
        },
    ],
}


BLOOD_PRESSURE = {
    "label": "Blood pressure",
    "unit": "mmHg",
    "type": "raw_clinical_marker",
    "metabolismx_concept": "haemodynamic load / vascular, renal and metabolic stress signal",
    "levels": [
        {
            "id": "optimal_non_elevated",
            "match": "below_and",
            "sbp_max": 120.0,
            "dbp_max": 70.0,
            "severity": 0,
            "label": "Optimal / non-elevated",
            "short_interpretation": "Optimal non-elevated blood pressure pattern.",
            "clinical_context": (
                "Blood pressure should be interpreted from optimal upward, not only from the hypertension threshold. "
                "Interpret with metabolic profile, vascular context and measurement quality."
            ),
        },
        {
            "id": "early_elevation_non_optimal",
            "match": "threshold_or",
            "sbp_min": 120.0,
            "dbp_min": 70.0,
            "severity": 1,
            "label": "Early elevation / non-optimal",
            "short_interpretation": "Early blood pressure elevation signal.",
            "clinical_context": (
                "This is below the classic hypertension threshold but may still represent increased haemodynamic exposure, "
                "especially with metabolic risk factors."
            ),
        },
        {
            "id": "elevated_risk_relevant",
            "match": "threshold_or",
            "sbp_min": 130.0,
            "dbp_min": 80.0,
            "severity": 2,
            "label": "Elevated / risk-relevant",
            "short_interpretation": "Risk-relevant elevated blood pressure pattern.",
            "clinical_context": (
                "This range is metabolically relevant, especially with central adiposity, insulin resistance, dyslipidaemia "
                "or high total cardiovascular risk."
            ),
        },
        {
            "id": "hypertension_range",
            "match": "threshold_or",
            "sbp_min": 140.0,
            "dbp_min": 90.0,
            "severity": 3,
            "label": "Hypertension range",
            "short_interpretation": "Blood pressure is in a hypertension range.",
            "clinical_context": (
                "This range requires clinical interpretation and confirmation according to measurement context. "
                "MetabolismX does not diagnose hypertension from a single reading."
            ),
        },
        {
            "id": "high_hypertension_range",
            "match": "threshold_or",
            "sbp_min": 160.0,
            "dbp_min": 100.0,
            "severity": 4,
            "label": "High hypertension range",
            "short_interpretation": "High blood pressure burden.",
            "clinical_context": (
                "This suggests substantial haemodynamic load and requires clinical context, repeated measurement and risk assessment."
            ),
        },
        {
            "id": "severe_hypertension_urgent_assessment",
            "match": "threshold_or",
            "sbp_min": 180.0,
            "dbp_min": 110.0,
            "severity": 5,
            "label": "Severe hypertension range / urgent clinical assessment",
            "short_interpretation": "Severe blood pressure elevation signal.",
            "clinical_context": (
                "This range can require urgent clinical assessment, especially with symptoms or signs of organ injury. "
                "MetabolismX should flag, not manage, this situation."
            ),
        },
    ],
}


MEAN_ARTERIAL_PRESSURE = {
    "label": "Mean arterial pressure",
    "unit": "mmHg",
    "type": "calculated_marker",
    "metabolismx_concept": "continuous arterial pressure load / haemodynamic context marker",
    "levels": [
        {
            "id": "low_context_required",
            "min": None,
            "max": 70.0,
            "label": "Low / clinical context required",
            "short_interpretation": "Low MAP; clinical context required.",
            "clinical_context": (
                "MAP is a haemodynamic context marker. Low values require interpretation with symptoms, measurement context, "
                "blood pressure, medications and clinical state."
            ),
        },
        {
            "id": "usual_range",
            "min": 70.0,
            "max": 93.0,
            "label": "Usual range",
            "short_interpretation": "MAP is in a usual haemodynamic range.",
            "clinical_context": (
                "Interpret MAP with systolic and diastolic blood pressure, pulse pressure and the broader cardiometabolic profile."
            ),
        },
        {
            "id": "elevated_haemodynamic_load",
            "min": 93.0,
            "max": 105.0,
            "label": "Elevated haemodynamic load",
            "short_interpretation": "Elevated mean arterial pressure.",
            "clinical_context": (
                "Elevated MAP can signal increased continuous arterial pressure load. Interpret with blood pressure category, "
                "kidney/metabolic context and measurement quality."
            ),
        },
        {
            "id": "high_haemodynamic_load",
            "min": 105.0,
            "max": None,
            "label": "High haemodynamic load",
            "short_interpretation": "High mean arterial pressure.",
            "clinical_context": (
                "High MAP suggests high continuous pressure burden. It is a context marker and does not replace blood pressure "
                "classification or clinical assessment."
            ),
        },
    ],
}


PULSE_PRESSURE = {
    "label": "Pulse pressure",
    "unit": "mmHg",
    "type": "calculated_marker",
    "metabolismx_concept": "systolic-diastolic pressure gap / arterial stiffness and stroke volume load context",
    "levels": [
        {
            "id": "low_context_required",
            "min": None,
            "max": 30.0,
            "label": "Low / context required",
            "short_interpretation": "Low pulse pressure; clinical context required.",
            "clinical_context": (
                "Low pulse pressure should be interpreted with symptoms, measurement quality, blood pressure level and "
                "clinical state."
            ),
        },
        {
            "id": "usual_range",
            "min": 30.0,
            "max": 50.0,
            "label": "Usual range",
            "short_interpretation": "Pulse pressure is in a usual range.",
            "clinical_context": (
                "Pulse pressure is a haemodynamic context marker. Interpret with age, systolic pressure, diastolic pressure, "
                "MAP and cardiometabolic risk."
            ),
        },
        {
            "id": "elevated_arterial_load_signal",
            "min": 50.0,
            "max": 60.0,
            "label": "Elevated arterial load signal",
            "short_interpretation": "Elevated pulse pressure; arterial load signal.",
            "clinical_context": (
                "Elevated pulse pressure may reflect increased arterial stiffness or stroke volume load. Interpret with age, "
                "blood pressure, MAP and vascular risk context."
            ),
        },
        {
            "id": "high_pulse_pressure_arterial_stiffness_signal",
            "min": 60.0,
            "max": None,
            "label": "High pulse pressure / arterial stiffness signal",
            "short_interpretation": "High pulse pressure; possible arterial stiffness signal.",
            "clinical_context": (
                "High pulse pressure can support a haemodynamic load pattern, particularly in older adults or vascular disease "
                "contexts. It should not be interpreted as a diagnosis in isolation."
            ),
        },
    ],
}


TG_HDL_RATIO = {
    "label": "TG/HDL ratio",
    "unit": "ratio, mmol/L based",
    "type": "calculated_marker",
    "metabolismx_concept": "atherogenic dyslipidaemia / insulin-resistant lipid pattern",
    "levels": [
        {
            "id": "insulin_sensitive_pattern",
            "min": None,
            "max": 1.0,
            "label": "Insulin-sensitive pattern",
            "short_interpretation": "Favourable TG/HDL pattern.",
            "clinical_context": (
                "Low TG/HDL ratio is generally compatible with better insulin sensitivity and less atherogenic dyslipidaemia."
            ),
        },
        {
            "id": "borderline",
            "min": 1.0,
            "max": 1.5,
            "label": "Borderline",
            "short_interpretation": "Intermediate pattern.",
            "clinical_context": (
                "Interpret with waist, fasting insulin, fasting glucose, HOMA-IR and TyG."
            ),
        },
        {
            "id": "early_ir_signal",
            "min": 1.5,
            "max": 2.0,
            "label": "Early insulin resistance signal",
            "short_interpretation": "Suggests early insulin-resistant lipid pattern.",
            "clinical_context": (
                "This can indicate emerging atherogenic dyslipidaemia, particularly when waist, insulin or glucose markers are also elevated."
            ),
        },
        {
            "id": "strong_ir_atherogenic_pattern",
            "min": 2.0,
            "max": None,
            "label": "Strong insulin resistance / atherogenic dyslipidaemia pattern",
            "short_interpretation": "Strong metabolic risk signal.",
            "clinical_context": (
                "High TG/HDL ratio together with elevated triglycerides, low HDL, central adiposity or high insulin markers "
                "supports an insulin-resistant, atherogenic phenotype."
            ),
        },
    ],
}
