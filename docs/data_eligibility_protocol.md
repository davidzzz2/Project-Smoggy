# Smoggy — Data Eligibility Protocol (Phase 2 Draft)

## Inclusion (all required)
- Sample type is realistically available at or before screening (e.g., blood/plasma/serum for cfDNA)
- Clear, reproducible label definition (case/control) without timing leakage
- Healthy or non‑cancer controls available and defined
- Collection timing is not post‑treatment or post‑diagnosis unless explicitly flagged for a different experiment
- Preprocessing is reproducible or can be standardized
- Clinical covariates (age/sex/smoking/ancestry/site/batch) available for confounding control, where feasible

## Prioritization
- cfDNA methylation
- cfDNA fragmentomics
- ctDNA mutation burden/patterns
- Copy‑number / chromosomal instability from blood
- Optional plasma protein markers for multimodal extension

## Use cautiously (later or exploratory)
- RNA panels, exosome markers, miRNA panels
- Germline PRS only as an auxiliary prior, not direct evidence of current cancer

## Exclusion
- Tissue-only tumor biopsy omics as primary inference input
- Post‑diagnosis or post‑treatment collections (unless explicitly separate experiments)
- Datasets without clear case/control timing or with high leakage risk
- Tiny datasets with no external validation value
- Massive site/plate/batch confounding without a credible correction path

## Documentation requirements
- Dataset provenance (study, accession, license, contact)
- Cohort: cancer types, stage distribution, demographics
- Sample handling: site, plate, batch, assay platform
- Label timing relative to diagnosis/treatment
- Preprocessing pipeline, version, seeds
- Inclusion/exclusion decision + rationale

## QC gates (before model ingestion)
- Missingness thresholds and imputation strategy
- Batch/site distribution checks; plan for hierarchical adjustment and/or harmonization
- Outlier detection and handling policy
- Leakage audit (features, labels, timestamps)
