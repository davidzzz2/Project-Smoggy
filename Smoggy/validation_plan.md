# Smoggy — Validation Plan

1) Objective and Scope
- Evaluate generalization, calibration, and decision utility across time, sites, and patient subgroups using prediagnostic blood‑based signals.

2) Datasets and Cohorts
- Internal development set: <sites/cohorts>, time window <start–end>.
- Held‑out internal test set: temporally and patient‑disjoint.
- External validation set: different hospital/system/platform; harmonized labels and preprocessing.
- Inclusion/exclusion: per data_eligibility_protocol.md.

3) Splits and Leakage Controls
- Patient‑level disjoint splits; plate/center‑aware blocked CV.
- Temporal split: train/val before cutoff T0; internal test after T0.
- External validation: different site/platform; document domain shifts.

4) Evaluation Layers
1. Internal cross‑validation (e.g., 5‑fold patient‑level, blocked by center/plate when feasible)
2. Held‑out site validation (reserve ≥1 internal site if available)
3. Temporal validation (rolling backtests optional)
4. External validation (unseen cohort/platform)
5. Subgroup validation (age, sex, cancer type/stage/site)
6. Calibration analysis (reliability curves; slope/intercept; ECE; Brier)
7. Decision‑threshold analysis (sensitivity@fixed specificity; specificity@fixed sensitivity; PPV/NPV under realistic prevalence)

5) Metrics
Primary: AUROC, AUPRC, sensitivity@fixed specificity, specificity@fixed sensitivity, Brier score, calibration slope/intercept, PPV/NPV (prevalence‑aware).
Secondary: CI width, hospital‑wise heterogeneity (random‑effects; I²), tissue‑of‑origin accuracy (if modeled), false‑positive workup burden.

6) Statistical Methods
- CIs via patient‑level bootstrap (≥2,000 resamples); DeLong for AUROC/AUPRC where applicable.
- Thresholds set on validation, frozen before testing; report drift under prevalence shifts.
- Calibration: report pre/post isotonic/Platt; no fitting on test/external.
- Heterogeneity: random‑effects meta‑analysis across sites; pooled + site metrics.

7) Prevalence and Scenario Modeling
- Report cohort prevalence; simulate PPV/NPV across 0.1%–10% prevalence with fixed sensitivity/specificity.
- Provide confusion matrices per 1,000 screened at chosen thresholds.

8) Data Handling and Preprocessing
- Immutable raw snapshot; provenance (hashes, queries, dates).
- Deterministic preprocessing with versioned configs; save fitted transformers.
- Train/val/test manifests committed; patient ID hashing; missing data strategy defined.

9) Reproducibility and Logging
- Seeds, exact commands, environment.yml saved.
- Log dataset hashes, splits, hyperparams, calibrators/thresholds, metrics to artifacts/ with run IDs.

10) Reporting Artifacts
- Tables: primary + secondary metrics per split; subgroup and site panels; calibration coefficients.
- Figures: ROC/PR, reliability, decision curves, temporal drift.
- Notebooks: evaluation/*.ipynb parameterized via papermill.
- Model card and dataset provenance in reports/.

11) Acceptance Criteria (to be finalized)
- External AUROC ≥ <X>, AUPRC ≥ <Y> vs. baseline; calibration slope ∈ [0.8,1.2], intercept ∈ [-0.1,0.1]; Brier ≤ <Z>.
- Sensitivity at 95% specificity ≥ <S>; PPV ≥ <P> at target prevalence.
- No subgroup underperformance beyond Δ vs. overall without mitigation plan.

12) Governance and Freezing
- Freeze code/configs pre‑external eval; tag release; independent rerun on clean env; archive artifacts.

13) Timeline and Ownership
- Fill owners/dates for CV, internal test, external, and final report.
