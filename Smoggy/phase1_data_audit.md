# Smoggy Phase 1 — Data Discovery & Audit

## Purpose
Establish the definitive catalog of cohorts, assays, and metadata required for Phase 2 feature consolidation. This phase guarantees that every downstream artifact (features, models, validation) references vetted, well-documented datasets with reproducible provenance.

## Key Questions
1. Which cohorts and hospital partners provide prediagnostic blood draws that meet Phase 0 rules?
2. What assays (cfDNA methylation, fragmentomics, proteins, ctDNA) exist per cohort, and what preprocessing is required before feature extraction?
3. Which metadata fields are mandatory for leakage control (site, batch, collection date, patient-level covariates)?
4. What are the data-sharing restrictions, consent scopes, and retention policies per cohort?

## Deliverables
- **Inventory spreadsheet** (`data_docs/phase1_inventory.parquet` placeholder) capturing cohort name, sample counts, case/control prevalence, assay list, QC status, and legal notes.
- **Audit checklist** stored in `data_docs/phase1_audit_checklist.md` enumerating QC gates (missingness thresholds, contamination flags, timing leakage checks).
- **Access log** describing how each dataset was retrieved (S3 bucket, SFTP, drive) including checksum + timestamp for traceability.
- **Gap assessment** summarizing missing cohorts or metadata required before Phase 2.

## Workflow
1. **Ingest** raw manifests from partner hospitals; normalize column names (snake_case) and attach unique sample IDs.
2. **Validate** sample timelines against diagnosis dates to ensure prediagnostic status; flag violations for exclusion.
3. **QC** assay-specific metrics: library complexity, duplication rates, bisulfite conversion efficiency, fragment size distribution, protein panel CVs.
4. **Document** any remediation performed (e.g., batch correction planned later) inside `data_docs/phase1_audit_checklist.md`.
5. **Sign-off** once every retained cohort meets: matching controls, metadata completeness ≥95%, leakage risk mitigated, legal approvals recorded.

## Status (2026-03-16)
- ✅ Partner manifest templates defined; awaiting latest uploads from Niko & site ops.
- 🟡 Need final approval from IRB/ethics for the two European cohorts (ETA 03/20).
- 🟡 Missing smoking history fields for Hospital C controls — request sent 03/15.
- 🔴 No data yet for the planned longitudinal pilot; track as Phase 1 blocker.

## Exit Criteria
- Inventory, audit checklist, and access log checked into `data_docs/` with versioned filenames.
- Each retained cohort assigned a unique `cohort_id` and `data_snapshot` tag for reproducibility.
- Documented remediation plan for any partial metadata (e.g., imputation, exclusion) approved by clinical governance.
