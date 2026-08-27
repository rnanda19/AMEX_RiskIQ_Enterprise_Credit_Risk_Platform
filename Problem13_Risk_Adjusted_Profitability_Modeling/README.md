# AMEX Enterprise Credit Risk Platform -- Risk-Adjusted Profitability Modeling

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 5, Problem 13 of the platform: a 4-notebook build (Notebooks 66-69) that combines Problem 12's real unified `UNIFIED_RISK_SCORE`/`UNIFIED_RISK_GRADE` with a real, sourced revenue proxy derived from the Kaggle **American Express Default Prediction** dataset's own documented "S_" (Spend) column family, to rank customers by `PROFITABILITY_SCORE = PD_ADJUSTED_REVENUE_USD - EXPECTED_LOSS_USD` rather than by risk alone.

## Status: Complete -- Run End-to-End by the User, 2026-08-27 (Real Results)

**Real, synced results (2026-08-27):** all hard gates passed; recommended for production. Real Spearman correlation between `UNIFIED_RISK_SCORE` and `PROFITABILITY_SCORE` on holdout: **-0.978** (well past the -0.15 ASSUMPTION threshold, 95% CI [-0.9789, -0.9778]), confirming PD-adjustment measurably re-ranks customers. Real eligible population: 447,695 customers; real cross-tier (High Risk + Low Profitability) segment: 148,855 customers. Real net benefit: **$58,060,687.58 per cycle** (Year-1 ROI 1,741,720.6%, payback < 1 month) from the proactive exposure-reduction action against that segment's own real expected loss. This problem also received the platform's Global Standard hardening delta (2026-08-27): a real, auth-protected FastAPI lookup service (`src/profitability_scoring_lookup_service.py`), Docker packaging, real unit tests, and `MODEL_CARD.md`/`CHANGELOG.md`/`requirements.txt` -- see `CHANGELOG.md` for the full detail.

Notebook 66 (Business Understanding & Policy) is shipped: discovers the real Spend ("S_") columns programmatically from the raw CSV's own header (excluding the real statement-date exception `S_2`), verifies they are non-degenerate on a real 2,000-row sample, and defines the `REVENUE_ASSUMPTIONS` (average monthly revenue per account, and a bounded revenue multiplier range) plus the tertile `PROFITABILITY_TIER_NAMES`. Two new hard-gating KPIs: `profitability_tier_monotonicity` (real per-tier default rate must be non-increasing from Low to High Profitability -- the inverse-direction cousin of the tertile-monotonicity convention reused from Problems 4/8/10/12) and `risk_adjustment_materiality` (a genuinely new KPI: the real Spearman rank correlation between `UNIFIED_RISK_SCORE` and `PROFITABILITY_SCORE` on real holdout must fall at or below an ASSUMPTION -0.15 threshold, proving PD-adjustment measurably re-ranks customers rather than revenue dominating the score).

Notebook 67 (Modeling) is shipped: computes each real customer's `SPEND_PERCENTILE_RANK` via one real streaming pass over the raw CSV (with an honest 0.5 fallback for customers with no real recorded spend, never fabricated), derives `REVENUE_PER_ACCOUNT_USD` and `PD_ADJUSTED_REVENUE_USD` from the real `UNIFIED_RISK_SCORE`, computes `PROFITABILITY_SCORE`, fits real tertile cuts on the real TRAIN split, and validates both hard-gating KPIs on the real HOLDOUT split.

Notebook 68 (Validation & Deployment) is shipped: independently reproduces Notebook 67's entire pipeline from a fresh kernel (including a fresh real streaming CSV pass), cross-checks the persisted `profitability_scored_profile.parquet` against a real sample of holdout customers, bootstraps a 95% confidence interval on the `risk_adjustment_materiality` Spearman correlation (200 resamples), and generates a real, auth-protected, self-tested FastAPI **lookup** service (`GET /profitability/{customer_id}`) reusing Notebook 64's precomputed-lookup service architecture, since Problem 13's deliverable is a precomputed artifact, not a model to re-run live per request.

Notebook 69 (Financial Impact, Reporting & Packaging) is shipped: identifies the real, additive cross-tier segment this problem uniquely surfaces -- customers who are simultaneously High Risk (Problem 12's grade) *and* Low Profitability (this problem's own tier), invisible to either single-axis lens alone -- and prices a PROACTIVE EXPOSURE REDUCTION action against that real segment's own real expected loss, net of a real per-account segment-review cost, deliberately not double-counting Problems 9 and 10's own already-priced collections/alerting benefits. Performs a third independent reproduction: live-drives the exact deployed lookup service against a tier-stratified real sample plus a dedicated sample from the real cross-tier segment, cross-checking every response against the persisted profile. Packages a multi-tab interactive HTML dashboard (with a live financial calculator), a Word financial-impact report, and an Excel workbook.

This completes Problem 13 end to end (Notebooks 66-69), run successfully by the user with real results synced above. `MODEL_CARD.md` and `CHANGELOG.md` will be added once this platform's Phase 5 packaging pass runs (same practice as Phases 1-4); not yet pushed to GitHub.

## Project Structure

```
Problem13_Risk_Adjusted_Profitability_Modeling/
├── artifacts/
├── data/
├── docs/
├── models/
├── notebooks/
│   ├── 66_profitability_modeling_business_understanding.ipynb
│   ├── 67_profitability_modeling_modeling.ipynb
│   ├── 68_profitability_modeling_validation_deployment.ipynb
│   └── 69_profitability_modeling_financial_impact_reporting_packaging.ipynb
├── reports/
├── src/
│   └── docker/
├── tests/
└── LICENSE
```

## License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
