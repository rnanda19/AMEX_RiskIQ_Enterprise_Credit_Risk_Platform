# AMEX Enterprise Credit Risk Platform -- Expected Credit Loss (IFRS9/CECL)

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 2, Problem 3 of a 14-problem enterprise credit risk platform: a **4-notebook** build (Notebooks 30-33) that computes real, dual-standard (IFRS9 and CECL) Expected Credit Loss for every holdout customer, using an outcome-free staging rubric built only from Problem 1's real PD and Problem 4's real severity tier -- never the known target. Depends on Problem 1 (champion PD model) and Problem 4 (tier-differentiated LGD).

## 1. Overview

- **Champion PD model reused (measured, Problem 1):** xgboost
- **Holdout customers scored (measured):** 91,783
- **IFRS9 stage counts (measured):** Stage 1: 30,281 -- Stage 2: 40,277 -- Stage 3: 21,225
- **Total ECL, IFRS9 (measured):** $72,448,498.95
- **Total ECL, CECL (measured):** $73,051,922.57
- **Total ECL, Notebook 08 flat-LGD baseline (measured):** $67,830,905.87

## Live Dashboard

- 📊 [ECL Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/Problem3_Expected_Credit_Loss_IFRS9_CECL/reports/financial_impact_reporting_packaging/ecl_financial_impact_dashboard.html) — interactive IFRS9/CECL reserve-change and stress-buffer dashboard

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

## 2. Problem Statement

A single flat LGD assumption (Problem 1's Notebook 08) understates loss provisioning for higher-severity accounts and overstates it for lower-severity ones. This build computes a real, dual-standard (IFRS9-staged and CECL lifetime) Expected Credit Loss figure per customer, using Problem 4's real tier-differentiated LGD instead of one flat number, and an outcome-free staging rubric (SICR/Stage 2 and credit-impaired/Stage 3 triggers computed only from real PD + real severity tier, never the known default outcome).

## 3. Approach & Methodology

Notebook 30 (Business Understanding & ECL Policy -- defines the outcome-free staging rubric, reads LGD-by-tier from Problem 4, sets lifetime-PD multiplier / discount-rate / macro-scenario-weight ASSUMPTIONs) -> Notebook 31 (ECL Modeling -- scores real live PD, joins Problem 4's real severity tier, applies the staging rubric, computes IFRS9 and CECL ECL, hard-validates stage monotonicity against real observed default rate) -> Notebook 32 (Statistical Validation, Macro Sensitivity & Deployment -- chi-square/z-test/bootstrap-CI/split-half-PSI validation, per-scenario macro-ECL sensitivity, a standalone `ecl_calculator.py` verified via an all-customer boundary-tie-aware self-test) -> Notebook 33 (this packaging notebook).

## 4. Key Results (Real, Measured)

- Chi-square (IFRS9 stage vs. actual default), p-value: 0.0
- Cramer's V (effect size): 0.7289977841059684
- Z-test p-value: 0.0
- Split-half score PSI: 1.278534602748648e-05 (stable)
- Standalone `ecl_calculator.py` self-test: 91,783/91,783 customers checked, 0 hard mismatches, 0 boundary ties
- Macro-scenario ECL sensitivity range (measured): $62,509,011.41 -- $77,255,633.18
- Reserve change, IFRS9 vs. flat-LGD baseline (measured): +$4,617,593.08
- CECL vs. IFRS9 delta (measured): +$603,423.62
- Macro stress capital buffer (measured, Downside minus Baseline): $3,715,619.76
- Efficiency-only Year-1 ROI / payback (measured, deliberately excludes the reserve-change dollars -- a provisioning change is a capital decision, not free cash): 42.9% / 8.4 months

## 5. Repository Structure

```
Problem3_Expected_Credit_Loss_IFRS9_CECL/
|-- notebooks/          4 notebooks (30-33), one markdown intro + one consolidated code cell each
|-- src/                ecl_calculator.py -- standalone deployable ECL scorer (deterministic, no training)
|-- reports/            real Word reports, Excel workbook, HTML dashboard, charts, per-notebook CSVs
|-- artifacts/          real notebook_30-33_summary.json + project_config.json (all real, measured values)
|-- docs/                ecl_policy.json (the real, frozen policy), stakeholder analysis
|-- data/                see data/README.md -- raw Kaggle data is not redistributed
|-- models/              see models/README.md -- this problem has no trained ML model of its own
`-- tests/               pytest coverage for ecl_calculator.py against the real, measured scoring bundle
```

## 6. Deployable Scorer

`src/ecl_calculator.py` computes IFRS9-staged and CECL ECL for one customer given their real PD (from Problem 1's deployed model) and real severity tier (from Problem 4's deployed model), loading every parameter from `reports/validation_deployment/ecl_scoring_bundle.json` (frozen from Notebook 30's real policy -- no training or threshold-fitting happens in this file). See `tests/` for a real, passing self-test driven from that same bundle.

The deployed `ecl_scoring_service.py` API requires a valid `X-API-Key` header on every endpoint except `/health` (see `.env.example`), and its `/score` response includes a real `top_reasons` field -- an exact narration of which IFRS9-stage rule fired and which frozen LGD value drove the ECL amount (see `CHANGELOG.md`).

## 7. Reproducing This

Raw Kaggle data is not redistributed here (see `data/README.md`). To reproduce: run Problem 1's Notebooks 01-05 (champion PD model), Problem 4's Notebooks 26-27 (tier-differentiated LGD), then this problem's Notebooks 30-33 in order against your own local copy of the platform folder.

## 8. Zero-Fabrication Statement

Every number in this README and this problem's reports is computed live by that notebook's own code on the real dataset. Anything without ground truth in the data (lifetime-PD multiplier, discount rates, macro-scenario weights, financial-impact assumptions) is an explicit, labeled, editable `ASSUMPTION` in `docs/ecl_policy.json` / `artifacts/p3_financial_assumptions.json` -- never silently presented as fact.

## License

See [LICENSE](LICENSE) -- All Rights Reserved. Published for portfolio/demonstration/evaluation purposes only.
