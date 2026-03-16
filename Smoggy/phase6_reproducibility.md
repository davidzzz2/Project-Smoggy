# Smoggy Phase 6 — Reproducibility & Release Package

## Goal
Deliver a self-contained bundle that allows any approved reviewer to recreate the Smoggy modeling and validation results end-to-end. This package becomes the audit artifact for regulatory, clinical governance, and partner tech transfers.

## Package Contents
1. **Code Snapshot:**
   - Tagged git commit (e.g., `smoggy-release-0.1`) with submodules vendored if necessary.
   - `requirements.txt`/`environment.yml` + lockfiles.
2. **Data Manifests:**
   - Checksums + secure locations for feature tables, holdout sets, calibration cohorts (actual data stored in governed buckets, not the repo).
   - Redacted sample metadata templates for reviewers.
3. **Model Artifacts:**
   - Posterior traces (`*.nc`), calibration curves, decision threshold tables.
   - Serialized baseline models (Elastic Net/XGBoost) for comparison.
4. **Execution Scripts:**
   - `scripts/run_all.sh` (or `.ps1`) orchestrating Phase 2–5 steps.
   - `make reproduce` target running unit/integration tests.
5. **Documentation:**
   - `reports/final_summary.pdf` (exported from markdown or notebook).
   - `reports/reproducibility_log.md` capturing commands, seeds, compute resources.
6. **Governance Appendix:**
   - Approvals, ethical reviews, data-sharing agreements, risk assessments.

## Process
- Freeze data snapshots + model configs; register them in `reports/release_manifest.yaml`.
- Run clean-room reproduction on a separate machine/conda env; document discrepancies.
- Collect signatures from responsible parties (data, modeling, validation, clinical) before handing off to deployment/ops.

## Checklist
- [ ] `release_manifest.yaml` created with dataset + artifact hashes.
- [ ] Automated test suite (unit + smoke) green on clean clone.
- [ ] Security review completed (PII removal, secrets audit).
- [ ] Packaging script uploaded to secure bucket or artifact store.

## Status (2026-03-16)
- 🔴 No release artifacts yet — depends on Phase 5 completion.
- 🟡 Draft manifest template planned; will populate once training pipeline stabilizes.

## Exit Criteria
- Independent reviewer can follow documented steps to reproduce metrics within tolerance (e.g., AUROC ±0.01).
- All governance sign-offs recorded; package archived in long-term storage.
- Communication sent to stakeholders summarizing results + reproduction instructions.
