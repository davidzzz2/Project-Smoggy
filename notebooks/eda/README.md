# EDA Notebook Plan

Notebooks to produce (Python):
1. 00_cohort_definition.ipynb — apply eligibility protocol; export cohort CSV(s)
2. 01_profile_missingness.ipynb — missingness maps and summaries
3. 02_shift_and_leakage_audit.ipynb — site/time shifts; post-dx artifact checks
4. 03_baseline_signal.ipynb — simple models (logistic/GBM) + calibration

Each notebook will:
- Read from canonical schema v0 tables or adapters
- Save figures to reports/ and intermediate artifacts to data_docs/
- Log seeds, env, and data hashes
