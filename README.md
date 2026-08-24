# AMEX RiskIQ: Enterprise Credit Risk Platform

[![CI](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/ci.yml) [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

An enterprise-grade credit risk platform built end-to-end on the real Kaggle **American Express Default Prediction** dataset. This repository holds **Phase 1: Foundation** of a larger 14-problem, 5-phase roadmap — Problem 1 (Probability of Default) and Problem 2 (Risk Tier Classification), 25 notebooks combined. Later phases (Regulatory & Loss Provisioning, Behavioral Intelligence, Operational Risk Management, Customer & Business Intelligence) are in active development.

Every number in this repository is either computed live by that notebook's own code on the real dataset, or is an explicitly labeled, editable `ASSUMPTION` where the dataset genuinely has no ground truth for it — never silently presented as fact.

## Phase 1 at a Glance (Real, Measured)

| Metric | Value |
|---|---|
| Champion PD model (measured) | XGBoost |
| Champion holdout AUC (measured) | 0.9620 |
| Champion holdout AMEX metric (measured) | 0.7936 |
| Training customers aggregated (measured) | 458,913 |
| Test customers aggregated (measured) | 924,621 |
| Live observed default rate (measured) | 25.89% |
| Total RWA, Basel III (computed) | $203,644,380 |
| Total IFRS9 ECL, flat-LGD baseline (computed) | $67,830,906 |
| Risk tiers defined (Problem 2) | 4, chi-square p≈0.0, Cramér's V 0.76 |
| Live FastAPI self-test, both problems (measured) | Pass |

## Live Dashboards

- 📊 [Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem1_Credit_Scoring_PD_Prediction/reports/executive_reports/Financial_Impact_Dashboard.html) — interactive ROI, revenue-impact, and loss-reduction dashboard for Problem 1
- 📈 [Power BI Dashboard Preview](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem1_Credit_Scoring_PD_Prediction/reports/powerbi_dashboard/PowerBI_Dashboard_Preview.html) — star-schema data model and dashboard preview

(Served via GitHub Pages — click through to view them rendered directly in your browser.)

## Repository Structure

```
AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/
├── Problem1_Credit_Scoring_PD_Prediction/    18 notebooks -- data engineering through
│                                              production architecture & comprehensive reporting
├── Problem2_Risk_Tier_Classification/        7 notebooks -- maps Problem 1's real PD score to
│                                              discrete, validated, deployed & monitored risk tiers
├── shared/                                   Cross-problem library (metrics, config, monitoring),
│                                              extracted & unit-tested -- see shared/tests/
├── scripts/                                  CI helper scripts (notebook syntax checker)
├── .github/workflows/                        CI: notebook syntax check, unit tests, lint
├── CONTRIBUTING.md                           Engineering standards this repo follows
├── ROADMAP.md                                Hardening-track + problem-roadmap status, both tracks
├── LICENSE
└── README.md   (this file)
```

Each subfolder is a complete, independently runnable package with its own `README.md`, `notebooks/`, `src/` (FastAPI service + Docker), `tests/` (pytest), `reports/` (real Word reports per pillar), `docs/`, `models/`, and `requirements.txt`. Start with each subfolder's own README for full detail.

## Engineering & Testing

- **CI** (`.github/workflows/ci.yml`) runs on every push: a syntax check of
  every code cell in every notebook (`scripts/check_notebook_syntax.py`),
  the unit test suite, and lint (pyflakes, currently advisory — see
  `docs/known_lint_findings.md`).
- **Tests** (41 passing, both problems + `shared/`) cover the parts of this
  platform that are already standalone, real Python (not notebook cells):
  both problems' FastAPI scoring services and Problem 1's monitoring job,
  tested against small, genuinely-fit synthetic fixtures so CI never needs
  the real multi-GB trained model — see each problem's
  `tests/conftest.py` for how, and each problem's `MODEL_CARD.md` for what
  the real trained numbers are.
- **`shared/`** holds logic extracted, byte-verified-identical (or, for
  Problem 2's tier assignment, generalized with the exact same behavior),
  from the notebooks/services that first defined it: the official AMEX
  competition metric, the platform config loader, the PSI monitoring
  helper, and threshold-band assignment — a single tested copy instead of
  duplicated inline code. See `shared/__init__.py` and `ROADMAP.md` for why
  the notebooks aren't wired to import from it yet.

## How to Run

1. Install Python 3.11 and the packages in each subfolder's `requirements.txt`.
2. Download the real Kaggle competition CSVs (see each subfolder's `data/README.md`) — raw data is not redistributed here.
3. Run `Problem1_Credit_Scoring_PD_Prediction/notebooks/` in numeric order (01 → 18) first — Problem 2 has a hard dependency on Problem 1's real champion model.
4. Then run `Problem2_Risk_Tier_Classification/notebooks/` in numeric order (19 → 25).

Every notebook is a single, idempotent code cell — safe to re-run, and each notebook's own intro states exactly which prior notebooks it depends on.

## Technologies Used

Polars (WARP-tuned thread pools), NumPy/Pandas, scikit-learn, XGBoost/LightGBM/CatBoost, SHAP & LIME, FastAPI + Uvicorn, Docker, Power BI (star schema + DAX), python-docx/Matplotlib for reporting.

## Roadmap

- **Phase 1 — Foundation** (this repository): Problem 1 (Probability of Default), Problem 2 (Risk Tier Classification) — complete.
- **Phase 2 — Regulatory & Loss Provisioning**: Problem 3 (Expected Credit Loss, IFRS9/CECL), Problem 4 (Delinquency Escalation / Loss Severity), Problem 5 (Early Payment Default Detection) — in progress.
- **Phase 3 — Behavioral Intelligence**, **Phase 4 — Operational Risk Management**, **Phase 5 — Customer & Business Intelligence**: planned.

## License

All Rights Reserved — this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
