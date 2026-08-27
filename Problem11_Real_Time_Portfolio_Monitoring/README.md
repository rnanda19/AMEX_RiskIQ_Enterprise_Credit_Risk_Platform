# AMEX Enterprise Credit Risk Platform -- Real-Time Portfolio Monitoring

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 4, Problem 11 of the platform: a **4-notebook** build (Notebooks 58-61) that streams monthly credit-bureau/statement aggregates into a real statistical-process-control monitor -- a whole-portfolio control chart, not a per-customer classifier -- and alerts when a calendar month's cross-sectional mean breaches its own real trailing baseline. Built end-to-end on the real Kaggle **American Express Default Prediction** dataset.

## 1. Overview

- **Technique:** unsupervised statistical process control (trailing-baseline control chart), not a trained model
- **Control limit:** 2.5-sigma (`control_limit_k_sigma`), 6-month minimum trailing baseline
- **Monitored columns (real SHAP-ranked, Notebook 06):** `P_2`, `B_1`, `B_11`, `D_39`, `B_4`, `S_3`, `R_1`, `B_5`
- **Winning candidate:** 1 consecutive breaching month, customer-joint-deviation threshold |z| >= 2.0 (same direction as the portfolio breach)
- **Recommended for production (measured):** True

## 2. Problem Statement

A per-customer classifier answers "is this customer at risk?". This problem answers a different, complementary question: "is the whole portfolio's behavior shifting?" -- surfacing calendar months where the cross-sectional average of key risk features moves beyond its own real trailing history, so a risk committee can investigate a cohort-level cause rather than waiting for it to show up one customer at a time.

## 3. Approach & Methodology

Notebook 58 (Business Understanding & Policy) -> Notebook 59 (Modeling -- builds the real monthly portfolio store, the trailing-baseline control chart, and the customer-level joint-deviation cohort score) -> Notebook 60 (Independent Validation & Deployment -- bootstrap CIs, statistical validation table, a real FastAPI alert-feed service, self-tested) -> Notebook 61 (Financial Impact, Reporting & Packaging -- Word/Excel/HTML deliverables, including the ops dashboard).

**Design note (real rework, 2026-08-27):** the first two real runs of this problem's customer-level cohort scoring collapsed to a degenerate 100%/0% split (ROC-AUC exactly 0.5) because presence-based customer flagging ("was this customer active in a flagged month?") carries zero information when over 75% of customers share an identical full-history coverage window. The fix was a genuinely new design: a customer only counts toward the cohort score if their *own* statement value is itself >=2.0 standard deviations from that month's real cross-sectional peer mean, in the *same direction* as the portfolio's own breach ("joint deviation" -- population breach + individual cross-sectional deviation). This restores real per-customer discrimination even within the fully-covered majority, since their month-presence is identical but their own raw values are not. See `CHANGELOG.md`.

## 4. Key Results (Real, Measured)

- **Baseline-eligible months:** 26 of 32 calendar months covered (13 labeled)
- **Alert months (winning candidate):** 12 of 26 baseline-eligible months (46.2%)
- **Cohort size in the winning candidate's alert months:** 12,971 accounts (14.1% of the 91,783-customer holdout)
- **Default rate, alerted cohort vs. base population:** 69.2% vs. 25.9% -- **2.67x lift** (95% CI [2.64, 2.70])
- **Full confusion-matrix suite:** accuracy 0.795, precision 0.692, recall 0.378, F1 0.488, specificity 0.941, **MCC 0.401**
- **Secondary, threshold-free continuous score:** ROC-AUC 0.663, PR-AUC 0.459 (68.9% of the full-history reference AUC of 0.961 -- expected for a coarse, month-level aggregate signal, not a failure)
- **Live API self-test (Notebook 60):** True
- **Estimated Year-1 ROI (Notebook 61, illustrative cost assumptions):** ~74,872%, ~$38,000 implementation cost, ~0 months payback -- see `reports/financial_impact_reporting_packaging/financial_assumptions.json` for every assumption's real source/rationale.

## 5. Live Dashboard

- [Real-Time Portfolio Monitoring Ops Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem11_Real_Time_Portfolio_Monitoring/reports/financial_impact_reporting_packaging/real_time_portfolio_monitoring_ops_dashboard.html) -- interactive alert-feed + KPI dashboard (also linked from the platform root README's sequential dashboard index).

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

## 6. How to Run

1. Complete Notebook 06 (Problem 1) first -- this problem depends on its real SHAP feature ranking.
2. Run `notebooks/58_real_time_portfolio_monitoring_business_understanding.ipynb` through `notebooks/61_real_time_portfolio_monitoring_financial_impact_reporting_packaging.ipynb` in numeric order -- each is a single, idempotent code cell.

The deployed `portfolio_alert_feed_service.py` API requires a valid `X-API-Key` header on every endpoint except `/health` (see `src/.env.example`).

## 7. Project Structure

```
Problem11_Real_Time_Portfolio_Monitoring/
├── artifacts/
├── data/
│   └── README.md
├── docs/
│   └── portfolio_monitoring_policy.json
├── models/
│   └── README.md
├── notebooks/
│   ├── 58_real_time_portfolio_monitoring_business_understanding.ipynb
│   ├── 59_real_time_portfolio_monitoring_modeling.ipynb
│   ├── 60_real_time_portfolio_monitoring_validation_deployment.ipynb
│   └── 61_real_time_portfolio_monitoring_financial_impact_reporting_packaging.ipynb
├── reports/
│   ├── modeling/
│   │   ├── portfolio_monitoring_modeling_results.json
│   │   └── notebook_59_*.png
│   ├── validation_deployment/
│   │   ├── portfolio_monitoring_statistical_validation.csv
│   │   ├── deployment_readiness_checklist.csv
│   │   ├── Real_Time_Portfolio_Monitoring_Validation_Deployment_Report.docx
│   │   └── notebook_60_*.png
│   └── financial_impact_reporting_packaging/
│       ├── real_time_portfolio_monitoring_ops_dashboard.html
│       ├── AMEX_Problem11_Financial_Impact_Workbook.xlsx
│       ├── Real_Time_Portfolio_Monitoring_Financial_Impact_Report.docx
│       ├── financial_assumptions.json
│       ├── p11_smart_suggestions.csv
│       └── net_benefit_waterfall_chart.png
├── src/
│   ├── docker/
│   │   ├── .dockerignore
│   │   ├── docker-compose.yml
│   │   └── Dockerfile
│   ├── portfolio_alert_feed_service.py
│   ├── portfolio_monitoring_deployment_policy.json
│   ├── requirements-api.txt
│   └── .env.example
├── tests/
├── .gitignore
├── LICENSE
└── requirements.txt
```

## 8. License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.

_Generated 2026-08-27, from this problem's real, measured Notebook 58-61 outputs._
