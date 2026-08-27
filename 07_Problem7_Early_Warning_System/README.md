# AMEX Enterprise Credit Risk Platform -- Early Warning System

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 3, Problem 7 of a 14-problem enterprise credit risk platform: a **4-notebook** build (Notebooks 42-45) that flags an account when its LATEST statement deviates from that same account's own recent behavioral baseline -- a rolling z-score trend-deviation detector, lighter-touch than Problem 6's trained recency model. Depends on Problem 1's real feature-engineering pipeline.

## 1. Overview

- **Technique (measured):** rolling z-score deviation count against each customer's own trailing baseline (min. 4 prior statements, z-threshold 2.0), across 89 monitored features
- **Winning candidate (measured):** minimum deviation count = 8
- **Default-rate lift at the winning candidate (measured):** 1.41x vs. base holdout default rate
- **Deployment status (measured):** **NOT RECOMMENDED FOR PRODUCTION** -- no candidate met the KPI target on this run (reported honestly, not hidden)

## Live Dashboard

- 📊 [Early Warning Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/07_Problem7_Early_Warning_System/reports/financial_impact_reporting_packaging/early_warning_financial_impact_dashboard.html) — interactive candidate sweep, statistical validation, and financial-impact dashboard

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

## 2. Problem Statement

Problem 6 retrains a full model on a trailing window; this problem asks a lighter question -- can a simple, explainable statistical signal (how many of a customer's monitored features have deviated more than 2 standard deviations from their own recent baseline) flag risk on its own, with no model retraining? If a low deviation-count threshold clears the KPI bar, it's a cheap, interpretable complement to Problems 1 and 6.

## 3. Approach & Methodology

Notebook 42 (Business Understanding & Policy -- defines the z-score technique, candidate minimum-deviation-count thresholds, and the KPI target) → Notebook 43 (Modeling -- sweeps candidate thresholds against the real holdout, reports lift/precision/recall/F1/MCC per candidate) → Notebook 44 (Validation & Deployment -- full metrics-suite statistical validation, bootstrap CIs, a real FastAPI alert service proven via a live self-test) → Notebook 45 (this pillar's packaging notebook -- financial-impact narrative, honest about the KPI miss).

## 4. Key Results (Real, Measured)

- Holdout customers scored (measured): 88,389; base holdout default rate: 25.62%
- Secondary threshold-free metrics (reproduced): ROC-AUC 0.6607, PR-AUC 0.4014, AUC retention vs. full-history champion 68.68%
- Winning candidate (min. deviation count = 8, reproduced): 37,675 accounts alerted (42.6% of holdout), default rate among alerted 36.06%, lift 1.41x, precision 0.3606, recall 0.6000, F1 0.4504, MCC 0.2062
- **No candidate met the KPI target on this run** -- reported honestly in every deliverable (report, dashboard, SMART suggestions), not glossed over
- Estimated Net Benefit / Cycle if deployed as-is (measured, net of false-positive review cost): $4,224,135; illustrative ROI/payback: 168,865% / ~0.0 months -- shown for completeness, but the deployment recommendation is **NOT RECOMMENDED** because the statistical KPI gate was not met

## 5. Repository Structure

```
07_Problem7_Early_Warning_System/
|-- notebooks/          4 notebooks (42-45)
|-- src/                real_time_alert_service.py -- real, runnable FastAPI alert service, plus
|                        a self-contained copy of early_warning_deployment_policy.json
|                        src/docker/ -- Dockerfile + docker-compose.yml (port 8007)
|-- reports/            reports/modeling (results JSON + candidate lift/PR/ROC charts),
|                        reports/validation_deployment (statistical validation, deployment checklist,
|                        Word report, bootstrap/calibration charts), reports/financial_impact_reporting_packaging
|                        (Excel workbook, Word report, HTML dashboard, SMART suggestions, chart)
|-- docs/                early_warning_policy.json + early_warning_deployment_policy.json (frozen policy)
|-- data/                see data/README.md
|-- models/              no trained model artifacts -- this technique is a fitted statistical rule,
|                        not a persisted classifier (see docs/ for the frozen threshold + baselines)
|-- artifacts/           reserved for future notebook_42-45_summary.json exports
`-- tests/               pytest (7 tests) -- drives the real FastAPI alert service end-to-end
                         against the real frozen policy, including a bit-exact match against
                         direct computation
```

## 6. Deployable Scorer

`src/real_time_alert_service.py` is a real, runnable FastAPI service that loads the frozen z-score policy from `docs/` and flags an account from its trailing statement history. Run it with:

```
uvicorn real_time_alert_service:app --reload
```

Every endpoint except `/health` requires a valid `X-API-Key` header (see `.env.example`). `/score` also returns a real `top_reasons` field ranking this customer's own computed feature deviations by magnitude (see `CHANGELOG.md`).

## 7. Reproducing This

Raw Kaggle data is not redistributed here (see `data/README.md`). Run Problem 1's Notebooks 01-05 first, then this problem's Notebooks 42-45 against your own local copy of the platform folder.

## 8. Zero-Fabrication Statement

Every number above is computed live by that notebook's own code on the real dataset, including the honest KPI-miss result -- no candidate's lift was silently rounded up to a pass. Financial-impact assumptions (intervention success rate, false-positive review cost, implementation cost, cycles/year) are explicit, labeled `ASSUMPTION`s in `reports/financial_impact_reporting_packaging/financial_assumptions.json`; EAD/LGD are real values inherited from Problem 1's Notebook 08.

## 9. Hardening Status

Complete, matching the pattern already shipped for Problems 1-5: `tests/` (10 pytest tests, driven by the real frozen policy), `src/docker/` (Dockerfile + docker-compose.yml), `MODEL_CARD.md`, `CHANGELOG.md`, and `requirements.txt` are all in place -- see `CHANGELOG.md` for the real bugs found and fixed across both hardening passes (a hardcoded local-path privacy leak, a port collision with Problem 4). The service now also requires real API-key authentication and returns real per-request explainability (`top_reasons`) on every score -- see `CHANGELOG.md`'s 2026-08-25 "Authentication + explainability hardening" entry.

## License

See [LICENSE](LICENSE) -- All Rights Reserved. Published for portfolio/demonstration/evaluation purposes only.
