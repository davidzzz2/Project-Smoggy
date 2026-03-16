# Smoggy Phase 4 — Training, Serving, and MLOps Integration

## Objective
Operationalize the chosen models with automated training pipelines, artifact tracking, and reproducible inference endpoints suitable for sandbox deployment.

## Components
1. **Training Orchestrator (`training/pipeline.py` placeholder):**
   - Accepts config bundle (data snapshot, model config, seed, output path).
   - Runs feature checks, model fit, evaluation hooks, and artifact uploads sequentially.
   - Emits MLFlow/Weights & Biases-style metadata, even if stored locally for now.
2. **Artifact Registry (`training/artifacts/manifest.json`):**
   - Records posterior trace path, calibration curves, threshold tables, and git commit hash.
3. **Inference Package (`inference/`):**
   - `predict.py`: loads posterior NetCDF + feature row, outputs calibrated probability + interval.
   - `schema.py`: enforces required columns, ranges, and modality indicators for runtime validation.
4. **Automation Hooks:**
   - GitHub Action or cron to retrain weekly/monthly when new cohorts approved.
   - Notification channel (Team Falcon + email) when new model artifacts pass QC.

## Deployment Targets
- **Internal notebook scoring:** default path using `hierarchical_logistic.py predict`.
- **Batch scoring job:** plan to containerize inference (`Dockerfile` referencing `environment.yml`).
- **Future API:** restful endpoint (FastAPI) to serve predictions once data governance approves.

## Checklists
- [ ] `training/README.md` describing CLI usage + environment setup.
- [ ] `inference/tests/` with smoke tests for schema validation and posterior loading.
- [ ] Resource estimates (GPU/CPU hours) logged for capacity planning.

## Status (2026-03-16)
- 🟡 Training orchestrator skeleton drafted (not yet committed).
- 🔴 No artifact registry or automated reporting in repo.
- 🔴 Inference schema + tests to be created after Phase 3 baseline solidifies.

## Exit Criteria
- One-touch training command produces: posterior trace, metrics, calibration curves, decision thresholds, and report markdown.
- Inference package validated on holdout set and packaged for deployment (conda env + container spec).
- Monitoring plan drafted (inputs drift, calibration drift) ready for Phase 5 validation feedback.
