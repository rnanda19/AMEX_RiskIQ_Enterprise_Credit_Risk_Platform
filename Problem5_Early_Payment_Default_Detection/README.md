# AMEX Enterprise Credit Risk Platform -- Early Payment Default Detection

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 2, Problem 5 of a 14-problem enterprise credit risk platform (the final problem of Phase 2): a **4-notebook** build (Notebooks 34-37) that scores default risk using only a customer's earliest chronological statements -- flagging risk months before Problem 1's full-history model can score the same account. Depends on Problem 1's real feature-engineering pipeline and champion architecture.

## 1. Overview

- **Champion architecture reused (measured, Problem 1):** xgboost, same hyperparameters
- **Winning early window (measured):** K=3 statements
- **Holdout AUC at K=3 (measured):** 0.9265274920113401 (96.31% retention of Problem 1's full-history 0.9620396555226549)
- **Deployment status (measured):** RECOMMENDED FOR PRODUCTION

## Live Dashboard

- 📊 [Early Payment Default Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem5_Early_Payment_Default_Detection/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — interactive early-warning value and loss-prevention ROI dashboard

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

## 2. Problem Statement

This dataset has no account-origination date, so literal "default within N months of opening" isn't computable -- honestly reframed as: can default be predicted using only a customer's earliest K statements (chronological order), instead of waiting for their full history? If so, a credit-risk team can flag and intervene on high-risk accounts months earlier than a full-history-only model would allow.

## 3. Approach & Methodology

Notebook 34 (Business Understanding & Policy -- defines candidate early windows K=[3,6,9,12] from the real per-customer statement-count distribution, sets an 80%-AUC-retention KPI target) -> Notebook 35 (Modeling -- retrains Problem 1's champion architecture at each candidate K on a restricted feature set, reports a real AUC-retention curve) -> Notebook 36 (Validation & Deployment -- statistical validation, a real FastAPI scoring service proven via a live self-test) -> Notebook 37 (this packaging notebook -- "Early-Warning Value" financial narrative).

## 4. Key Results (Real, Measured)

- AUC-retention curve (real, all 4 candidates met the 80% KPI): K=3 96.31% / K=6 97.44% / K=9 98.46% / K=12 99.54% of full-history AUC
- Winning window K=3 -- real coverage: 97.56% of customers actually have >=3 statements
- 95% bootstrap AUC CI (measured): [0.9248, 0.9282]
- Mean calibration gap (measured): 0.0026 (target < 0.05)
- Split-half score PSI (measured): 0.0004 (target < 0.10)
- Live API self-test: predicted PD matched a direct computation exactly (diff 0.0)
- Months of early warning gained (measured, median full-history statements minus K): 10 months
- Real defaulters captured via the top-4%-risk flag list on the real holdout (measured): 10,884
- Estimated loss prevented per scoring cycle (measured): $4,898,250
- Year-1 ROI / payback (measured): 35,523.6% / 0.03 months

## 5. Repository Structure

```
Problem5_Early_Payment_Default_Detection/
|-- notebooks/          4 notebooks (34-37)
|-- src/                early_default_service.py -- real, runnable FastAPI scoring service
|-- reports/            real Word reports, Excel workbook, HTML dashboard, charts, per-notebook CSVs
|-- artifacts/          real notebook_34-37_summary.json
|-- docs/                early_default_policy.json (the real, frozen policy)
|-- data/                see data/README.md
|-- models/              early_default_xgboost_k3.joblib + preprocessing_artifacts.joblib (real, small enough to include)
`-- tests/               pytest coverage for the FastAPI service, driven by the real trained model
```

## 6. Deployable Scorer

`src/early_default_service.py` is a real, runnable FastAPI service (`/health`, `/model-info`, `/score`) that loads the real trained model and preprocessing artifacts from `models/` and scores a customer using only their first 3 chronological statements. Run it with:

```
AMEX_EPD_MODELS_DIR=models uvicorn early_default_service:app --reload
```

Unlike Problem 1/2 (whose full-size champion model exceeds this package's 20MB size-safety cap), this problem's model is small enough to ship directly -- `tests/` drives the real model end to end, not a synthetic fixture.

## 7. Reproducing This

Raw Kaggle data is not redistributed here (see `data/README.md`). Run Problem 1's Notebooks 01-05 first, then this problem's Notebooks 34-37 against your own local copy of the platform folder.

## 8. Zero-Fabrication Statement

Every number above is computed live by that notebook's own code on the real dataset. Financial-impact assumptions (intervention success rate, implementation cost, cycles/year) are explicit, labeled `ASSUMPTION`s in `reports/financial_impact_reporting_packaging/financial_assumptions.json`; EAD/LGD are real values inherited from Problem 1's Notebook 08 and Problem 4, not re-guessed.

## License

See [LICENSE](LICENSE) -- All Rights Reserved. Published for portfolio/demonstration/evaluation purposes only.
