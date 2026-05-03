import math

from metabolic_modifier_system.interpretation import interpret_blood_pressure, interpret_value, interpret_waist
from metabolic_modifier_system.reference_values import (
    BLOOD_PRESSURE,
    BMI,
    C_PEPTIDE,
    FASTING_GLUCOSE,
    FASTING_INSULIN,
    HBA1C,
    HDL,
    HOMA_IR,
    LDL_CHOLESTEROL,
    LDL_HDL_RATIO,
    MEAN_ARTERIAL_PRESSURE,
    NON_HDL_CHOLESTEROL,
    PULSE_PRESSURE,
    QUICKI,
    REMNANT_CHOLESTEROL,
    TG_HDL_RATIO,
    TOTAL_CHOLESTEROL,
    TOTAL_HDL_RATIO,
    TRIGLYCERIDES,
    TYG_INDEX,
    WAIST_CIRCUMFERENCE,
    WAIST_HEIGHT_RATIO,
)
from metabolic_modifier_system.summary_models import (
    calculate_metabolic_burden_score,
    calculate_metabolic_syndrome_components,
    summarise_atherogenic_dyslipidaemia,
    summarise_insulin_resistance_pattern,
)

# =========================
# VALIDATION / REFERENCES
# =========================
#
# Input units:
# - glucose: mmol/L
# - insulin: mIU/L
# - triglycerides: mmol/L
# - HbA1c: mmol/mol
#
# HOMA-IR:
# fasting insulin (mIU/L) * fasting glucose (mmol/L) / 22.5
# Source: Matthews et al., Diabetologia, 1985
#
# QUICKI:
# 1 / (log10(insulin µU/mL) + log10(glucose mg/dL))
# Source: Katz et al., JCEM, 2000
#
# TyG:
# ln((triglycerides mg/dL * glucose mg/dL) / 2)
# Commonly used TyG index formula; requires mg/dL conversion.
#
# eAG:
# estimated average glucose mmol/L = 0.146 * HbA1c mmol/mol + 0.837
# Derived from ADAG relationship.

# =========================
# INPUT DATA (rådata)
# =========================

patient = {
    "name": "Test Testsson",
    "sex": "male",

    "fasting_glucose": 5.8,        # mmol/L
    "fasting_insulin": 14,         # mIU/L
    "c_peptide": 0.95,             # nmol/L
    "hba1c": 39,                   # mmol/mol

    "total_cholesterol": 5.4,      # mmol/L
    "ldl": 3.3,                    # mmol/L
    "hdl": 1.0,                    # mmol/L
    "triglycerides": 2.1,          # mmol/L

    "height_cm": 178,
    "weight_kg": 94,
    "waist_cm": 104,

    "systolic_bp": 138,
    "diastolic_bp": 86,
}

def calculate_expanded_labs(patient):

    fasting_glucose = patient["fasting_glucose"]
    fasting_insulin = patient["fasting_insulin"]
    c_peptide = patient["c_peptide"]
    hba1c = patient["hba1c"]

    total_cholesterol = patient["total_cholesterol"]
    ldl = patient["ldl"]
    hdl = patient["hdl"]
    triglycerides = patient["triglycerides"]

    height_cm = patient["height_cm"]
    weight_kg = patient["weight_kg"]
    waist_cm = patient["waist_cm"]

    systolic_bp = patient["systolic_bp"]
    diastolic_bp = patient["diastolic_bp"]

    # UNIT CONVERSIONS
    fasting_glucose_mg_dl = fasting_glucose * 18.018
    triglycerides_mg_dl = triglycerides * 88.57

    # CALCULATIONS
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    waist_height_ratio = waist_cm / height_cm

    homa_ir = fasting_insulin * fasting_glucose / 22.5
    quicki = 1 / (math.log10(fasting_insulin) + math.log10(fasting_glucose_mg_dl))

    tyg_index = math.log((triglycerides_mg_dl * fasting_glucose_mg_dl) / 2)
    tyg_bmi = tyg_index * bmi
    tyg_waist = tyg_index * waist_cm

    insulin_glucose_ratio = fasting_insulin / fasting_glucose
    c_peptide_glucose_ratio = c_peptide / fasting_glucose
    insulin_c_peptide_ratio = fasting_insulin / c_peptide

    estimated_average_glucose_mmol_l = 0.146 * hba1c + 0.837

    non_hdl = total_cholesterol - hdl
    remnant_cholesterol = total_cholesterol - ldl - hdl
    tg_hdl_ratio = triglycerides / hdl
    total_hdl_ratio = total_cholesterol / hdl
    ldl_hdl_ratio = ldl / hdl

    pulse_pressure = systolic_bp - diastolic_bp
    mean_arterial_pressure = diastolic_bp + pulse_pressure / 3

    return {
        "bmi": bmi,
        "waist_height_ratio": waist_height_ratio,
        "homa_ir": homa_ir,
        "quicki": quicki,
        "tyg_index": tyg_index,
        "tyg_bmi": tyg_bmi,
        "tyg_waist": tyg_waist,
        "insulin_glucose_ratio": insulin_glucose_ratio,
        "c_peptide_glucose_ratio": c_peptide_glucose_ratio,
        "insulin_c_peptide_ratio": insulin_c_peptide_ratio,
        "eAG": estimated_average_glucose_mmol_l,
        "non_hdl": non_hdl,
        "remnant": remnant_cholesterol,
        "tg_hdl_ratio": tg_hdl_ratio,
        "total_hdl_ratio": total_hdl_ratio,
        "ldl_hdl_ratio": ldl_hdl_ratio,
        "pulse_pressure": pulse_pressure,
        "map": mean_arterial_pressure,
    }

