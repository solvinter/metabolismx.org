Create an evidence-linking layer between the MetabolismX calculation code and the existing website reference library.

Context:
The website already has a scientific reference library in:

data/references.yaml

It is rendered on the website by existing scripts, so any new YAML entries must follow the exact same structure already used in that file.

Goal:
Add a new section/category in the website reference library for the mathematical and rule-based models used in the MetabolismX metabolic analysis engine.

Suggested category name:
"Beräkningar – metabol belastning"

Use this category for references supporting formulas, indices, derived markers, and summary criteria.

Tasks:

1. Update data/references.yaml

Add missing references for the calculation models used in:

metabolic_modifier_system/python/src/metabolic_modifier_system/

Add entries using the existing YAML schema:

- id
- type
- title
- short
- summary
- authors
- journal
- year
- doi
- category
- abstract

Do not change the structure of existing references.

Add at least these references if not already present:

A. HOMA-IR
id: ref_homa_ir_matthews_1985
Title:
Homeostasis model assessment: insulin resistance and beta-cell function from fasting plasma glucose and insulin concentrations in man
Authors:
Matthews DR et al.
Journal:
Diabetologia
Year:
1985
DOI:
10.1007/BF00280883
Category:
Beräkningar – metabol belastning

B. QUICKI
id: ref_quicki_katz_2000
Title:
Quantitative insulin sensitivity check index: a simple, accurate method for assessing insulin sensitivity in humans
Authors:
Katz A et al.
Journal:
Journal of Clinical Endocrinology & Metabolism
Year:
2000
DOI:
10.1210/jcem.85.7.6661
Category:
Beräkningar – metabol belastning

C. TyG index
id: ref_tyg_simental_mendia_2008
Title:
The product of fasting glucose and triglycerides as surrogate for identifying insulin resistance in apparently healthy subjects
Authors:
Simental-Mendía LE et al.
Journal:
Metabolic Syndrome and Related Disorders
Year:
2008
DOI:
10.1089/met.2008.0034
Category:
Beräkningar – metabol belastning

D. TyG index validation
id: ref_tyg_guerrero_romero_2010
Title:
The product of triglycerides and glucose, a simple measure of insulin sensitivity. Comparison with the euglycemic-hyperinsulinemic clamp
Authors:
Guerrero-Romero F et al.
Journal:
Journal of Clinical Endocrinology & Metabolism
Year:
2010
DOI:
10.1210/jc.2010-0288
Category:
Beräkningar – metabol belastning

E. Metabolic syndrome harmonised criteria
id: ref_metabolic_syndrome_harmonized_2009
Title:
Harmonizing the metabolic syndrome: a joint interim statement
Authors:
Alberti KGMM et al.
Journal:
Circulation
Year:
2009
DOI:
10.1161/CIRCULATIONAHA.109.192644
Category:
Beräkningar – metabol belastning

F. Waist-to-height ratio
id: ref_waist_height_ashwell_2012
Title:
Waist-to-height ratio is a better screening tool than waist circumference and BMI for adult cardiometabolic risk factors
Authors:
Ashwell M et al.
Journal:
Obesity Reviews
Year:
2012
DOI:
10.1111/j.1467-789X.2011.00952.x
Category:
Beräkningar – metabol belastning

G. Remnant cholesterol
id: ref_remnant_varbo_2013
Title:
Remnant cholesterol as a causal risk factor for ischemic heart disease
Authors:
Varbo A et al.
Journal:
Journal of the American College of Cardiology
Year:
2013
DOI:
10.1016/j.jacc.2013.06.032
Category:
Beräkningar – metabol belastning

H. Non-HDL / dyslipidaemia guideline context
id: ref_esc_eas_dyslipidaemia_2019
Title:
2019 ESC/EAS Guidelines for the management of dyslipidaemias
Authors:
Mach F et al.
Journal:
European Heart Journal
Year:
2020
DOI:
10.1093/eurheartj/ehz455
Category:
Beräkningar – metabol belastning

I. Blood pressure guideline context
id: ref_esc_hypertension_2024
Title:
2024 ESC Guidelines for the management of elevated blood pressure and hypertension
Authors:
McEvoy JW et al.
Journal:
European Heart Journal
Year:
2024
DOI:
10.1093/eurheartj/ehae178
Category:
Beräkningar – metabol belastning

