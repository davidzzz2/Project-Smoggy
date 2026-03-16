# Smoggy Phase 5 — Validation Plan

This document distills the validation strategy originally drafted in `Smoggy/validation_plan.md` and ties it explicitly to Phase 5 deliverables.

## Objectives
- Quantify discrimination, calibration, subgroup fairness, and clinical utility of Smoggy’s screening model(s).
- Stress-test generalization across hospitals, assay batches, and temporal cohorts.
- Produce decision-threshold guidance aligned with screening operations.

## Dataset Strategy
1. **Internal development cohort:** primary training + cross-validation folds.
2. **Held-out site cohort:** entire hospital system kept untouched until final evaluation.
3. **Temporal holdout:** latest quarter per site excluded from training to measure drift.
4. **External platform cohort (stretch goal):** alternate assay or consortium data pending approvals.

Splitting rules:
- Stratify by site/time; enforce patient-level exclusivity between splits.
- Document inclusion/exclusion decisions in `data_docs/` with reproducible filters.

## Evaluation Layers
1. Site-stratified 5-fold CV.
2. Held-out site evaluation.
3. Temporal drift assessment.
4. External cohort validation (if available).
5. Subgroup analyses (age, sex, cancer type/stage, ancestry bins).
6. Calibration: reliability diagrams, slope/intercept, Brier score.
7. Decision-threshold sweeps: sensitivity @ 95% specificity, specificity @ 90% sensitivity, PPV/NPV under screening prevalence.

## Metrics
- **Primary:** AUROC, AUPRC, Sens@95%Spec, Spec@90%Sens, Brier score, calibration slope/intercept, PPV/NPV.
- **Secondary:** uncertainty interval width (bootstrap), hospital heterogeneity estimates, tissue-of-origin accuracy (if available), downstream workup burden per 1,000 screens.

## Reporting Artifacts
- `evaluation/metrics.csv`: all folds + cohorts with confidence intervals.
- `reports/validation_summary.md`: narrative + tables, calibration plots, subgroup figures.
- `reports/decision_thresholds.yaml`: recommended operating points + rationale.
- `notebooks/validation/*.ipynb`: visualization code; export plots into `reports/figures/`.
- `reports/reproducibility_log.md`: command history, seeds, environment, git hash.

## Governance
- Validation owner: TBD (assign before Phase 5 starts).
- Sign-off required from clinical governance + data governance boards.
- Every exception (e.g., missing external cohort) documented with mitigation plan.

## Status (2026-03-16)
- ✅ Draft plan captured (this file + `validation_plan.md`).
- 🔴 Metrics scripts (`evaluation/`) not started.
- 🔴 Subgroup definitions awaiting Phase 1 inventory.
- 🔴 Visualization notebooks pending baseline model outputs.

## Exit Criteria
- All evaluation layers executed or formally waived with justification.
- Metrics + plots committed, linked to immutable data/model snapshots.
- Decision-threshold memo approved by screening operations.