def print_expanded_lab_report(patient, results):
    name = patient["name"]

    print(f"\nEXPANDED LAB LIST: {name}")
    print("=================")

    print("\nBODY / ADIPOSITY")
    print("----------------")
    bmi_level = interpret_value(results["bmi"], BMI)
    waist_level = interpret_waist(patient["waist_cm"], patient.get("sex"), WAIST_CIRCUMFERENCE)
    waist_height_level = interpret_value(results["waist_height_ratio"], WAIST_HEIGHT_RATIO)

    print(f"BMI: {results['bmi']:.2f}")
    if bmi_level is not None:
        print(f"BMI interpretation: {bmi_level['label']}")
    print(f"Waist circumference: {patient['waist_cm']:.0f} cm")
    if waist_level is not None:
        print(f"Waist circumference interpretation: {waist_level['label']}")
    print(f"Waist/height ratio: {results['waist_height_ratio']:.2f}")
    if waist_height_level is not None:
        print(f"Waist/height ratio interpretation: {waist_height_level['label']}")

    print("\nGLUCOSE–INSULIN AXIS")
    print("--------------------")
    fasting_glucose_level = interpret_value(patient["fasting_glucose"], FASTING_GLUCOSE)
    fasting_insulin_level = interpret_value(patient["fasting_insulin"], FASTING_INSULIN)
    c_peptide_level = interpret_value(patient["c_peptide"], C_PEPTIDE)
    hba1c_level = interpret_value(patient["hba1c"], HBA1C)
    homa_ir_level = interpret_value(results["homa_ir"], HOMA_IR)
    quicki_level = interpret_value(results["quicki"], QUICKI)
    tyg_index_level = interpret_value(results["tyg_index"], TYG_INDEX)

    print(f"Fasting glucose: {patient['fasting_glucose']:.2f} mmol/L")
    if fasting_glucose_level is not None:
        print(f"Fasting glucose interpretation: {fasting_glucose_level['label']}")
    print(f"Fasting insulin: {patient['fasting_insulin']:.2f} mIU/L")
    if fasting_insulin_level is not None:
        print(f"Fasting insulin interpretation: {fasting_insulin_level['label']}")
    print(f"C-peptide: {patient['c_peptide']:.2f} nmol/L")
    if c_peptide_level is not None:
        print(f"C-peptide interpretation: {c_peptide_level['label']}")
    print(f"HbA1c: {patient['hba1c']:.0f} mmol/mol")
    if hba1c_level is not None:
        print(f"HbA1c interpretation: {hba1c_level['label']}")
    print(f"Estimated average glucose: {results['eAG']:.2f} mmol/L")
    print(f"HOMA-IR: {results['homa_ir']:.2f}")
    if homa_ir_level is not None:
        print(f"HOMA-IR interpretation: {homa_ir_level['label']}")
    print(f"QUICKI: {results['quicki']:.3f}")
    if quicki_level is not None:
        print(f"QUICKI interpretation: {quicki_level['label']}")
    print(f"TyG index: {results['tyg_index']:.2f}")
    if tyg_index_level is not None:
        print(f"TyG index interpretation: {tyg_index_level['label']}")
    print(f"TyG-BMI: {results['tyg_bmi']:.2f}")
    print(f"TyG-waist: {results['tyg_waist']:.2f}")
    print(f"Insulin/glucose ratio: {results['insulin_glucose_ratio']:.2f}")
    print(f"C-peptide/glucose ratio: {results['c_peptide_glucose_ratio']:.3f}")
    print(f"Insulin/C-peptide ratio: {results['insulin_c_peptide_ratio']:.2f}")

    print("\nLIPID / ATHEROGENIC AXIS")
    print("------------------------")
    total_cholesterol_level = interpret_value(patient["total_cholesterol"], TOTAL_CHOLESTEROL)
    ldl_level = interpret_value(patient["ldl"], LDL_CHOLESTEROL)
    triglycerides_level = interpret_value(patient["triglycerides"], TRIGLYCERIDES)
    hdl_level = interpret_value(patient["hdl"], HDL)
    non_hdl_level = interpret_value(results["non_hdl"], NON_HDL_CHOLESTEROL)
    remnant_level = interpret_value(results["remnant"], REMNANT_CHOLESTEROL)
    tg_hdl_level = interpret_value(results["tg_hdl_ratio"], TG_HDL_RATIO)
    total_hdl_level = interpret_value(results["total_hdl_ratio"], TOTAL_HDL_RATIO)
    ldl_hdl_level = interpret_value(results["ldl_hdl_ratio"], LDL_HDL_RATIO)

    print(f"Total cholesterol: {patient['total_cholesterol']:.2f} mmol/L")
    if total_cholesterol_level is not None:
        print(f"Total cholesterol interpretation: {total_cholesterol_level['label']}")
    print(f"LDL cholesterol: {patient['ldl']:.2f} mmol/L")
    if ldl_level is not None:
        print(f"LDL cholesterol interpretation: {ldl_level['label']}")
    print(f"HDL cholesterol: {patient['hdl']:.2f} mmol/L")
    if hdl_level is not None:
        print(f"HDL interpretation: {hdl_level['label']}")
    print(f"Triglycerides: {patient['triglycerides']:.2f} mmol/L")
    if triglycerides_level is not None:
        print(f"Triglycerides interpretation: {triglycerides_level['label']}")
    print(f"Non-HDL cholesterol: {results['non_hdl']:.2f} mmol/L")
    if non_hdl_level is not None:
        print(f"Non-HDL cholesterol interpretation: {non_hdl_level['label']}")
    print(f"Remnant cholesterol: {results['remnant']:.2f} mmol/L")
    if remnant_level is not None:
        print(f"Remnant cholesterol interpretation: {remnant_level['label']}")
    print(f"TG/HDL ratio: {results['tg_hdl_ratio']:.2f}")
    if tg_hdl_level is not None:
        print(f"TG/HDL interpretation: {tg_hdl_level['label']}")
    print(f"Total/HDL ratio: {results['total_hdl_ratio']:.2f}")
    if total_hdl_level is not None:
        print(f"Total/HDL interpretation: {total_hdl_level['label']}")
    print(f"LDL/HDL ratio: {results['ldl_hdl_ratio']:.2f}")
    if ldl_hdl_level is not None:
        print(f"LDL/HDL interpretation: {ldl_hdl_level['label']}")

    print("\nBLOOD PRESSURE / HEMODYNAMICS")
    print("-----------------------------")
    blood_pressure_level = interpret_blood_pressure(
        patient["systolic_bp"],
        patient["diastolic_bp"],
        BLOOD_PRESSURE,
    )
    pulse_pressure_level = interpret_value(results["pulse_pressure"], PULSE_PRESSURE)
    map_level = interpret_value(results["map"], MEAN_ARTERIAL_PRESSURE)

    print(f"Systolic BP: {patient['systolic_bp']:.0f} mmHg")
    print(f"Diastolic BP: {patient['diastolic_bp']:.0f} mmHg")
    if blood_pressure_level is not None:
        print(f"Blood pressure interpretation: {blood_pressure_level['label']}")
    print(f"Pulse pressure: {results['pulse_pressure']:.0f} mmHg")
    if pulse_pressure_level is not None:
        print(f"Pulse pressure interpretation: {pulse_pressure_level['label']}")
    print(f"Mean arterial pressure: {results['map']:.1f} mmHg")
    if map_level is not None:
        print(f"MAP interpretation: {map_level['label']}")

    print("\nMETABOLISM X SUMMARY")
    print("--------------------")
    metabolic_syndrome = calculate_metabolic_syndrome_components(patient, results)
    metabolic_burden = calculate_metabolic_burden_score(patient, results)
    insulin_resistance = summarise_insulin_resistance_pattern(patient, results)
    atherogenic_dyslipidaemia = summarise_atherogenic_dyslipidaemia(patient, results)

    meets_3_of_5 = "yes" if metabolic_syndrome["meets_3_of_5"] else "no"
    print(f"Metabolic syndrome components: {metabolic_syndrome['component_count']}/5")
    print(f"Meets 3-of-5 criterion: {meets_3_of_5}")
    print(f"Metabolic burden score: {metabolic_burden['score']} ({metabolic_burden['level']})")
    print(f"Insulin resistance pattern: {insulin_resistance['summary']}")
    print(f"Atherogenic dyslipidaemia pattern: {atherogenic_dyslipidaemia['summary']}")

# =========================
# OUTPUT
# =========================

results = calculate_expanded_labs(patient)
print_expanded_lab_report(patient, results)
