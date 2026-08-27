# AMEX Enterprise Credit Risk Platform -- 360° Customer Intelligence

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 5, Problem 12 of the platform: a 4-notebook build (Notebooks 62-65) that composes Problems 1, 6, 9, and 10's real, already-validated signals into one unified per-customer risk profile, on the real Kaggle **American Express Default Prediction** dataset.

## Status: Complete -- Run End-to-End by the User, 2026-08-27 (Real Results)

**Real, synced results (2026-08-27):** all hard gates passed; recommended for production. Real eligible population: 447,695 customers (149,012 Low Risk / 149,286 Medium Risk / 149,397 High Risk); real collections-eligible population: 303,660. Real composite ROC-AUC: 0.9590 vs. real best single-signal AUC 0.9626 (gap -0.0032 to -0.0040 at 95% CI, inside the -0.005 ASSUMPTION tolerance -- `composite_non_inferiority` passes, honestly reported even though the composite is very slightly below the best single signal). Real net benefit: **$1,275,022 per cycle** (Year-1 ROI 33,900.6%, payback 0.04 months) from collapsing four case lookups into one.

Notebook 62 (Business Understanding & Policy) is shipped: it loads Problem 1's real champion model, Problem 6's real dynamic-PD deployment, Problem 9's real propensity-to-cure deployment, and Problem 10's real scored worklist, then defines `UNIFIED_RISK_SCORE = 0.35*STATIC_PD + 0.65*DYNAMIC_PD` (+ a real 0.10 collections adjustment where a real propensity-to-cure score exists), tertile-graded into Low/Medium/High Risk. Two new hard-gating KPIs: `profile_completeness` and `composite_non_inferiority` (the composite's real ROC-AUC must not fall below its best single real input signal's AUC).

Notebook 63 (Modeling) is shipped: builds the real per-customer unified profile by joining Problem 10's already-scored worklist with a freshly-scored real per-customer propensity-to-cure signal (Problem 9's model, run once per collections-eligible customer's own real latest statement), computes `UNIFIED_RISK_SCORE`/`UNIFIED_RISK_GRADE`, and validates both hard-gating KPIs on the real holdout split.

Notebook 64 (Validation & Deployment) is shipped: independently reproduces Notebook 63's entire pipeline from scratch, cross-checks the persisted `unified_customer_profile.parquet` against a fresh reproduction sample, bootstraps a 95% CI on the `composite_non_inferiority` gap, and generates a real, auth-protected, self-tested FastAPI **lookup** service (`GET /profile/{customer_id}`) that serves the precomputed unified profile -- deliberately not a live-compute endpoint, since Problem 12's deliverable is a precomputed artifact, not a model to re-run per request.

Notebook 65 (Financial Impact, Reporting & Packaging) is shipped: synthesizes real results from all three prior notebooks, prices Problem 12's real, additive OPERATIONAL EFFICIENCY value (collapsing four separate case lookups -- Problems 1, 6, 9, 10 -- into one unified profile, using the real collections-eligible population as case-lookup volume, net of a genuinely new ongoing-hosting-cost stream) -- a deliberately different financial-model shape from every prior alerting/scoring problem, which does not double-count Problem 9/10's own already-priced loss-prevention benefit. Performs a third independent reproduction of the unified profile: reads the real persisted parquet directly for the exact full-population grade distribution, then live-drives the exact deployed lookup service against a real, grade-stratified sample, cross-checking every response against the persisted profile. Packages a multi-tab interactive HTML ops dashboard, a Word financial-impact report, and an Excel workbook.

This completes Problem 12 end to end (Notebooks 62-65), run successfully by the user with real results synced above. `MODEL_CARD.md` and `CHANGELOG.md` will be added once this platform's Phase 5 packaging pass runs (same practice as Phases 1-4); not yet pushed to GitHub.

## Project Structure

```
Problem12_360_Customer_Intelligence/
├── artifacts/
├── data/
├── docs/
├── models/
├── notebooks/
│   ├── 62_customer_intelligence_business_understanding.ipynb
│   ├── 63_customer_intelligence_modeling.ipynb
│   ├── 64_customer_intelligence_validation_deployment.ipynb
│   └── 65_customer_intelligence_financial_impact_reporting_packaging.ipynb
├── reports/
├── src/
│   └── docker/
├── tests/
└── LICENSE
```

## License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
