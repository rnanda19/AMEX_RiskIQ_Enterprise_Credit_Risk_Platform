# AMEX Enterprise Credit Risk Platform -- 360° Customer Intelligence

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 5, Problem 12 of the platform: a 4-notebook build (Notebooks 62-65) that composes Problems 1, 6, 9, and 10's real, already-validated signals into one unified per-customer risk profile, on the real Kaggle **American Express Default Prediction** dataset.

## Status: In Progress

Notebook 62 (Business Understanding & Policy) is shipped: it loads Problem 1's real champion model, Problem 6's real dynamic-PD deployment, Problem 9's real propensity-to-cure deployment, and Problem 10's real scored worklist, then defines `UNIFIED_RISK_SCORE = 0.35*STATIC_PD + 0.65*DYNAMIC_PD` (+ a real 0.10 collections adjustment where a real propensity-to-cure score exists), tertile-graded into Low/Medium/High Risk. Two new hard-gating KPIs: `profile_completeness` and `composite_non_inferiority` (the composite's real ROC-AUC must not fall below its best single real input signal's AUC).

Notebooks 63 (Modeling), 64 (Validation & Deployment), and 65 (Financial Impact, Reporting & Packaging) are not yet built. This README, `MODEL_CARD.md`, `CHANGELOG.md`, and this problem's real dashboard link will be filled in once the full 4-notebook build is run and synced -- no figures are stated here in the meantime.

## Project Structure

```
Problem12_360_Customer_Intelligence/
├── artifacts/
├── data/
├── docs/
├── models/
├── notebooks/
│   └── 62_customer_intelligence_business_understanding.ipynb
├── reports/
├── src/
│   └── docker/
├── tests/
└── LICENSE
```

## License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
