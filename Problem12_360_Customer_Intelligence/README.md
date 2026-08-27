# AMEX Enterprise Credit Risk Platform -- 360° Customer Intelligence

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 5, Problem 12 of the platform: a 4-notebook build (Notebooks 62-65) that composes Problems 1, 6, 9, and 10's real, already-validated signals into one unified per-customer risk profile, on the real Kaggle **American Express Default Prediction** dataset.

## Status: In Progress (3 of 4 notebooks shipped)

Notebook 62 (Business Understanding & Policy) is shipped: it loads Problem 1's real champion model, Problem 6's real dynamic-PD deployment, Problem 9's real propensity-to-cure deployment, and Problem 10's real scored worklist, then defines `UNIFIED_RISK_SCORE = 0.35*STATIC_PD + 0.65*DYNAMIC_PD` (+ a real 0.10 collections adjustment where a real propensity-to-cure score exists), tertile-graded into Low/Medium/High Risk. Two new hard-gating KPIs: `profile_completeness` and `composite_non_inferiority` (the composite's real ROC-AUC must not fall below its best single real input signal's AUC).

Notebook 63 (Modeling) is shipped: builds the real per-customer unified profile by joining Problem 10's already-scored worklist with a freshly-scored real per-customer propensity-to-cure signal (Problem 9's model, run once per collections-eligible customer's own real latest statement), computes `UNIFIED_RISK_SCORE`/`UNIFIED_RISK_GRADE`, and validates both hard-gating KPIs on the real holdout split.

Notebook 64 (Validation & Deployment) is shipped: independently reproduces Notebook 63's entire pipeline from scratch, cross-checks the persisted `unified_customer_profile.parquet` against a fresh reproduction sample, bootstraps a 95% CI on the `composite_non_inferiority` gap, and generates a real, auth-protected, self-tested FastAPI **lookup** service (`GET /profile/{customer_id}`) that serves the precomputed unified profile -- deliberately not a live-compute endpoint, since Problem 12's deliverable is a precomputed artifact, not a model to re-run per request.

Notebook 65 (Financial Impact, Reporting & Packaging) is not yet built. This README, `MODEL_CARD.md`, `CHANGELOG.md`, and this problem's real dashboard link will be filled in once the full 4-notebook build is run and synced -- no figures are stated here in the meantime.

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
│   └── 64_customer_intelligence_validation_deployment.ipynb
├── reports/
├── src/
│   └── docker/
├── tests/
└── LICENSE
```

## License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