J. HbA1c / diagnostic classification context
id: ref_ada_standards_diagnosis_2024
Title:
2. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2024
Authors:
American Diabetes Association Professional Practice Committee
Journal:
Diabetes Care
Year:
2024
DOI:
10.2337/dc24-S002
Category:
Beräkningar – metabol belastning

K. C-peptide clinical utility
id: ref_c_peptide_jones_2013
Title:
The clinical utility of C-peptide measurement in the care of patients with diabetes
Authors:
Jones AG; Hattersley AT
Journal:
Diabetic Medicine
Year:
2013
DOI:
10.1111/dme.12159
Category:
Beräkningar – metabol belastning

L. TG/HDL and insulin resistance
id: ref_tg_hdl_mclaughlin_2003
Title:
Use of metabolic markers to identify overweight individuals who are insulin resistant
Authors:
McLaughlin T et al.
Journal:
Annals of Internal Medicine
Year:
2003
DOI:
10.7326/0003-4819-139-10-200311180-00007
Category:
Beräkningar – metabol belastning

If any DOI is uncertain, keep the DOI field empty rather than inventing one, and add a short note in the summary that the DOI should be verified.

2. Update metabolic_modifier_system/python/src/metabolic_modifier_system/reference_values.py

For each relevant marker dictionary, add an evidence_ids field pointing to the IDs in data/references.yaml.

Examples:

HOMA_IR:
"evidence_ids": ["ref_homa_ir_matthews_1985"]

QUICKI:
"evidence_ids": ["ref_quicki_katz_2000"]

TYG_INDEX:
"evidence_ids": [
  "ref_tyg_simental_mendia_2008",
  "ref_tyg_guerrero_romero_2010"
]

HBA1C:
"evidence_ids": ["ref_ada_standards_diagnosis_2024"]

C_PEPTIDE:
"evidence_ids": ["ref_c_peptide_jones_2013"]

TG_HDL_RATIO:
"evidence_ids": ["ref_tg_hdl_mclaughlin_2003"]

REMNANT_CHOLESTEROL:
"evidence_ids": ["ref_remnant_varbo_2013"]

NON_HDL_CHOLESTEROL and LDL_CHOLESTEROL:
"evidence_ids": ["ref_esc_eas_dyslipidaemia_2019"]

WAIST_HEIGHT_RATIO:
"evidence_ids": ["ref_waist_height_ashwell_2012"]

WAIST_CIRCUMFERENCE and metabolic syndrome related logic:
"evidence_ids": ["ref_metabolic_syndrome_harmonized_2009"]

BLOOD_PRESSURE, MEAN_ARTERIAL_PRESSURE, PULSE_PRESSURE:
"evidence_ids": ["ref_esc_hypertension_2024"]

3. Update metabolic_modifier_system/python/src/metabolic_modifier_system/summary_models.py

Where relevant, add evidence_ids to returned summary objects, especially:

calculate_metabolic_syndrome_components:
"evidence_ids": ["ref_metabolic_syndrome_harmonized_2009"]

calculate_metabolic_burden_score:
"evidence_ids": [
  "ref_metabolic_syndrome_harmonized_2009",
  "ref_homa_ir_matthews_1985",
  "ref_tyg_simental_mendia_2008",
  "ref_tg_hdl_mclaughlin_2003"
]

summarise_insulin_resistance_pattern:
"evidence_ids": [
  "ref_homa_ir_matthews_1985",
  "ref_quicki_katz_2000",
  "ref_tyg_simental_mendia_2008",
  "ref_tyg_guerrero_romero_2010"
]

summarise_atherogenic_dyslipidaemia:
"evidence_ids": [
  "ref_tg_hdl_mclaughlin_2003",
  "ref_esc_eas_dyslipidaemia_2019",
  "ref_remnant_varbo_2013"
]

4. Add a short note to metabolic_modifier_system/MetabolismX_Methods.md

Add a section:

## Evidence linkage

Explain:
- the implementation contains evidence_ids
- these IDs map to data/references.yaml
- the website can render the full references from that YAML file
- the code should not duplicate the full reference library

5. Validation

After changes:
- run Python syntax check
- run lab_exploration.py
- verify that every evidence_id used in Python exists in data/references.yaml
- do not modify unrelated files
