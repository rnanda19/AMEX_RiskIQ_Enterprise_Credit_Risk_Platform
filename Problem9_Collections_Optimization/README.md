# AMEX Enterprise Credit Risk Platform -- Collections Optimization

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 4, Problem 9 of the platform: a 4-notebook build (Notebooks 50-53) covering collections-strategy optimization on the real Kaggle **American Express Default Prediction** dataset.

## Status: Complete -- Real Results Synced, Hardened (2026-08-27)

**Real, synced results:** a real, trained XGBoost propensity-to-cure classifier -- real holdout ROC-AUC **0.8236** (reproduced, bit-identical), meeting the KPI target (>= 0.60). **Recommended for production.** Real net benefit: **$341,908,210 per cycle** -- the platform's single largest value-creation figure (see the [Executive Capstone Report](../Executive_Capstone_Report/) and root `README.md`'s Platform-at-a-Glance table).

📊 [Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem9_Collections_Optimization/reports/financial_impact_reporting_packaging/collections_optimization_financial_impact_dashboard.html) · 📄 [Financial Impact Report (Word)](reports/financial_impact_reporting_packaging/Collections_Optimization_Financial_Impact_Report.docx) · 📊 [Financial Impact Workbook (Excel)](reports/financial_impact_reporting_packaging/AMEX_Problem9_Financial_Impact_Workbook.xlsx)

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

This problem also received the platform's Global Standard hardening delta (2026-08-27): a real, auth-protected FastAPI scoring service (`src/collections_scoring_service.py`), Docker packaging, real unit tests, and `MODEL_CARD.md`/`CHANGELOG.md`/`requirements.txt` -- see `CHANGELOG.md` for the full detail, including a real hardcoded-path bug found and fixed.

## Project Structure

```
Problem9_Collections_Optimization/
├── data/
│   └── README.md
├── docs/
│   ├── collections_deployment_policy.json
│   └── collections_policy.json
├── models/
│   └── collections_propensity_xgboost.joblib
├── notebooks/
│   ├── 50_collections_optimization_business_understanding.ipynb
│   ├── 51_collections_optimization_modeling.ipynb
│   ├── 52_collections_optimization_validation_deployment.ipynb
│   └── 53_collections_optimization_financial_impact_reporting_packaging.ipynb
├── reports/
│   ├── modeling/
│   └── financial_impact_reporting_packaging/
├── src/
│   ├── collections_scoring_service.py
│   └── docker/
├── tests/
├── MODEL_CARD.md
├── CHANGELOG.md
├── requirements.txt
└── LICENSE
```

## License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
