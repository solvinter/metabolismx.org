# MetabolismX – Model Definition (v0.1)

## Purpose
MetabolismX is a structured, deterministic framework for interpreting metabolic biomarkers.  
Its purpose is to organise routinely available data into physiologically meaningful patterns.

It is **not a diagnostic system**, but an **interpretation layer** to support clinical reasoning.

---

## Conceptual foundation
The model is based on a core principle:

> Glucose reflects achieved stability.  
> Insulin reflects the physiological cost required to maintain that stability.

MetabolismX integrates:

- glucose regulation  
- insulin dynamics  
- lipid transport (VLDL/remnant/HDL patterns)  
- adiposity  
- haemodynamic load  

into a system-level interpretation.

---

## Model structure

### 1. Direct measurements
Laboratory and clinical values (e.g. glucose, triglycerides, blood pressure).

### 2. Derived markers
Reorganised variables (e.g. non-HDL, remnant cholesterol, ratios).

### 3. Model-based estimates
Established indices (e.g. HOMA-IR, QUICKI, TyG).  
These are **indirect estimates**, not direct measurements.

### 4. Summary models (v0.1)
Rule-based synthesis outputs (e.g. metabolic burden score, pattern summaries).  
These are **heuristic and not externally validated**.

---

## Interpretation framework

Two parallel systems are used:

### Clinical reference ranges
- guideline-aligned thresholds  
- identify established risk or disease ranges  

### MetabolismX levels
- “optimal”, “early drift”, “metabolic signal”, “dysregulation”  
- capture gradual physiological change  

Key principle:

> Values within conventional reference ranges may still reflect increased metabolic load.

---

## Position in clinical context

MetabolismX does not:
- diagnose disease  
- replace clinical judgement  
- replace validated risk models  

MetabolismX aims to:
- support pattern recognition  
- highlight early compensatory states  
- contextualise biomarker relationships  

---

## Assumptions

The current model assumes:
- adult population  
- fasting-state measurements  
- general reference context  

No adjustment is currently made for:
- age  
- ethnicity  
- pregnancy  
- major comorbid conditions  

---

## Limitations

- Model-based indices are indirect estimates  
- Biological variability (e.g. insulin assays, HbA1c, triglycerides)  
- Summary models are heuristic (v0.1)  
- Risk of overinterpretation if used without clinical context  

---

## Transparency

All calculations are:
- deterministic  
- explicitly defined  
- reproducible  

No black-box components are used.

---

## Positioning statement

MetabolismX should be understood as:

> A transparent framework for metabolic pattern recognition  
> designed to support — not replace — clinical interpretation.
