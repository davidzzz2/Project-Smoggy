# Smoggy — Problem Statement (Phase 0)

Objective
- Build a reproducible, research-grade Bayesian early cancer detection / prediagnosis system using biologically and clinically defensible prediagnostic data.

Target population
- Asymptomatic screening adults and/or defined high‑risk cohorts (to be fixed before training). Prevalence assumptions will follow the chosen cohort.

Sample type
- Peripheral blood, plasma‑derived cfDNA as the primary Stage‑1 analyte.

Prediction target
- Binary: cancer‑associated signal present vs absent at the time of blood draw.
- Optional secondary: tissue/site of origin (TOO) when uncertainty is acceptable.

Time horizon
- Current occult cancer / near‑term signal consistent with early disease; no post‑diagnosis or treatment‑derived features.

Output format
- Posterior probability with calibrated uncertainty interval; decision support phrasing ("cancer signal detected/not detected" with recommended follow‑up), not a diagnosis.

Exclusion rules (hard)
- Exclude post‑diagnosis, post‑treatment, or advanced workup samples from Stage‑1 training/eval.
- Exclude tissue‑only biopsy omics as primary inputs.
- Do not use germline‑only features to infer current cancer presence.
- Control for batches/plates/centers in splits to prevent leakage.

Primary Stage‑1 modalities
- cfDNA methylation signatures (genome‑wide patterns, DMRs)
- cfDNA fragmentomics (fragment size distributions, end motifs, nucleosome positioning)
- Optional: shallow‑WGS CNV/aneuploidy, ultra‑low‑VAF mutation burden; later optional protein panels if truly prediagnostic.

Validation stance
- Strict: internal CV, temporal holdout, external site validation, subgroup analyses (age/sex/cancer type/stage/site), calibration and thresholding with PPV under realistic prevalence.
