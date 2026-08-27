# AMEX Enterprise Credit Risk Platform -- Executive Decision Support Dashboard

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 5, Problem 14 of the platform -- the grand finale: a 4-notebook build (Notebooks 70-73) that depends on **all 13 prior problems** and converts every real, already-validated model this platform has built into one executive dashboard a CRO or head of risk can act on in a single meeting, per the master execution plan's own definition ("BI aggregation layer" -> "Executive dashboard").

## Status: Code-Complete (4 of 4 notebooks shipped, not yet run end-to-end by the user)

Notebook 70 (Business Understanding & Policy) is shipped: registers every one of the 13 prior problems' own canonical summary JSON(s) (Problems 1-13, spanning Phases 1-5) into a single real registry, classifying each into `foundational_model` (Problems 1, 2 -- no standalone dollar benefit, value realized downstream), `reserve_optimization` (Problem 3 -- a reserve-accuracy gain, a different kind of number from a P&L benefit), or `value_creation` (Problems 4-13 -- a real net-benefit-per-cycle figure). Two new hard-gating KPIs with no prior platform analog: `aggregation_completeness` (all 13 problems load and parse) and `aggregation_scope_correctness` (the platform total's inclusion set is provably correct -- no foundational model, reserve figure, or not-recommended system silently summed in).

Notebook 71 (Modeling -- the real BI aggregation layer itself) is shipped: builds the real executive rollup table from all 13 problems' real data, computes `TOTAL_PLATFORM_NET_VALUE_USD` as the sum of only the production-recommended `value_creation` problems' real benefit figures, and validates both hard-gating KPIs -- including a real partition-completeness proof (every problem is included exactly once, in exactly one of the included/excluded sets) and a real cross-check that Problem 7 (this platform's one built-but-not-recommended system) is correctly excluded for a genuine, data-driven reason.

Notebook 72 (Validation & Deployment) is shipped: independently reproduces the entire aggregation from scratch in a fresh kernel, cross-checks the persisted table row-by-row, re-validates both hard-gating KPIs fresh, and generates a real, auth-protected FastAPI **lookup** service (`GET /executive-summary`, `GET /problem/{problem_number}`) serving the precomputed rollup -- reusing Problems 12/13's precomputed-lookup architecture, since this is a BI aggregation artifact, not a live model.

Notebook 73 (Financial Impact, Reporting & Packaging -- the grand finale) is shipped: prices this problem's own genuinely new, additive claim -- **executive decision-latency reduction** (real time saved reviewing one unified dashboard vs. 13 separate reports, a different constituency's time than any prior problem priced) -- performs a **fourth** independent reproduction by live-driving the deployed service, and builds a real risk-profitability portfolio map (Problem 12's `UNIFIED_RISK_GRADE` crossed with Problem 13's `PROFITABILITY_TIER` on the real persisted data -- the honest analog to a geographic map, since this dataset carries no real location field). Packages a 7-tab interactive HTML executive dashboard with real functional phase/category/status filters on the Problem Registry, a real HTML/CSS heat-grid map, a live financial calculator, a comprehensive Word report, and a 7-sheet Excel workbook with real AutoFilter tables and conditional-formatting color scales.

This completes Problem 14, Phase 5, and the entire 14-problem, 5-phase platform end to end (Notebooks 1-73, code-complete). It has not yet been run by the user and not yet pushed to GitHub -- `MODEL_CARD.md`, `CHANGELOG.md`, and this problem's real dashboard link will be filled in once the full run is synced; no figures are stated here in the meantime.

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
