# Smoggy Bayesian Model Blueprint

## Overview

This document captures the initial Phase 3 modeling plan for Smoggy. The goal is to design a transparent, reproducible Bayesian modeling family that can ingest prediagnostic cfDNA methylation/fragmentomic features (with room for additional blood biomarkers) and return calibrated cancer-risk posteriors.

Key requirements:

- Binary primary task: occult cancer signal present vs. absent.
- Optional secondary task: tissue-of-origin prediction when labels exist.
- Population: asymptomatic/high-risk screening cohorts with blood draws that precede formal diagnosis.
- Outputs: posterior probability with uncertainty intervals; never a definitive diagnosis.
- Inputs: blood-based features (cfDNA methylation, fragmentomics, ctDNA mutation burden, copy-number metrics, proteins) plus covariates (age, sex, smoking status, ancestry PCs, site indicators).
- Strict controls for batch/site leakage and reproducible inference code.

## Data Foundations and Priors

1. **Feature engineering**
   - Aggregate methylation loci or fragmentomic bins into biologically meaningful groups (genes, pathways, fragment size spectra, copy-number tiles).
   - Standardize and log-transform skewed biomarkers (protein panels, fragment count ratios).
   - Encode hospital/assay platform as categorical random effects.

2. **Priors**
   - Global intercept: weakly informative logistic prior (Normal(0, 2.5)).
   - Feature coefficients: hierarchical shrinkage (e.g., Horseshoe or Laplace) to encourage sparsity.
   - Group-level effects: Normal(0, σ_group) with half-Student-t prior on σ_group for site/platform/cancer-type hierarchies.
   - Covariate slopes: centered on literature estimates when available (e.g., smoking increases risk, so weak positive priors).
   - Latent-factor loadings (for multi-omics) with zero-mean Normal priors and LKJ prior for correlation matrices.

## Candidate Model Family

### Model 1 — Bayesian Hierarchical Logistic Baseline
- Likelihood: Bernoulli outcome (cancer signal yes/no) with logit link.
- Predictors: engineered cfDNA methylation + fragmentomic summaries + covariates.
- Hierarchical structure:
  - Intercepts by site/batch.
  - Slopes for major feature groups by assay platform if needed.
- Confounder adjustment for age, sex, smoking, ancestry, sample storage duration.
- Implementation options: Stan, NumPyro, or PyMC with automatic differentiation for HMC/NUTS.
- Purpose: interpretable baseline, calibrated posteriors, sanity check against classical methods.

### Model 2 — Bayesian Pathway-Informed Extension
- Build on Model 1 but map methylation/fragment features to pathway-level summaries (e.g., KEGG, Hallmark gene sets) or chromatin states.
- Use group lasso-style priors (e.g., hierarchical horseshoe) so pathways turn on/off as units.
- Encourages biological interpretability and stabilizes inference when thousands of loci exist.

### Model 3 — Bayesian Sparse Additive Model
- Captures nonlinear effects for select biomarkers (e.g., monotonic splines over fragment size ratios or methylation entropy).
- Priors: spike-and-slab or horseshoe on spline coefficients; monotonicity constraints where scientifically justified.
- Useful when handcrafted features show nonlinear risk patterns.

### Model 4 — Bayesian Latent Factor Multi-Omics Fusion
- Treat each modality (methylation blocks, fragmentomics, proteins) as loading on shared latent factors plus modality-specific noise.
- Combine latent factors in a hierarchical logistic head.
- Include site-specific random intercepts and allow factor loadings to vary by cohort.
- Good candidate once multimodal data is ready; keeps uncertainty propagation explicit.

### Non-Bayesian Reference Models (for benchmarking)
- Elastic Net logistic regression on the same feature matrix.
- Gradient-boosted trees (XGBoost/LightGBM) with blocked cross-validation.
- Random forest baseline.
- Lightweight neural net with dropout + calibration layer.
- Purpose: sanity check, highlight where Bayesian models add value (uncertainty, calibration, continual updating).

## Model Comparison Plan

1. **Shared dataset splits**
   - Follow Phase 5 rules: site-level held-out cohorts, temporal splits, and fully external validation when possible.
2. **Evaluation metrics**
   - AUROC, AUPRC, sensitivity at 95% specificity, calibration slope/intercept, PPV/NPV under screening prevalence.
3. **Posterior diagnostics**
   - R-hat, ESS, energy plots to ensure HMC convergence.
   - Posterior predictive checks vs. covariate distributions.
4. **Interpretability outputs**
   - Posterior coefficient intervals for top pathways/features.
   - Site-specific random effect summaries to monitor drift.

## Continual Updating Hooks

- Maintain a frozen reference posterior for each model.
- When new hospital data arrives, run QC, then update via:
  - Exact re-fit with new data appended.
  - Importance sampling / sequential Monte Carlo when feasible.
  - Hierarchical site-level updates (new random-effect draws) for fast adaptation.
- Log every update batch with data provenance, QC report, and before/after calibration metrics.

## Next Steps

1. Finalize feature dictionaries from Niko’s Phase 1 surveys.
2. Implement Model 1 in PyMC or NumPyro with reproducible scripts under `Smoggy/models/`.
3. Draft `model_blueprint.md` addendum with mathematical notation and pseudo-code once features are concrete.
4. Stand up baseline Elastic Net/XGBoost scripts for comparison.
