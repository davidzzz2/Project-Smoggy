# Smoggy — Data Eligibility Protocol (Phase 2)

Purpose
Define strict, reproducible criteria for selecting datasets/samples for prediagnostic cancer‑signal modeling, preventing leakage and minimizing confounding.

Inclusion Criteria (all required)
- Sample type: Peripheral blood plasma/serum cfDNA or blood‑derived biomarkers realistically available at/before screening time.
- Label clarity: Case/control definition unambiguous; case draw timing vs. diagnosis documented; controls cancer‑free at draw with follow‑up if available.
- Controls: Healthy/non‑cancer controls in comparable sampling frame.
- Timing: No post‑diagnosis, post‑treatment, or late workup samples in Stage‑1 training/evaluation.
- Reproducibility: Assay details/pipelines sufficient to reproduce features (or raw data available).
- Metadata: Age, sex, site/hospital, collection date, assay batch/plate; relevant risk factors.
- Volume: Sufficient N for temporal and external validation or clearly labeled exploratory.

Exclusion Criteria (any triggers exclusion)
- Tissue‑only biopsy omics as primary inference input for Stage‑1.
- Only advanced cancer cases without realistic controls or without timing metadata.
- Ambiguous labels or mixed/uncertain case/control status.
- Sampling timing that creates leakage (e.g., clearly after diagnostic pathway start).
- Massive batch/site confounding with no feasible correction.
- Unclear licensing/legal terms for research use.

Sample‑Level QC and Provenance
- Unique patient IDs; deduplicate repeated draws or model as longitudinal per protocol.
- Record pre‑analytics: tube type, time‑to‑plasma, storage temp, extraction kit, library prep, platform, read length/depth.
- Quantify batch/plate/center distributions across case/control; flag imbalances.
- Store raw data hashes and environment capture; version preprocessing configs.

Leakage Prevention and Splits
- Patient‑level disjoint splits; plate/center‑aware blocking.
- Temporal: train/val before T0; internal test strictly after T0.
- External: different site/platform; document domain shifts.

Confounding Control
- Minimum covariates: age, sex, center/site, assay/batch; add smoking/ancestry when available.
- Predefine adjustment: model covariates, stratified analyses, or hierarchical priors.

Feature Derivation Rules
- Features only from data available at/near draw time.
- cfDNA methylation: normalization, binning/DMR calling; lock genome build.
- Fragmentomics: size histograms, end‑motifs, nucleosome periodicity; fixed windowing and QC.
- CNV/aneuploidy: coverage bins, GC correction, segmentation parameters.
- Save fitted transformers and schemas; version every change.

Documentation and Audit
- For each dataset: DOI/link, license, cohort diagram, timing schema, completed eligibility checklist.
- Deviations require a written waiver and reviewer sign‑off.

Reviewer Workflow
- Dual review for include/exclude; disagreements resolved by third reviewer.
- Track decisions and reasons in evidence_matrix.csv with timestamps and reviewer IDs.
