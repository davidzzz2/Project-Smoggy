# Smoggy — Problem Statement (Phase 0 confirmation)

Target population:
- Primary: asymptomatic screening or high‑risk screening population (to be finalized by data availability)

Sample type:
- Blood (plasma/serum) first; cfDNA-derived signals prioritized

Prediction target:
- Binary: cancer signal present vs absent

Optional secondary:
- Tissue of origin (if evidence supports and data permit)

Time horizon:
- Current occult cancer / near‑term cancer signal

Output:
- Posterior probability (risk score) with uncertainty interval

Exclusion rules:
- No post‑diagnosis or post‑treatment features
- No tissue‑only tumor biopsy omics as primary inference input
- No label leakage from case/control timing, treatment status, or late-stage workup

Clinical‑use disclaimer:
- Outputs are decision support (risk signal), not diagnosis; recommend confirmatory follow‑up for positives

Reproducibility:
- All experiments must include code, env files, seeds, and dataset provenance

Validation:
- Strict: site/plate/batch/patient non‑leakage, held‑out site validation, temporal/external validation where possible
