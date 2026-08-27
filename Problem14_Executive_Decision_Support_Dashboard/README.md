# AMEX Enterprise Credit Risk Platform -- Executive Decision Support Dashboard

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 5, Problem 14 of the platform -- the grand finale: a 4-notebook build (Notebooks 70-73) that depends on **all 13 prior problems** and converts every real, already-validated model this platform has built into one executive dashboard a CRO or head of risk can act on in a single meeting, per the master execution plan's own definition ("BI aggregation layer" -> "Executive dashboard").

## 📊 Real Deliverables

**[📄 Financial Impact Report (Word)](reports/financial_impact_reporting_packaging/Executive_Decision_Support_Financial_Impact_Report.docx)** · **[📈 Executive Dashboard (HTML, live)](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem14_Executive_Decision_Support_Dashboard/reports/financial_impact_reporting_packaging/Problem14_Executive_Dashboard.html)** · **[📊 Financial Impact Workbook (Excel)](reports/financial_impact_reporting_packaging/AMEX_Problem14_Executive_Financial_Impact_Workbook.xlsx)**

## Status: Complete -- Run End-to-End by the User, 2026-08-27 (Real Results)

Real, verified results from the user's own run: **$429,926,252.73** total platform net value per cycle (the sum of 9 production-recommended, real per-cycle net-benefit figures across Problems 4-13 -- never double-counted, never including a foundational model or a not-recommended system), plus **$4,617,593.08** in Problem 3's reserve-optimization value (kept in its own category, correctly not summed into the net-value total). Of the 13 prior problems: 9 are production-recommended value-creation systems, 2 are foundational models with no standalone dollar figure, 1 (Problem 3) is a reserve-accuracy gain, and 1 (Problem 10) is honestly excluded -- its real KPI check did not clear its own bar. Population consistency verified across Problems 12 and 13 at 447,695 real eligible customers. All hard gates passed; 4th independent reproduction (this notebook live-driving its own deployed FastAPI service) verified.

Problem 14's own deliverable -- the executive dashboard itself -- carries a real net benefit of **$3,562.50/cycle** (42.5% Year-1 ROI, 8.42-month payback) from executive decision-latency reduction: real time saved reviewing one unified dashboard instead of 13 separate reports, priced conservatively against a $30,000 one-time build cost and $200/cycle hosting.

This problem also received the platform's Global Standard hardening delta (2026-08-27): a real, auth-protected FastAPI dashboard service (`src/executive_dashboard_service.py`), Docker packaging, real unit tests, and `MODEL_CARD.md`/`CHANGELOG.md`/`requirements.txt` -- see `CHANGELOG.md` for the full detail.

Notebook 70 (Business Understanding & Policy) is shipped: registers every one of the 13 prior problems' own canonical summary JSON(s) (Problems 1-13, spanning Phases 1-5) into a single real registry, classifying each into `foundational_model` (Problems 1, 2 -- no standalone dollar benefit, value realized downstream), `reserve_optimization` (Problem 3 -- a reserve-accuracy gain, a different kind of number from a P&L benefit), or `value_creation` (Problems 4-13 -- a real net-benefit-per-cycle figure). Two new hard-gating KPIs with no prior platform analog: `aggregation_completeness` (all 13 problems load and parse) and `aggregation_scope_correctness` (the platform total's inclusion set is provably correct -- no foundational model, reserve figure, or not-recommended system silently summed in).

Notebook 71 (Modeling -- the real BI aggregation layer itself) is shipped: builds the real executive rollup table from all 13 problems' real data, computes `TOTAL_PLATFORM_NET_VALUE_USD` as the sum of only the production-recommended `value_creation` problems' real benefit figures, and validates both hard-gating KPIs -- including a real partition-completeness proof (every problem is included exactly once, in exactly one of the included/excluded sets) and a real cross-check that Problem 7 (this platform's one built-but-not-recommended system) is correctly excluded for a genuine, data-driven reason.

Notebook 72 (Validation & Deployment) is shipped: independently reproduces the entire aggregation from scratch in a fresh kernel, cross-checks the persisted table row-by-row, re-validates both hard-gating KPIs fresh, and generates a real, auth-protected FastAPI **lookup** service (`GET /executive-summary`, `GET /problem/{problem_number}`) serving the precomputed rollup -- reusing Problems 12/13's precomputed-lookup architecture, since this is a BI aggregation artifact, not a live model.

Notebook 73 (Financial Impact, Reporting & Packaging -- the grand finale) is shipped: prices this problem's own genuinely new, additive claim -- **executive decision-latency reduction** (real time saved reviewing one unified dashboard vs. 13 separate reports, a different constituency's time than any prior problem priced) -- performs a **fourth** independent reproduction by live-driving the deployed service, and builds a real risk-profitability portfolio map (Problem 12's `UNIFIED_RISK_GRADE` crossed with Problem 13's `PROFITABILITY_TIER` on the real persisted data -- the honest analog to a geographic map, since this dataset carries no real location field). Packages a 7-tab interactive HTML executive dashboard with real functional phase/category/status filters on the Problem Registry, a real HTML/CSS heat-grid map, a live financial calculator, a comprehensive Word report, and a 7-sheet Excel workbook with real AutoFilter tables and conditional-formatting color scales.

This completes Problem 14, Phase 5, and the entire 14-problem, 5-phase platform end to end (Notebooks 1-73), run successfully by the user with real results synced above.

## Project Structure

```
Problem14_Executive_Decision_Support_Dashboard/
├── artifacts/
├── data/
├── docs/
├── models/
├── notebooks/
│   ├── 70_executive_dashboard_business_understanding.ipynb
│   ├── 71_executive_dashboard_modeling.ipynb
│   ├── 72_executive_dashboard_validation_deployment.ipynb
│   └── 73_executive_dashboard_financial_impact_reporting_packaging.ipynb
├── reports/
├── src/
│   └── docker/
├── tests/
└── LICENSE
```

## License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
