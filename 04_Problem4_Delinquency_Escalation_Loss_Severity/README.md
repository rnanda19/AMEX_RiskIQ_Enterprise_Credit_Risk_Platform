# AMEX Enterprise Credit Risk Platform -- Delinquency Escalation / Loss Severity

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 2, Problem 4 of a 14-problem enterprise credit risk platform: a **4-notebook** build (Notebooks 26-29) that replaces Problem 1's flat 45% LGD assumption with a real, 3-tier, validated Escalation Severity Score -- so loss provisioning reflects how *severe* an account's delinquency signals are, not just whether it defaults. Depends on Problem 1's real champion PD model and feature store.

## 1. Overview

- **Champion PD model reused (measured, Problem 1):** xgboost
- **Severity tiers (measured):** 3 (Low Severity, Moderate Severity, Severe), LGD 0.3015 / 0.45 / 0.648
- **Severe-to-Low default-rate ratio (measured):** 48.66x
- **Real features used (measured):** 243 correlation-filtered D_* engineered columns

## Live Dashboard

- 📊 [Loss Severity Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/04_Problem4_Delinquency_Escalation_Loss_Severity/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — interactive tiered-LGD vs flat-LGD loss-severity dashboard

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

## 2. Problem Statement

Not every default is equally costly -- a flat LGD hides real severity variation across accounts. This build derives an outcome-aware, monotonic Escalation Severity Score from real delinquency-adjacent engineered features, buckets it into 3 tiers, and validates that tier assignment is a statistically real, monotonic proxy for eventual loss severity, then deploys it as a standalone scorer.

## 3. Approach & Methodology

Notebook 26 (LGD Policy -- defines the tier framework and baseline flat LGD) -> Notebook 27 (LGD Modeling -- computes a weighted severity score from 243 real correlation-filtered features, buckets into 3 tiers, validates default-rate monotonicity) -> Notebook 28 (Statistical Validation & Deployment -- chi-square/z-test/split-half PSI, a standalone `severity_scorer.py` verified via an all-customer, boundary-tie-aware self-test) -> Notebook 29 (this packaging notebook -- the master template reused by Problems 3 and 5).

## 4. Key Results (Real, Measured)

- Chi-square (tier vs. actual default), p-value: 0.0
- Cramer's V (effect size): 0.6415662408634579
- Z-test p-value: 0.0
- Split-half score PSI: 6.8687392670068315e-06 (stable)
- Standalone `severity_scorer.py` self-test: 91,783/91,783 customers checked, 0 hard mismatches, 0 boundary ties
- Loss under flat 45% LGD (measured): $53,473,500.00
- Loss under tier-differentiated LGD (measured): $72,908,932.50
- Reserve-change delta vs. flat baseline (measured): +$19,435,432.50
- Year-1 ROI / payback (measured, efficiency-only, excludes the reserve-change dollars): 64,505.6% / 0.02 months

## 5. Repository Structure

```
04_Problem4_Delinquency_Escalation_Loss_Severity/
|-- notebooks/          4 notebooks (26-29)
|-- src/                severity_scorer.py -- standalone deployable severity scorer
|-- reports/            real Word reports, Excel workbook, HTML dashboard, charts, per-notebook CSVs
|-- artifacts/          real notebook_26-29_summary.json + project_config.json
|-- docs/                lgd_policy.json (the real, frozen policy), stakeholder analysis
|-- data/                see data/README.md
|-- models/              see models/README.md
`-- tests/               pytest coverage for severity_scorer.py against the real, measured scoring bundle
```

## 6. Deployable Scorer

`src/severity_scorer.py` scores one customer's real D_* engineered features into a severity tier and LGD, loading every weight/mean/std/cutpoint from `reports/validation_deployment/severity_scoring_bundle.json` at full float precision -- deliberately NOT re-derived or rounded, after a real bug (see project history) was found and fixed where a rounded display copy of the weights caused real-size score drift.

The deployed `severity_scoring_service.py` API requires a valid `X-API-Key` header on every endpoint except `/health` (see `.env.example`), and its `/score` response includes a real `top_reasons` field -- the exact per-feature weight*direction*z terms that drove this customer's own severity score (see `CHANGELOG.md`).

## 7. Reproducing This

Raw Kaggle data is not redistributed here (see `data/README.md`). Run Problem 1's Notebooks 01-05 first, then this problem's Notebooks 26-29 against your own local copy of the platform folder.

## 8. Zero-Fabrication Statement

Every number above is computed live by that notebook's own code on the real dataset. Financial-impact assumptions (intervention success rate, implementation cost, cycles/year) are explicit, labeled `ASSUMPTION`s in `artifacts/financial_assumptions.json`.

## License

See [LICENSE](LICENSE) -- All Rights Reserved. Published for portfolio/demonstration/evaluation purposes only.
