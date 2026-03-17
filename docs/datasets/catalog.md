# Dataset Catalog (Working)

Purpose: enumerate internal/public datasets suitable for early cancer prediagnosis research, with eligibility, access, and notes.

Template fields per dataset
- Name:
- Type: internal | public | synthetic
- Scope: demographics | labs | vitals | claims | notes | imaging-meta | genetics | other
- Time horizon: prediagnostic window available? how long?
- Size (N):
- Access: owner/contact or URL
- License/IRB/DUA:
- Eligibility fit: aligns with data_eligibility_protocol.md (Y/N + notes)
- Known biases/leakage risks:
- Status: proposed | requested | in hand | profiled

Candidate sources (to vet)
- Internal EHR extracts (owner TBD)
- Insurance claims datasets with longitudinal coverage
- National health surveys with lab panels
- Registry-linked cohorts with prediagnosis labs/vitals
- Synthetic or de-identified cohorts for method development

Worklog
- 2026-03-16: created catalog structure; awaiting confirmed sources
