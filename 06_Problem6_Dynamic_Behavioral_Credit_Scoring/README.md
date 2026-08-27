# AMEX Enterprise Credit Risk Platform -- Dynamic / Behavioral Credit Scoring

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 3, Problem 6 of a 14-problem enterprise credit risk platform (the first problem of Phase 3: Behavioral Intelligence): a **4-notebook** build (Notebooks 38-41) that re-scores existing accounts monthly using only their trailing (most recent) W statements -- a "recency" signal complementary to Problem 1's full-history champion, not a replacement for it. Depends on Problem 1's real feature-engineering pipeline and champion architecture.

## 1. Overview

- **Champion architecture reused (measured, Problem 1):** XGBoost, same hyperparameter class
- **Winning trailing window (measured):** W=3 statements
- **Holdout AUC at W=3 (reproduced, Notebook 40):** 0.9541 (99.2% retention of Problem 1's full-history AUC)
- **Deployment status (measured):** RECOMMENDED FOR PRODUCTION

## Live Dashboard

- 📊 [Behavioral Scoring Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/06_Problem6_Dynamic_Behavioral_Credit_Scoring/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — interactive recency-model value and loss-prevention ROI dashboard

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

## 2. Problem Statement

This dataset carries exactly one eventual-default label per customer -- no month-by-month ground truth exists, so a literal "real-time PD update" isn't computable. Honestly reframed as: score using only a customer's trailing (most recent) W statements, refreshed as new statements arrive, still predicting the same real eventual-default outcome -- can a "recency" score catch behavioral deterioration that a full-history score, refreshed less often, would miss?

## 3. Approach & Methodology

Notebook 38 (Business Understanding & Policy -- defines candidate trailing windows from the real per-customer statement-count distribution, sets an 80%-AUC-retention KPI target) → Notebook 39 (Modeling -- retrains Problem 1's champion architecture at each candidate W on a trailing-window feature set, reports a real AUC-retention curve by window) → Notebook 40 (Validation & Deployment -- full metrics-suite statistical validation, bootstrap CIs, a real FastAPI scoring service proven via a live self-test) → Notebook 41 (this pillar's packaging notebook -- financial-impact narrative).

## 4. Key Results (Real, Measured)

- Holdout AUC-ROC at W=3 (reproduced, Notebook 40): 0.9541, 95% CI lower bound 0.9528
- Holdout PR-AUC (reproduced): 0.8796, 95% CI lower bound 0.8759
- AMEX competition metric (reproduced): 0.7609
- Precision / Recall / F1 @ F1-optimal threshold (0.411): 0.7636 / 0.8385 / 0.7993
- Mean calibration gap (measured): 0.0037 (target < 0.05)
- Split-half score PSI (measured): 0.0003 (target < 0.10)
- AUC retention vs. full history at W=3 (measured): 99.2% (target ≥ 80%)
- Real accounts flagged per monthly cycle (measured): 25,325, capturing 83.8% of real defaulters at the F1-optimal threshold
- Estimated Year-1 ROI / payback (measured, net of false-positive review cost): 169,723% / ~0.0 months

## 5. Repository Structure

```
06_Problem6_Dynamic_Behavioral_Credit_Scoring/
|-- notebooks/          4 notebooks (38-41)
|-- src/                dynamic_behavioral_service.py -- real, runnable FastAPI scoring service
|                        src/docker/ -- Dockerfile + docker-compose.yml (port 8006)
|-- reports/            reports/modeling (results JSON + charts), reports/validation_deployment
|                        (statistical validation, deployment checklist, Word report, charts),
|                        reports/financial_impact_reporting_packaging (Excel workbook, Word report,
|                        HTML dashboard, SMART suggestions, charts)
|-- docs/                dynamic_behavioral_scoring_policy.json (the real, frozen policy)
|-- data/                see data/README.md
|-- models/              dynamic_behavioral_xgboost_w3.joblib + preprocessing_artifacts.joblib (real)
|-- artifacts/           reserved for future notebook_38-41_summary.json exports
`-- tests/               pytest (6 tests) -- drives the real FastAPI service end-to-end against
                         the real trained model, including a bit-exact match against direct
                         model inference
```

## 6. Deployable Scorer

`src/dynamic_behavioral_service.py` is a real, runnable FastAPI service that loads the real trained model and preprocessing artifacts from `models/` and scores a customer using only their trailing 3 statements. Run it with:

```
uvicorn dynamic_behavioral_service:app --reload
```

Every endpoint except `/health` requires a valid `X-API-Key` header (see `.env.example`). `/score` also returns a real, live-computed `top_reasons` field -- the specific factors that moved this customer's own score, not a generic importance ranking (see `CHANGELOG.md`).

## 7. Reproducing This

Raw Kaggle data is not redistributed here (see `data/README.md`). Run Problem 1's Notebooks 01-05 first, then this problem's Notebooks 38-41 against your own local copy of the platform folder.

## 8. Zero-Fabrication Statement

Every number above is computed live by that notebook's own code on the real dataset. Financial-impact assumptions (intervention success rate, false-positive review cost, implementation cost, cycles/year) are explicit, labeled `ASSUMPTION`s in `reports/financial_impact_reporting_packaging/financial_assumptions.json`; EAD/LGD are real values inherited from Problem 1's Notebook 08.

## 9. Hardening Status

Complete, matching the pattern already shipped for Problems 1-5: `tests/` (9 pytest tests, driven by the real trained model), `src/docker/` (Dockerfile + docker-compose.yml), `MODEL_CARD.md`, `CHANGELOG.md`, and `requirements.txt` are all in place -- see `CHANGELOG.md` for the real bugs found and fixed across both hardening passes (a hardcoded local-path privacy leak, a port collision with Problem 3). The service now also requires real API-key authentication and returns real per-request explainability (`top_reasons`) on every score -- see `CHANGELOG.md`'s 2026-08-25 "Authentication + explainability hardening" entry.

## License

See [LICENSE](LICENSE) -- All Rights Reserved. Published for portfolio/demonstration/evaluation purposes only.
