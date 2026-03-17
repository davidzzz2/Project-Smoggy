# Canonical Schema v0 (Working Draft)

Goal: minimal, leakage-safe schema spanning expected sources. Version and extend as needed.

Core tables
- patients
  - patient_id (anon), sex, birth_year, site_id
- encounters
  - patient_id, encounter_id, start_date, end_date, setting (in/out/ED), site_id
- observations
  - patient_id, encounter_id?, date, code_system, code, value_num, value_text, unit, ref_range_low, ref_range_high
- vitals
  - patient_id, date, systolic, diastolic, hr, temp, weight, height, bmi
- medications
  - patient_id, start_date, end_date, atc|rxnorm_code, dose, route
- diagnoses
  - patient_id, date, icd_code, description
- outcomes (labels)
  - patient_id, index_date (diagnosis date), cancer_type, label_window (pre-dx window definition)

Conventions
- Dates truncated to day; no post-index information in features
- Units normalized to SI where applicable
- All tables carry site_id for shift analysis

Quality gates (v0)
- Demographics present (sex, birth_year)
- Date validity (no future dates; within study window)
- Unit checks and plausible ranges for common labs/vitals

Open questions
- Exact prediagnosis window (e.g., 6/12/24 months)
- Code system coverage (LOINC/SNOMED/ICD versions)
