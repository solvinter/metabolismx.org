# Python-lager

Den här mappen är platsen för den transparenta beräkningskoden.

Målet är att alla grundberäkningar ska kunna förstås, testas och granskas utan AI. AI-lagret ska bara tolka ett strukturerat resultat från Python/API-lagret.

## Föreslagen struktur

```text
python/
  README.md
  pyproject.toml                  # läggs till när paketet formaliseras
  src/
    metabolic_modifier_system/
      calculations.py             # HOMA-IR, QUICKI, TyG, lipidkvoter, BMI, midja/längd
      classifiers.py              # prediabetes, blodtryck, metabola syndromet, delprofiler
      score2_adapter.py           # adapter mot SCORE2/SCORE2-OP eller extern riskmotor
      scenarios.py                # mediator-baserad scenario-modellering
      schemas.py                  # input/output-modeller
      report_payload.py           # strukturerat underlag för 397-rapport
  tests/
    test_calculations.py
    test_classifiers.py
    test_scenarios.py
```

## Kodprinciper

- rena funktioner före globala tillstånd
- explicit enhetshantering
- inga AI-tolkningar i beräkningslagret
- trösklar i konfigurerbara tabeller
- varje beräkning ska returnera både värde och metadata
- saknade data ska ge `None` plus datakvalitetsflagga, inte tysta fel
- tester ska täcka formler, enhetskonvertering och gränsvärden

## Första beräkningsfunktioner

Prioriterad ordning:

1. `homa_ir(fasting_insulin, fasting_glucose_mmol_l)`
2. `quicki(fasting_insulin, fasting_glucose, glucose_unit)`
3. `tyg(triglycerides, fasting_glucose, units)`
4. `tg_hdl_ratio(triglycerides_mmol_l, hdl_mmol_l)`
5. `non_hdl(total_cholesterol_mmol_l, hdl_mmol_l)`
6. `remnant_cholesterol(total_cholesterol_mmol_l, ldl_mmol_l, hdl_mmol_l)`
7. `total_hdl_ratio(total_cholesterol_mmol_l, hdl_mmol_l)`
8. `ldl_hdl_ratio(ldl_mmol_l, hdl_mmol_l)`
9. `waist_height_ratio(waist_cm, height_cm)`
10. `bmi(weight_kg, height_cm)`

## Första klassificeringar

- diabetes-/prediabetes-screening från fasteglukos
- blodtrycksklassificering
- metabola syndromet enligt konfigurerad definition
- glukos-insulinprofil
- aterogen lipidprofil
- visceral adipositetsprofil
- klinisk riskprofil

## API-output

Beräkningslagret bör i slutändan leverera ungefär:

```json
{
  "calculated": {
    "homa_ir": {"value": 2.8, "unit": "index", "status": "elevated"},
    "quicki": {"value": 0.33, "unit": "index", "status": "low"},
    "non_hdl": {"value": 4.1, "unit": "mmol/L", "status": "elevated"}
  },
  "profiles": {
    "glucose_insulin": "metabolic_risk",
    "atherogenic_lipids": "high_metabolic_risk",
    "visceral_adiposity": "metabolic_risk",
    "clinical": "moderate_cvd_risk"
  },
  "missing_data": ["c_peptide", "apob"],
  "report_payload": {
    "summary_level": "metabolic_risk",
    "ai_allowed_outputs": [
      "prediabetes_diabetes_risk",
      "insulin_resistance_profile",
      "metabolic_syndrome",
      "atherogenic_dyslipidemia",
      "blood_pressure_risk",
      "score2_10_year_cvd_risk"
    ]
  }
}
```

## AI-kontrakt

AI får:

- formulera rapporttext
- förklara vad profilerna betyder
- föreslå vilka data som saknas
- sammanfatta scenario-modellering

AI får inte:

- skapa egna formler
- ersätta SCORE2/PREVENT
- ange diagnos när underlaget bara stödjer screeningflagga
- dölja osäkerhet eller saknade värden
