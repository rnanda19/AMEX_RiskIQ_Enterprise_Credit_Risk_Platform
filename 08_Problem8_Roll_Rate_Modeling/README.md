# AMEX Enterprise Credit Risk Platform -- Roll-Rate Modeling

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 3, Problem 8 of a 14-problem enterprise credit risk platform (the final problem of Phase 3: Behavioral Intelligence, and of this repository's push so far): a **4-notebook** build (Notebooks 46-49) that fits a real Markov transition-probability matrix across three severity states (Low / Moderate / Severe), stratified against Problem 6's dynamic PD score. Depends on Problem 1's real feature-engineering pipeline and Problem 6's real dynamic scoring output.

## 1. Overview

- **Technique (measured):** composite severity score (89 monitored features, fitted weights/directions) cut into 3 states; empirical Markov transition matrix between states across consecutive statements
- **Severe/Low default-rate ratio (reproduced):** 107.21x, 95% CI [92.78x, 125.17x]
- **Both hard-gate KPIs met (reproduced):** monotonicity (Low < Moderate < Severe default rate) and coherence (P(Severe→Severe) > P(Low→Severe))
- **Deployment status (measured):** RECOMMENDED FOR PRODUCTION

## Live Dashboard

- 📊 [Roll-Rate Financial Impact Dashboard](https://rnanda19.github.io/AMEX_RiskIQ_Enterprise_Credit_Risk_Platform/08_Problem8_Roll_Rate_Modeling/reports/financial_impact_reporting_packaging/roll_rate_financial_impact_dashboard.html) — interactive transition-matrix, escalation-validity, and financial-impact dashboard

(Served via GitHub Pages — click the link above to view it rendered in your browser. Opening the `.html` file directly in GitHub's own file browser shows raw source code instead.)

## 2. Problem Statement

Problems 6 and 7 score risk from a customer's own statement trend; this problem asks a classic credit-ops question instead -- given a customer's current delinquency-severity state, what is the real, empirically observed probability they roll to a worse state next cycle? A "roll-rate" / Markov transition view lets collections teams act on realized behavioral moves, not just point-in-time scores, and cross-validates against Problem 6's own dynamic PD as an independent stratification check.

## 3. Approach & Methodology

Notebook 46 (Business Understanding & Policy -- defines the composite severity score, state cuts, and both hard-gate KPI targets) → Notebook 47 (Modeling -- fits the real transition matrix, tests monotonicity and coherence, cross-stratifies escalation rate against Problem 6's real dynamic PD) → Notebook 48 (Validation & Deployment -- zero-randomness reproduction check, bootstrap CIs on the ratio/coherence-gap/AUC, a real FastAPI scoring service proven via a live self-test) → Notebook 49 (this pillar's packaging notebook and Phase 3 close-out -- financial-impact narrative synthesizing all three of this problem's notebooks).

## 4. Key Results (Real, Measured)

- Holdout customers scored (measured): 91,783; transition-eligible pairs: 90,783
- State population split (measured): Low Severity 31.7% / Moderate Severity 31.0% / Severe 37.4%
- Monotonic default rate across states (reproduced): True -- Low 0.57% → Moderate 9.16% → Severe 61.24%
- Severe/Low default-rate ratio (reproduced): 107.21x, 95% CI lower bound 92.78x (target ≥ 1.5x)
- Coherence gap P(Severe→Severe) − P(Low→Severe) (reproduced): 0.9557, 95% CI lower bound 0.9550 (target > 0)
- Escalation-magnitude ROC-AUC / PR-AUC (reproduced): 0.5126 / 0.2635
- Cross-validation against Problem 6's real dynamic PD (measured): escalation rate above vs. below Problem 6's median PD, z = 8.80, p < 0.001 -- statistically significant, confirming the two techniques agree independently
- Split-half severity-score PSI (measured): 0.0001 (target < 0.10)
- Real defaulters captured among 4,042 escalated accounts (measured): 933
- Estimated Net Benefit / Cycle (measured, net of false-positive review cost): $315,820

## 5. Repository Structure

```
08_Problem8_Roll_Rate_Modeling/
|-- notebooks/          4 notebooks (46-49)
|-- src/                roll_rate_scoring_service.py -- real, runnable FastAPI scoring service, plus
|                        a self-contained copy of roll_rate_deployment_policy.json
|                        src/docker/ -- Dockerfile + docker-compose.yml (port 8005)
|-- reports/            reports/modeling (results JSON + transition-matrix/escalation/default-rate
|                        charts), reports/validation_deployment (statistical validation, deployment
|                        checklist, Word report, bootstrap charts), reports/financial_impact_reporting_packaging
|                        (Excel workbook, Word report, HTML dashboard, SMART suggestions, chart)
|-- docs/                roll_rate_policy.json + roll_rate_deployment_policy.json (the real, frozen policy)
|-- data/                see data/README.md
|-- models/              no trained classifier artifacts -- this technique is a fitted composite score
|                        plus an empirical Markov transition matrix, both frozen in docs/
|-- artifacts/           reserved for future notebook_46-49_summary.json exports
`-- tests/               pytest (8 tests) -- drives the real FastAPI scoring service end-to-end
                         against the real frozen policy and transition matrix, including a
                         bit-exact match against direct computation
```

## 6. Deployable Scorer

`src/roll_rate_scoring_service.py` is a real, runnable FastAPI service that loads the frozen composite-score weights and transition matrix from `docs/` and scores a customer's current severity state and escalation status. Run it with:

```
uvicorn roll_rate_scoring_service:app --reload
```

Every endpoint except `/health` requires a valid `X-API-Key` header (see `.env.example`). `/score` also returns a real `top_reasons` field -- the exact per-feature terms (weight x direction x z-score) that drove this customer's own severity score (see `CHANGELOG.md`).

## 7. Reproducing This

Raw Kaggle data is not redistributed here (see `data/README.md`). Run Problem 1's Notebooks 01-05 first, then Problem 6's Notebooks 38-41 (this problem cross-stratifies against Problem 6's real dynamic PD output), then this problem's Notebooks 46-49, against your own local copy of the platform folder.

## 8. Zero-Fabrication Statement

Every number above is computed live by that notebook's own code on the real dataset. Financial-impact assumptions (intervention success rate, false-positive review cost, implementation cost, cycles/year) are explicit, labeled `ASSUMPTION`s in `reports/financial_impact_reporting_packaging/financial_assumptions.json`; EAD/LGD are real values inherited from Problem 1's Notebook 08. This notebook set also does not double-count reserve-timing dollars against Problem 3's ECL work -- the SMART suggestions frame that as a coordination point, not a second dollar estimate.

## 9. Hardening Status

Complete, matching the pattern already shipped for Problems 1-5: `tests/` (11 pytest tests, driven by the real frozen policy), `src/docker/` (Dockerfile + docker-compose.yml), `MODEL_CARD.md`, `CHANGELOG.md`, and `requirements.txt` are all in place -- see `CHANGELOG.md` for the real bug (a hardcoded local-path privacy leak) found and fixed; unlike Problems 6 and 7, no port reassignment was needed here since 8005 was already free. The service now also requires real API-key authentication and returns real per-request explainability (`top_reasons`) on every score -- see `CHANGELOG.md`'s 2026-08-25 "Authentication + explainability hardening" entry.

## License

See [LICENSE](LICENSE) -- All Rights Reserved. Published for portfolio/demonstration/evaluation purposes only.
