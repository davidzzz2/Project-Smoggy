# Phase 4 — Modeling Strategy

Purpose: Choose model families, training regimes, and validation strategies.

- Objectives
  - Define target(s); cost-sensitive metrics
- Model Families
  - Baselines (logistic/GBM), candidates (Bayesian models per Smoggy goals)
- Validation
  - Nested CV or CV + locked holdout; site/time group splits
- Hyperparameter Tuning
  - Search space, early stopping, seeds
- Reproducibility
  - Determinism, tracking (seeds, env, data hashes)
