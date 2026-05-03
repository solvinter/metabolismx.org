"""Small smoke script to verify view functions return DataFrame."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import pandas as pd
from metabolic_modifier_system.laboratory_results_views.classic_lab_view import render_classic_lab_view
from metabolic_modifier_system.laboratory_results_views.metabolismx_lab_view import render_metabolismx_lab_view

# Minimal fake patient and results
patient = {
    "name": "Test Testsson",
    "sex": "male",
    "height_cm": 178.0,
    "weight_kg": 94.0,
    "waist_cm": 104.0,
    "systolic_bp": 138.0,
    "diastolic_bp": 86.0,
    "fasting_glucose": 5.8,
    "fasting_insulin": 14.0,
    "c_peptide": 0.95,
    "hba1c": 39.0,
    "total_cholesterol": 5.4,
    "ldl": 3.3,
    "hdl": 1.0,
    "triglycerides": 2.1,
}

results = {
    "bmi": 29.7,
    "waist_height_ratio": 0.58,
    "eAG": 6.2,
    "homa_ir": 2.25,
    "quicki": 0.33,
    "tyg_index": 8.5,
    "non_hdl": 4.4,
    "remnant": 0.8,
    "tg_hdl_ratio": 2.1,
    "total_hdl_ratio": 5.4,
    "ldl_hdl_ratio": 3.3,
    "pulse_pressure": 52,
    "map": 103.3,
}

levels = {}

summaries = {}


def run():
    df1 = render_classic_lab_view(patient, results, levels=levels, summaries=summaries)
    assert isinstance(df1, pd.DataFrame), "classic view did not return DataFrame"
    print("classic view OK, rows:", len(df1))

    df2 = render_metabolismx_lab_view(patient, results, levels=levels, summaries=summaries)
    assert isinstance(df2, pd.DataFrame), "metabolismx view did not return DataFrame"
    print("metabolismx view OK, rows:", len(df2))


if __name__ == '__main__':
    run()
