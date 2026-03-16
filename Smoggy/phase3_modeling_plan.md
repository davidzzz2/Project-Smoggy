# Smoggy Phase 3 — Modeling Strategy

## Scope
Translate the curated feature matrices into calibrated risk models with explicit uncertainty estimates. This phase covers baseline model definitions, priors, implementation details, and benchmarking strategy.

## Model Family
- **Bayesian Hierarchical Logistic Baseline (Model 1):**
  - Implemented in `Smoggy/models/hierarchical_logistic.py` (PyMC + Typer CLI).
  - Random intercepts per site/batch, hierarchical shrinkage on feature groups, optional covariate priors.
- **Pathway-Informed Extension (Model 2):**
  - Grouped features (KEGG/Hallmark pathways), hierarchical horseshoe prior to switch pathways on/off.
- **Sparse Additive Model (Model 3):**
  - Monotonic spline components for biomarkers with non-linear effects (fragment size ratios, methylation entropy).
- **Latent Factor Fusion (Model 4):**
  - Multi-omics latent factors feeding a hierarchical logistic head; supports modality-specific noise.
- **Reference Baselines:** Elastic Net, Gradient Boosted Trees, Random Forest, lightweight neural net for calibration comparison.

Full details live in `Smoggy/models/model_blueprint.md`, which also tracks implementation status.

## Training Workflow
1. Load Phase 2 `features.parquet` via CLI config (`models/configs/model1_example.yaml`).
2. Fit Model 1 with NUTS (NumPyro backend) → artifacts stored under `artifacts/model1/`.
3. Compare baselines using shared splits; metrics logged to `evaluation/metrics.csv`.
4. Document posterior diagnostics + interpretation in `reports/modeling_summary.md`.

## Dependencies
- PyMC, ArviZ, NumPy, pandas, Typer (captured in `Smoggy/configs/requirements.txt`).
- Future: JAX/NumPyro for latent factor models, XGBoost/LightGBM for baselines.

## Status (2026-03-16)
- ✅ CLI + config scaffolding merged (commit `ffd8d44`).
- 🟡 Feature schema integration pending Phase 2 export.
- 🟡 Baseline benchmarking scripts (Elastic Net/XGBoost) not yet added.
- 🔴 Latent factor fusion prototype not started; pending multimodal data.

## Exit Criteria
- Model 1 fit on Phase 2 snapshot with documented convergence (R-hat < 1.01, ESS > 400 for key parameters).
- Baseline comparisons complete with calibration reports.
- Decision log describing which model(s) advance to Phase 4 deployment.
