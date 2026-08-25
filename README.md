# AMEX RiskIQ: Enterprise Credit Risk Platform

[![CI](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/ci.yml) [![Code Quality](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/code-quality.yml/badge.svg)](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/code-quality.yml) [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

An enterprise-grade credit risk platform built end-to-end on the real Kaggle **American Express Default Prediction** dataset. This repository holds **Phase 1: Foundation** and **Phase 2: Regulatory & Loss Provisioning** of a larger 14-problem, 5-phase roadmap — five problems, 37 notebooks combined. Later phases (Behavioral Intelligence, Operational Risk Management, Customer & Business Intelligence) are planned.

Every number in this repository is either computed live by that notebook's own code on the real dataset, or is an explicitly labeled, editable `ASSUMPTION` where the dataset genuinely has no ground truth for it — never silently presented as fact.

## Platform at a Glance (Real, Measured)

| Metric | Value |
|---|---|
| Champion PD model (measured, Problem 1) | XGBoost |
| Champion holdout AUC (measured) | 0.9620 |
| Champion holdout AMEX metric (measured) | 0.7936 |
| Training / test customers aggregated (measured) | 458,913 / 924,621 |
| Live observed default rate (measured) | 25.89% |
| Risk tiers defined (Problem 2) | 4, chi-square p≈0.0, Cramér's V 0.76 |
| ECL, IFRS9 vs. CECL vs. flat baseline (Problem 3, measured) | $72.4M / $73.1M / $67.8M |
| Severity tiers + LGD (Problem 4, measured) | 3 tiers, LGD 0.30 / 0.45 / 0.65, Severe-to-Low default ratio 48.7x |
| Earliest reliable default signal (Problem 5, measured) | 3 statements, 96.3% of full-history AUC, RECOMMENDED FOR PRODUCTION |
| Live FastAPI self-tests, all deployable services (measured) | Pass |

## Live Dashboards

- 📊 [Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem1_Credit_Scoring_PD_Prediction/reports/executive_reports/Financial_Impact_Dashboard.html) — interactive ROI, revenue-impact, and loss-reduction dashboard for Problem 1
- 📈 [Power BI Dashboard Preview](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem1_Credit_Scoring_PD_Prediction/reports/powerbi_dashboard/PowerBI_Dashboard_Preview.html) — star-schema data model and dashboard preview
- 📊 [ECL Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem3_Expected_Credit_Loss_IFRS9_CECL/reports/financial_impact_reporting_packaging/ecl_financial_impact_dashboard.html) — IFRS9/CECL reserve-change and stress-buffer dashboard for Problem 3
- 📊 [Loss Severity Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem4_Delinquency_Escalation_Loss_Severity/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — tiered-LGD vs flat-LGD loss-severity dashboard for Problem 4
- 📊 [Early Payment Default Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem5_Early_Payment_Default_Detection/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — early-warning value and loss-prevention ROI dashboard for Problem 5

(Served via GitHub Pages — click through to view them rendered directly in your browser. **Note:** clicking an `.html` file directly in GitHub's file browser shows raw source code, not the rendered page — always use these `github.io` links, or any problem's own README, to view a dashboard rendered.)

## Repository Structure

```
AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/
├── Problem1_Credit_Scoring_PD_Prediction/       18 notebooks -- data engineering through
│                                                 production architecture & comprehensive reporting
├── Problem2_Risk_Tier_Classification/           7 notebooks -- maps Problem 1's real PD score to
│                                                 discrete, validated, deployed & monitored risk tiers
├── Problem3_Expected_Credit_Loss_IFRS9_CECL/    4 notebooks -- dual-standard (IFRS9/CECL) ECL,
│                                                 built on Problem 1's PD + Problem 4's severity tier
├── Problem4_Delinquency_Escalation_Loss_Severity/  4 notebooks -- real, validated, 3-tier
│                                                 loss-severity score, replaces Problem 1's flat LGD
├── Problem5_Early_Payment_Default_Detection/    4 notebooks -- scores default risk from a
│                                                 customer's earliest statements, months before
│                                                 full-history scoring is possible
├── shared/                                      Cross-problem library (metrics, config, monitoring),
│                                                 extracted & unit-tested -- see shared/tests/
├── scripts/                                     CI helper scripts (notebook syntax checker)
├── .github/workflows/                           ci.yml (tests, notebook syntax) +
│                                                 code-quality.yml (lint, format check, security scan)
├── .github/ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md
├── setup.py, pyproject.toml, Makefile           Packaging + `make test` / `make lint` / `make test-all`
├── CONTRIBUTING.md                              Engineering standards this repo follows
├── ROADMAP.md                                   Hardening-track + problem-roadmap status, both tracks
├── BENCHMARKS.md                                Real baseline-vs-model comparisons, all 5 problems
├── LICENSE
└── README.md   (this file)
```

Each subfolder is a complete, independently runnable package with its own `README.md`, `notebooks/`, `src/` (deployable scorer/service — Problems 3, 4, and 5 each also ship a `src/docker/` container for their service), `tests/` (pytest), `reports/` (real Word reports, Excel workbooks, HTML dashboards per pillar), `docs/`, `models/`, and `requirements.txt`. Start with each subfolder's own README for full detail.

## Engineering & Testing

- **CI** is split across two workflows: `.github/workflows/ci.yml` (a
  syntax check of every code cell in every notebook via
  `scripts/check_notebook_syntax.py`, 37 notebooks, plus the unit test
  suite across all five problems) and `.github/workflows/code-quality.yml`
  (pyflakes lint — advisory, see `docs/known_lint_findings.md`; `black
  --check` format check — advisory, repo-wide reformatting is a deliberate
  future pass, see `ROADMAP.md`; and a `bandit` security scan of every
  problem's real deployable `src/` — currently blocking, 0 findings).
- **Tests** (73 passing across all five problems + `shared/` as of this
  writing) cover the parts of this platform that are already standalone,
  real Python (not notebook cells): every problem's deployable scorer or
  FastAPI service, tested either against small, genuinely-fit synthetic
  fixtures (Problems 1/2, whose champion model exceeds this package's
  size-safety cap) or — for Problems 3, 4, and 5, whose deployable
  artifacts are small enough to ship directly — against the **real,
  measured scoring bundle or trained model itself**, not a mock. See each
  problem's `tests/conftest.py` for which, and each problem's
  `MODEL_CARD.md` for the real trained numbers.
- **Deployment**: Problems 1, 3, 4, and 5 each ship a runnable FastAPI
  service in `src/`, with a `src/docker/` Dockerfile + docker-compose.yml.
  Problems 3, 4, and 5's real deployable artifacts (scoring bundles / the
  real trained early-default model) are small enough to bake directly into
  the image — fully self-contained, no volume mount required. Problem 1's
  much larger champion model is instead mounted at runtime. `make help`
  (or each problem's own README/MODEL_CARD) lists the exact run commands.
- **`shared/`** holds logic extracted, byte-verified-identical (or, for
  Problem 2's tier assignment, generalized with the exact same behavior),
  from the notebooks/services that first defined it: the official AMEX
  competition metric, the platform config loader, the PSI monitoring
  helper, and threshold-band assignment — a single tested copy instead of
  duplicated inline code, installable in editable mode via `pip install
  -e .`. See `shared/__init__.py` and `ROADMAP.md` for why the notebooks
  aren't wired to import from it yet.
- **Real, measured comparisons** across all five problems — every
  baseline-vs-model delta, side by side — are consolidated in
  `BENCHMARKS.md`.

## How to Run

1. Install Python 3.11 and the packages in each subfolder's `requirements.txt`.
2. Download the real Kaggle competition CSVs (see each subfolder's `data/README.md`) — raw data is not redistributed here.
3. Run `Problem1_Credit_Scoring_PD_Prediction/notebooks/` in numeric order (01 → 18) first — every later problem depends on Problem 1's real champion model.
4. Then `Problem2_Risk_Tier_Classification/notebooks/` (19 → 25) and `Problem4_Delinquency_Escalation_Loss_Severity/notebooks/` (26 → 29) — Problem 3 depends on Problem 4's real severity tier.
5. Then `Problem3_Expected_Credit_Loss_IFRS9_CECL/notebooks/` (30 → 33).
6. Then `Problem5_Early_Payment_Default_Detection/notebooks/` (34 → 37) — independent of Problems 2-4, only needs Problem 1.

Every notebook is a single, idempotent code cell — safe to re-run, and each notebook's own intro states exactly which prior notebooks it depends on.

## Technologies Used

Polars (WARP-tuned thread pools), NumPy/Pandas, scikit-learn, XGBoost/LightGBM/CatBoost, SHAP & LIME, FastAPI + Uvicorn, Docker, Power BI (star schema + DAX), python-docx/openpyxl/Matplotlib/Chart.js for reporting.

## Roadmap

- **Phase 1 — Foundation** (this repository): Problem 1 (Probability of Default), Problem 2 (Risk Tier Classification) — complete.
- **Phase 2 — Regulatory & Loss Provisioning** (this repository): Problem 3 (Expected Credit Loss, IFRS9/CECL), Problem 4 (Delinquency Escalation / Loss Severity), Problem 5 (Early Payment Default Detection) — **complete**.
- **Phase 3 — Behavioral Intelligence**, **Phase 4 — Operational Risk Management**, **Phase 5 — Customer & Business Intelligence**: planned.

## License

All Rights Reserved — this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
