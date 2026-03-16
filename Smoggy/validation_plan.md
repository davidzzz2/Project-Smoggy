# Smoggy Validation Plan

## 1. Objectives
- Quantify model discrimination, calibration, and clinical utility for the Smoggy screening workflow.
- Stress-test generalization across sites, time, and demographic/clinical subgroups.
- Provide clear decision-threshold guidance for downstream screening operations.

## 2. Datasets & Splits
- **Internal development cohort:** primary training + validation data.
- **Held-out site cohort:** distinct hospital system reserved for external-like validation.
- **Temporal holdout:** most recent quarter per site held out to measure time drift.
- **External cohort (stretch goal):** different platform or consortium data if access is approved.

Splitting rules:
1. Stratify by site and time to maintain prevalence balance.
2. Ensure patients do not appear in multiple splits.
3. Document inclusion/exclusion in `data_docs/`.

## 3. Evaluation Layers
1. **Internal cross-validation:** 5-fold, site-stratified; report fold-level stats + pooled estimates.
2. **Held-out site validation:** evaluate on untouched site(s), compare against internal performance.
3. **Temporal validation:** train on early periods, test on later timestamps per site.
4. **External validation:** repeat metrics on alternate cohort/platform (if available).
5. **Subgroup validation:** age bands, sex, cancer type/stage/site; include confidence intervals.
6. **Calibration analysis:** reliability diagrams + calibration slope/intercept, Brier score.
7. **Decision-threshold analysis:** sensitivity/specificity sweeps and operating points aligned with screening use cases.

## 4. Primary Metrics
- AUROC
- AUPRC
- Sensitivity @ fixed specificity (e.g., 95%)
- Specificity @ fixed sensitivity (e.g., 90%)
- Brier score
- Calibration slope / intercept
- PPV / NPV under realistic prevalence assumptions (document prevalence per cohort)

## 5. Secondary Metrics
- Uncertainty interval width (bootstrap 1,000 replicates)
- Hospital-wise heterogeneity (random-effects meta-analysis)
- Tissue-of-origin accuracy (if model outputs tissue labels)
- False-positive workup burden estimates (per 1,000 screened)

## 6. Calibration & Threshold Strategy
- Use isotonic or Platt scaling fitted on validation folds; evaluate on held-out sets only.
- Produce calibration plots per cohort and subgroup.
- Define at least two operating points: high-sensitivity (screening) and balanced.
- Translate PPV/NPV for baseline prevalence (document assumptions in `reports/`).

## 7. Reporting & Reproducibility
- Log every experiment configuration in `configs/` with seed, data snapshot, and git commit hash.
- Store raw metrics in `evaluation/metrics.csv` and summary tables in `reports/validation_summary.md`.
- Generate notebooks in `notebooks/` for visualization (calibration curves, subgroup plots).
- Capture command history + environment in `reports/reproducibility_log.md`.

## 8. Responsibilities & Timeline
- **Phase 5 (Validation):** finalize scripts in `evaluation/` and update `reports/` with results.
- **Phase 6 (Reproducibility package):** assemble full repo bundle (see requirements list) and archive versions of datasets/metadata references.

## 9. Acceptance Criteria
- All seven evaluation layers executed (or documented rationale if a layer is infeasible).
- Primary and secondary metrics reported with confidence intervals.
- Calibration + decision-threshold analyses included in final report.
- Reproducibility package contains code, configs, environment, seeds, and documentation per required directory layout.
