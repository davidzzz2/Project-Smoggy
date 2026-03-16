# Smoggy Phase 0 — Problem Statement

## Target Population
- **Primary cohort:** Asymptomatic adults aged 45–80 presenting for annual wellness or high-risk surveillance visits.
- **Risk enrichment:** Includes individuals with elevated baseline risk (e.g., smoking history, family history, known genetic predisposition) but **excludes** those with a current cancer diagnosis or ongoing treatment.
- **Care setting:** Outpatient preventive clinics and partner hospital screening programs.

## Sample Type
- **Matrix:** Peripheral blood, processed for plasma-derived cfDNA and serum/plasma protein markers.
- **Assays (Stage 1 focus):** cfDNA methylation profiles, fragmentomics (size/position histograms, nucleosome footprinting), shallow WGS-derived copy-number/aneuploidy scores.
- **Optional adjuncts:** Targeted ctDNA mutation burden and selected plasma proteins for multimodal experiments after baseline model is stable.

## Prediction Target
- **Primary task:** Binary detection of an occult/incipient cancer signal ("cancer signal present" vs. "absent") corresponding to current or near-term (≤12 months) clinical confirmation.
- **Secondary (optional) task:** Tissue-of-origin probability vector for positive signals, constrained to major cancer groupings once sufficient labeled data exist.
- **Output:** Posterior probability of cancer signal with calibrated uncertainty interval; model communicates risk tier (e.g., low / indeterminate / elevated) plus a recommendation for confirmatory diagnostics.

## Exclusion Rules
1. **Timing leakage:** Remove samples collected after diagnostic confirmation, treatment initiation, or during surveillance of known cancer unless explicitly labeled for a separate experiment.
2. **Sample modality:** Exclude tissue-only biopsy omics and germline-only assays as primary features for this task.
3. **Label ambiguity:** Drop datasets lacking precise case/control definitions, sample acquisition date, or clinical context needed to ensure prediagnostic status.
4. **Confounding:** Exclude cohorts with irreparable batch/site leakage (e.g., all cases from one lab and controls from another) unless metadata allow hierarchical adjustment.
5. **Insufficient controls:** Require adequately matched non-cancer controls; discard datasets without them.

## Clinical-use Disclaimer
Smoggy estimates the probability of a detectable cancer-associated signal in blood for screening-like populations. It **does not provide a definitive diagnosis** and must not be used to initiate treatment without standard-of-care confirmatory diagnostics. Outputs are decision-support risk assessments intended to prompt follow-up imaging, repeat testing, or specialist referral according to institutional protocols. Model updates are logged, versioned, and validated before deployment; performance, calibration, and uncertainty must be reviewed by clinical governance teams prior to any patient-facing use.
