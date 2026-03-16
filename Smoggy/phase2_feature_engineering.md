# Smoggy Phase 2 — Feature Engineering & Data Products

## Objectives
Convert audited raw assays into standardized feature matrices ready for modeling. Harmonize cfDNA methylation, fragmentomics, ctDNA, and protein data into unified tables with consistent IDs, leakage-safe splits, and documented transformations.

## Pipelines
1. **Ingestion Layer (preprocessing/):**
   - `ingest_methylation.py`: converts per-locus beta values into gene/pathway aggregates; outputs parquet per cohort.
   - `ingest_fragmentomics.py`: computes fragment size histograms, nucleosome occupancy features, jaggedness scores.
   - `ingest_proteins.py`: normalizes multiplex protein intensities, log-transforms skewed markers, handles batch effects.
2. **Feature Assembly (feature_engineering/):**
   - `build_feature_matrix.py`: merges modality-specific tables on `sample_id`, fills missing modalities with sentinel values + modality indicators.
   - Adds covariates (age, sex, smoking_pack_years, ancestry PCs) from Phase 1 inventory.
   - Enforces leakage-safe train/validation split tags (site-stratified) and writes `features.parquet`.
3. **Quality Dashboard (notebooks/phase2_feature_qc.ipynb):** visualizes missingness, modality coverage, per-feature variance, and site/batch distributions.

## Data Contracts
- **Schema:** Documented in `data_docs/feature_schema.json` (to be finalized) with column data types, units, and acceptable ranges.
- **IDs:** Every row keyed by `sample_id`, `patient_id`, `cohort_id`, `site_id`, `draw_date`, `label`.
- **Versioning:** Each export tagged with `feature_snapshot=YYYYMMDD` and stored under `preprocessing/exports/{snapshot}/features.parquet`.

## Deliverables
- `feature_engineering/README.md` describing ingestion commands + configs.
- Canonical `features.parquet` (train/dev) + `features_holdout.parquet` (site + temporal holdout) with metadata sidecars.
- Missingness + modality coverage report in `reports/phase2_feature_qc.md`.

## Status (2026-03-16)
- 🟡 Methylation + fragmentomics ingestion scripts drafted locally (awaiting manifests for testing).
- 🟡 Feature schema skeleton prepared; final column list blocked on Niko’s Phase 1 inventory.
- 🔴 No consolidated `features.parquet` yet; dependent on hospital uploads.

## Exit Criteria
- Feature tables validated via QC notebook (variance > 0 for active features, <2% missingness after imputation strategy applied).
- All modality indicators + covariates present, with clear documentation of imputation or exclusion rules.
- Snapshot + git commit hash recorded in `reports/phase2_feature_qc.md`.
