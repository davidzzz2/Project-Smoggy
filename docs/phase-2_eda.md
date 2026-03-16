# Phase 2 — Exploratory Data Analysis (EDA)

Purpose: Understand distributions, missingness, leakage risks, cohort balance, and initial signal.

- Cohort Overview
  - N, class balance, stratification variables (age/sex/site)
- Data Profiling
  - Missingness maps, ranges, outliers, drift by site/time
- Leakage Audit
  - Post-diagnostic artifacts, proxy features, temporal cutoffs
- Initial Signal Checks
  - Univariate associations, simple baselines
- Visuals
  - Histograms, KDEs, pairplots (safe subsets), SHAP on baseline
- Findings & Decisions
  - Issues to fix before FE/modeling
