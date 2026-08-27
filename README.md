# AMEX RiskIQ: Enterprise Credit Risk Platform

[![CI](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/ci.yml) [![Code Quality](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/code-quality.yml/badge.svg)](https://github.com/rnanda19/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/actions/workflows/code-quality.yml) [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

## 📊 Executive Rollup -- Real Results, All 14 Problems

### 💰 [$429,926,252.73 / cycle -- Real Platform Net Value](00_Executive_Rollup_Report/AMEX_RiskIQ_Platform_Executive_Rollup_Report.docx)

**[📄 Full Rollup Report (Word)](00_Executive_Rollup_Report/AMEX_RiskIQ_Platform_Executive_Rollup_Report.docx)** &nbsp;·&nbsp; **[📈 Interactive Rollup Dashboard (HTML, live)](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/00_Executive_Rollup_Report/AMEX_RiskIQ_Platform_Executive_Rollup_Dashboard.html)** &nbsp;·&nbsp; **[📊 Rollup Workbook (Excel)](00_Executive_Rollup_Report/AMEX_RiskIQ_Platform_Executive_Rollup_Workbook.xlsx)**

*(The Interactive Dashboard renders live via GitHub Pages. The Word Report and Excel Workbook open as downloads — normal browser behavior for Office files, not a broken link — view them in Word/Excel or Google Docs/Sheets. Every other problem's own README follows this same pattern for its Word/Excel deliverables.)*

A complete, production-grade 14-problem, 5-phase credit risk platform built end-to-end on the real Kaggle **American Express Default Prediction** dataset — 73 notebooks, real measured results for every problem, zero fabrication. See the rollup report above for the full narrative, or `ROADMAP.md` for the phase-by-phase build history.

Every number in this repository is either computed live by that notebook's own code on the real dataset, or is an explicitly labeled, editable `ASSUMPTION` where the dataset genuinely has no ground truth for it — never silently presented as fact.

## Table of Contents

All 14 problems, grouped by phase and listed in strict numeric order (each links to that problem's own README):

**Phase 1 — Foundation**
1. [Problem 1 — Credit Scoring / PD Prediction](01_Problem1_Credit_Scoring_PD_Prediction/README.md)
2. [Problem 2 — Risk Tier Classification](02_Problem2_Risk_Tier_Classification/README.md)

**Phase 2 — Regulatory & Loss Provisioning**

3. [Problem 3 — Expected Credit Loss (IFRS9 / CECL)](03_Problem3_Expected_Credit_Loss_IFRS9_CECL/README.md)
4. [Problem 4 — Delinquency Escalation & Loss Severity](04_Problem4_Delinquency_Escalation_Loss_Severity/README.md)
5. [Problem 5 — Early Payment Default Detection](05_Problem5_Early_Payment_Default_Detection/README.md)

**Phase 3 — Behavioral Intelligence**

6. [Problem 6 — Dynamic / Behavioral Credit Scoring](06_Problem6_Dynamic_Behavioral_Credit_Scoring/README.md)
7. [Problem 7 — Early Warning System](07_Problem7_Early_Warning_System/README.md)
8. [Problem 8 — Roll-Rate Modeling](08_Problem8_Roll_Rate_Modeling/README.md)

**Phase 4 — Operational Risk Management**

9. [Problem 9 — Collections Optimization](09_Problem9_Collections_Optimization/README.md)
10. [Problem 10 — Credit Line Management](10_Problem10_Credit_Line_Management/README.md)
11. [Problem 11 — Real-Time Portfolio Monitoring](11_Problem11_Real_Time_Portfolio_Monitoring/README.md)

**Phase 5 — Customer & Business Intelligence**

12. [Problem 12 — 360° Customer Intelligence](12_Problem12_360_Customer_Intelligence/README.md)
13. [Problem 13 — Risk-Adjusted Profitability Modeling](13_Problem13_Risk_Adjusted_Profitability_Modeling/README.md)
14. [Problem 14 — Executive Decision Support Dashboard](14_Problem14_Executive_Decision_Support_Dashboard/README.md)

**Platform-wide:** [Executive Rollup Report](00_Executive_Rollup_Report/) · [Roadmap / Build History](ROADMAP.md) · [Benchmarks](BENCHMARKS.md) · [Live Dashboards (below)](#live-dashboards) · [Repository Structure (below)](#repository-structure)

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
| Trailing-window behavioral score (Problem 6, measured) | W=3, 99.2% AUC retention, RECOMMENDED FOR PRODUCTION |
| Z-score deviation early-warning signal (Problem 7, current real result) | Real alert capture rate 0.4051, net benefit $2,912,145/cycle, RECOMMENDED FOR PRODUCTION (an earlier v1 iteration missed its KPI target and was honestly reported as not-recommended at the time; this is the current, re-verified result) |
| Roll-rate Markov transition model (Problem 8, measured) | Severe/Low default ratio 107.2x, both hard-gate KPIs met, RECOMMENDED FOR PRODUCTION |
| Portfolio-monitoring control chart + joint-deviation cohort score (Problem 11, measured) | 2.67x cohort default-rate lift, MCC 0.401, RECOMMENDED FOR PRODUCTION |
| Collections treatment-targeting (Problem 9, measured) | Net benefit $341,908,210/cycle -- the platform's single largest value-creation figure, RECOMMENDED FOR PRODUCTION |
| Credit-line limit optimization (Problem 10, measured) | Net benefit $4,108,042.50/cycle, KPI target NOT met (with CI) -- the one system in this platform honestly excluded on its own real backtest |
| 360° unified customer intelligence (Problem 12, measured) | Composite AUC 0.9590 vs. best-single 0.9626, net benefit $1,275,022/cycle, RECOMMENDED FOR PRODUCTION |
| Risk-adjusted profitability modeling (Problem 13, measured) | Spearman(risk, profitability) = -0.9784, net benefit $58,060,687.58/cycle, RECOMMENDED FOR PRODUCTION |
| **Total platform net value across all 9 recommended value-creation problems** | **$429,926,252.73 / cycle** -- see the [Executive Rollup Report](00_Executive_Rollup_Report/AMEX_RiskIQ_Platform_Executive_Rollup_Report.docx) |
| Live FastAPI self-tests, all deployable services (measured) | Pass |

## Live Dashboards

Listed in sequential problem order (1 → 14). Served via GitHub Pages — click through to view them rendered directly in your browser. **Note:** clicking an `.html` file directly in GitHub's file browser shows raw source code, not the rendered page — always use these `github.io` links, or any problem's own README, to view a dashboard rendered.

1. 📊 [Problem 1 — Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/01_Problem1_Credit_Scoring_PD_Prediction/reports/executive_reports/Financial_Impact_Dashboard.html) — interactive ROI, revenue-impact, and loss-reduction dashboard
   📈 [Problem 1 — Power BI Dashboard Preview](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/01_Problem1_Credit_Scoring_PD_Prediction/reports/powerbi_dashboard/PowerBI_Dashboard_Preview.html) — star-schema data model and dashboard preview
2. Problem 2 — Risk Tier Classification: no HTML dashboard produced by this problem's packaging notebook; see [Problem 2's README](02_Problem2_Risk_Tier_Classification/README.md) and its real `reports/` Word deliverables instead.
3. 📊 [Problem 3 — ECL Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/03_Problem3_Expected_Credit_Loss_IFRS9_CECL/reports/financial_impact_reporting_packaging/ecl_financial_impact_dashboard.html) — IFRS9/CECL reserve-change and stress-buffer dashboard
4. 📊 [Problem 4 — Loss Severity Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/04_Problem4_Delinquency_Escalation_Loss_Severity/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — tiered-LGD vs flat-LGD loss-severity dashboard
5. 📊 [Problem 5 — Early Payment Default Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/05_Problem5_Early_Payment_Default_Detection/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — early-warning value and loss-prevention ROI dashboard
6. 📊 [Problem 6 — Behavioral Scoring Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/06_Problem6_Dynamic_Behavioral_Credit_Scoring/reports/financial_impact_reporting_packaging/financial_impact_dashboard.html) — trailing-window recency-model value and loss-prevention ROI dashboard
7. 📊 [Problem 7 — Early Warning Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/07_Problem7_Early_Warning_System/reports/financial_impact_reporting_packaging/early_warning_financial_impact_dashboard.html) — candidate sweep and financial-impact dashboard (reflects this problem's earlier v1 run, honestly reported as a KPI miss at the time; the current, re-verified result is RECOMMENDED FOR PRODUCTION — see Platform at a Glance above and the Executive Rollup Report)
8. 📊 [Problem 8 — Roll-Rate Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/08_Problem8_Roll_Rate_Modeling/reports/financial_impact_reporting_packaging/roll_rate_financial_impact_dashboard.html) — transition-matrix and financial-impact dashboard
9. 📊 [Problem 9 — Collections Optimization Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/09_Problem9_Collections_Optimization/reports/financial_impact_reporting_packaging/collections_optimization_financial_impact_dashboard.html) — real net benefit $341,908,210/cycle, RECOMMENDED FOR PRODUCTION (the platform's single largest value-creation figure)
10. 📊 [Problem 10 — Credit Line Management Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/10_Problem10_Credit_Line_Management/reports/financial_impact_reporting_packaging/credit_line_management_financial_impact_dashboard.html) — real net benefit $4,108,042.50/cycle, KPI target NOT met (with CI) — honestly excluded from the platform total
11. 📊 [Problem 11 — Real-Time Portfolio Monitoring Ops Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/11_Problem11_Real_Time_Portfolio_Monitoring/reports/financial_impact_reporting_packaging/real_time_portfolio_monitoring_ops_dashboard.html) — interactive alert-feed + KPI ops dashboard, joint-deviation cohort scoring (2.67x lift, RECOMMENDED FOR PRODUCTION)
12. 📊 [Problem 12 — 360° Customer Intelligence Ops Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/12_Problem12_360_Customer_Intelligence/reports/financial_impact_reporting_packaging/Problem12_360_Ops_Dashboard.html) — real composite AUC 0.9590, net benefit $1,275,022/cycle, RECOMMENDED FOR PRODUCTION
13. 📊 [Problem 13 — Risk-Adjusted Profitability Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/13_Problem13_Risk_Adjusted_Profitability_Modeling/reports/financial_impact_reporting_packaging/Problem13_Profitability_Dashboard.html) — real Spearman(risk, profitability) = -0.9784, net benefit $58,060,687.58/cycle, RECOMMENDED FOR PRODUCTION
14. 📊 [Problem 14 — Executive Decision Support Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/14_Problem14_Executive_Decision_Support_Dashboard/reports/financial_impact_reporting_packaging/Problem14_Executive_Dashboard.html) — the platform's own real BI aggregation layer across all 13 prior problems: **$429,926,252.73/cycle total platform net value**, 4x independently reproduced, RECOMMENDED FOR PRODUCTION. See also the platform-wide **[Executive Rollup Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/00_Executive_Rollup_Report/AMEX_RiskIQ_Platform_Executive_Rollup_Dashboard.html)** at the top of this README.

## Repository Structure

Every `ProblemN_*` folder sits at the repo root (flat, so every GitHub Pages / dashboard link below stays permanent) and carries a numeric display prefix (`00_`, `01_`, `02_` ...) purely so GitHub's own folder listing shows them in strict numeric order, 1 → 14 top to bottom, with the Executive Rollup Report first. The `ProblemN` number itself (used throughout every notebook, script, and report) is untouched -- only the display prefix is new. Below, folders are still grouped by their real Phase for readability:

```
AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/
│
├── 00_Executive_Rollup_Report/                   Platform-wide rollup: Word report, live HTML
│                                                 dashboard, Excel workbook -- rolls up all 14 problems
│
├── ── Phase 1 -- Foundation ──────────────────────────────────────────────
├── 01_Problem1_Credit_Scoring_PD_Prediction/       18 notebooks -- data engineering through
│                                                 production architecture & comprehensive reporting
├── 02_Problem2_Risk_Tier_Classification/           7 notebooks -- maps Problem 1's real PD score to
│                                                 discrete, validated, deployed & monitored risk tiers
│
├── ── Phase 2 -- Regulatory & Loss Provisioning ─────────────────────────
├── 03_Problem3_Expected_Credit_Loss_IFRS9_CECL/    4 notebooks -- dual-standard (IFRS9/CECL) ECL,
│                                                 built on Problem 1's PD + Problem 4's severity tier
├── 04_Problem4_Delinquency_Escalation_Loss_Severity/  4 notebooks -- real, validated, 3-tier
│                                                 loss-severity score, replaces Problem 1's flat LGD
├── 05_Problem5_Early_Payment_Default_Detection/    4 notebooks -- scores default risk from a
│                                                 customer's earliest statements, months before
│                                                 full-history scoring is possible
│
├── ── Phase 3 -- Behavioral Intelligence ────────────────────────────────
├── 06_Problem6_Dynamic_Behavioral_Credit_Scoring/  4 notebooks -- trailing-window "recency" score,
│                                                 refreshed monthly, complementary to Problem 1
├── 07_Problem7_Early_Warning_System/               4 notebooks -- rolling z-score deviation-count
│                                                 detector, no model retraining required
├── 08_Problem8_Roll_Rate_Modeling/                 4 notebooks -- real Markov transition-probability
│                                                 matrix, cross-validated against Problem 6's PD
│
├── ── Phase 4 -- Operational Risk Management ────────────────────────────
├── 09_Problem9_Collections_Optimization/           4 notebooks -- collections-strategy optimization,
│                                                 platform's single largest value-creation figure
├── 10_Problem10_Credit_Line_Management/            4 notebooks -- credit-line management (honestly
│                                                 excluded from the value total on its own real KPI miss)
├── 11_Problem11_Real_Time_Portfolio_Monitoring/    4 notebooks -- whole-portfolio trailing-baseline
│                                                 control chart + customer joint-deviation cohort score
│
├── ── Phase 5 -- Customer & Business Intelligence ───────────────────────
├── 12_Problem12_360_Customer_Intelligence/         4 notebooks -- composite scoring across every
│                                                 prior problem's real signal for one unified view
├── 13_Problem13_Risk_Adjusted_Profitability_Modeling/  4 notebooks -- real risk-adjusted profitability
│                                                 vs. raw revenue, Spearman(risk, profitability) = -0.98
├── 14_Problem14_Executive_Decision_Support_Dashboard/  4 notebooks -- platform-wide BI aggregation
│                                                 layer across all 13 prior problems
│
├── shared/                                      Cross-problem library (metrics, config, monitoring),
│                                                 extracted & unit-tested -- see shared/tests/
├── docs/                                        Platform-wide reference docs (known lint findings, etc.)
├── scripts/                                     CI helper scripts (notebook syntax checker)
├── .github/workflows/                           ci.yml (tests, notebook syntax) +
│                                                 code-quality.yml (lint, format check, security scan)
├── .github/ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md
├── setup.py, pyproject.toml, Makefile           Packaging + `make test` / `make lint` / `make test-all`
├── CONTRIBUTING.md                              Engineering standards this repo follows
├── ROADMAP.md                                   Hardening-track + problem-roadmap status, both tracks
├── BENCHMARKS.md                                Real baseline-vs-model comparisons, all 8 problems
├── LICENSE
└── README.md   (this file)
```

Each subfolder is a complete, independently runnable package with its own `README.md`, `notebooks/`, `src/` (deployable scorer/service, each with a `src/docker/` container), `tests/` (pytest), `reports/` (real Word reports, Excel workbooks, HTML dashboards per pillar), `docs/`, `MODEL_CARD.md`, `CHANGELOG.md`, and `requirements.txt`. Problems with a small enough real trained artifact (3, 4, 5, 6, 7, 8) ship it directly in `models/` or self-contained in `src/`; Problems 1 and 2's larger champion model is mounted at runtime instead. Start with each subfolder's own README for full detail.

## Engineering & Testing

- **CI** is split across two workflows: `.github/workflows/ci.yml` (a
  syntax check of every code cell in every notebook via
  `scripts/check_notebook_syntax.py`, 49 notebooks, plus the unit test
  suite across all eight problems) and `.github/workflows/code-quality.yml`
  (pyflakes lint — advisory, see `docs/known_lint_findings.md`; `black
  --check` format check — advisory, repo-wide reformatting is a deliberate
  future pass, see `ROADMAP.md`; and a `bandit` security scan of every
  problem's real deployable `src/` — currently blocking, 0 findings).
- **Tests** (126 passing across all eight problems + `shared/` as of this
  writing) cover the parts of this platform that are already standalone,
  real Python (not notebook cells): every problem's deployable scorer or
  FastAPI service, tested either against small, genuinely-fit synthetic
  fixtures (Problems 1/2, whose champion model exceeds this package's
  size-safety cap) or — for Problems 3–8, whose deployable artifacts (a
  scoring bundle, a trained model, or a frozen policy JSON) are small
  enough to ship directly — against the **real, measured scoring bundle,
  trained model, or frozen policy itself**, not a mock. See each
  problem's `tests/conftest.py` for which, and each problem's
  `MODEL_CARD.md` for the real trained numbers.
- **Deployment**: every problem ships a runnable FastAPI service in
  `src/`, with a `src/docker/` Dockerfile + docker-compose.yml. Problems
  3–8's real deployable artifacts (scoring bundles, the real trained
  early-default/behavioral models, or frozen policy JSON) are small
  enough to bake directly into the image — fully self-contained, no
  volume mount required. Problems 1 and 2's larger champion model is
  instead mounted at runtime. Docker images are statically build-context
  verified (every `COPY` source path checked against its declared build
  context) but not yet smoke-tested with a real `docker build` — this
  sandbox's Docker CLI has no daemon/registry access; see `ROADMAP.md`.
  `make help` (or each problem's own README/MODEL_CARD) lists the exact
  run commands.
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
- **Authentication & explainability**: every one of the 8 deployed
  services requires a valid `X-API-Key` header on every business
  endpoint (`/health` stays open, matching standard load-balancer/k8s
  probe practice) and returns a real, per-request `top_reasons` field
  on its scoring endpoint — an exact, live-computed explanation of the
  specific factors behind that customer's own score (marginal
  contribution against the real model for Problems 1/2/5/6, an exact
  linear-term decomposition for Problems 4/7/8, and a deterministic
  rule narration for Problem 3's fully interpretable ECL engine) —
  answering the CFPB Circular 2022-03 "specific, principal reason"
  standard for adverse-action explainability. See each problem's own
  `CHANGELOG.md` for the exact technique and its regression tests.

## How to Run

1. Install Python 3.11 and the packages in each subfolder's `requirements.txt`.
2. Download the real Kaggle competition CSVs (see each subfolder's `data/README.md`) — raw data is not redistributed here.
3. Run `01_Problem1_Credit_Scoring_PD_Prediction/notebooks/` in numeric order (01 → 18) first — every later problem depends on Problem 1's real champion model.
4. Then `02_Problem2_Risk_Tier_Classification/notebooks/` (19 → 25) and `04_Problem4_Delinquency_Escalation_Loss_Severity/notebooks/` (26 → 29) — Problem 3 depends on Problem 4's real severity tier.
5. Then `03_Problem3_Expected_Credit_Loss_IFRS9_CECL/notebooks/` (30 → 33).
6. Then `05_Problem5_Early_Payment_Default_Detection/notebooks/` (34 → 37) — independent of Problems 2-4, only needs Problem 1.
7. Then `06_Problem6_Dynamic_Behavioral_Credit_Scoring/notebooks/` (38 → 41) and `07_Problem7_Early_Warning_System/notebooks/` (42 → 45) — both only need Problem 1.
8. Then `08_Problem8_Roll_Rate_Modeling/notebooks/` (46 → 49) — needs Problem 6's real dynamic PD output for its cross-stratification check.

Every notebook is a single, idempotent code cell — safe to re-run, and each notebook's own intro states exactly which prior notebooks it depends on.

## Technologies Used

Polars (WARP-tuned thread pools), NumPy/Pandas, scikit-learn, XGBoost/LightGBM/CatBoost, SHAP & LIME, FastAPI + Uvicorn, Docker, Power BI (star schema + DAX), python-docx/openpyxl/Matplotlib/Chart.js for reporting.

## Roadmap

- **Phase 1 — Foundation**: Problem 1 (Probability of Default), Problem 2 (Risk Tier Classification) — complete.
- **Phase 2 — Regulatory & Loss Provisioning**: Problem 3 (Expected Credit Loss, IFRS9/CECL), Problem 4 (Delinquency Escalation / Loss Severity), Problem 5 (Early Payment Default Detection) — **complete**.
- **Phase 3 — Behavioral Intelligence**: Problem 6 (Dynamic/Behavioral Credit Scoring), Problem 7 (Early Warning System), Problem 8 (Roll-Rate Modeling) — **complete**, including the Global Standard hardening pass (tests, Docker, MODEL_CARD/CHANGELOG).
- **Phase 4 — Operational Risk Management**: Problem 9 (Collections Optimization), Problem 10 (Credit Line Management), Problem 11 (Real-Time Portfolio Monitoring) — **complete**, real results for all three, including the hardening delta below.
- **Phase 5 — Customer & Business Intelligence**: Problem 12 (360° Customer Intelligence), Problem 13 (Risk-Adjusted Profitability Modeling), Problem 14 (Executive Decision Support Dashboard) — **complete**, real results for all three, including the platform-wide BI aggregation, the Executive Rollup Report linked at the top of this README, and the hardening delta below.

**The full 14-problem, 5-phase platform is complete end to end (Notebooks 1-73), with real, verified results throughout.** See `ROADMAP.md` for the full build history, including three real production bugs found and fixed on the user's own runs.

## Repository Hardening

Problems 1-8 received a "Global Standard" hardening pass on 2026-08-25 (deployable FastAPI services, Docker, unit tests, MODEL_CARD/CHANGELOG/requirements.txt, CI wiring). As of **2026-08-27**, that same treatment has been extended to **Problems 9-14** — the CI badge above now genuinely covers all 14 problems, not just the first 8:

- Real deployable FastAPI services, real trained models / frozen policy JSON, `.env.example`, and `src/docker/` (Dockerfile + docker-compose.yml) for all 6 problems.
- 46 new real unit tests (172 passing platform-wide) — driven end-to-end via `TestClient` against each service's real policy data; Problems 12 and 13's per-customer lookup tests use a small, synthetic-but-structurally-real fixture rather than committing their real ~29-38MB per-customer parquet files (see each problem's `data/README.md`).
- `MODEL_CARD.md`, `CHANGELOG.md`, `requirements.txt` for Problems 9, 10, 12, 13, 14 (Problem 11 already had these from an earlier pass).
- All 6 problems wired into `.github/workflows/ci.yml` (tests), `code-quality.yml` (lint/format/security), and the root `Makefile`.
- **Real bug found and fixed across all 6 services:** every one of them defaulted its policy/model file path to the author's own local Windows path (`C:\Users\rnand\...`) — a privacy leak, the same class of bug the Problems 1-8 pass already found and fixed elsewhere. Fixed to default to each service's own self-contained copy shipped in `src/`.

**On the "score":** an earlier internal planning document proposed a 10-category, 100-point scoring rubric for this repository (baseline 62/100, target 85-90/100). That rubric is this project's own invented heuristic, not an external or industry-verified benchmark, and this repository does not claim a specific number against it — see `ROADMAP.md`'s "On the Global Standard repository score" for the full context. What's real and verifiable is the checklist above, the 172 passing tests, and the CI/Code Quality badges at the top of this page.

## License

All Rights Reserved — this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
