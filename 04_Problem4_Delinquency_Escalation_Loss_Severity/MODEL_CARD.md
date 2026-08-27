# Model Card -- Delinquency Escalation / Loss Severity

## Model details

- **Model type:** Weighted linear severity score (243 real correlation-filtered D_* engineered features, z-scored, correlation-weighted, direction-signed), bucketed into 3 tiers via 2 real cutpoints.
- **Tiers (measured):** Low Severity (LGD 0.3015), Moderate Severity (LGD 0.45), Severe (LGD 0.648).
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `26_lgd_policy.ipynb` -> `29_financial_impact_reporting_packaging.ipynb`.
- **Summation order:** iterates `sorted(bundle["features"])` (alphabetical) -- must match Notebook 27's own real computation order exactly; a real bug was found and fixed where the deployed scorer's saved-CSV row order (weight-sorted for display) drifted from this, flipping tier assignment for accounts within float-epsilon of a cutpoint. See CHANGELOG / project history.

## Intended use

Assign a severity tier and corresponding LGD to each customer, replacing Problem 1's single flat 45% LGD, so provisioning (Problem 3) and collections prioritization reflect real severity variation rather than a single average.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real holdout customers scored: 91,783.
- Real features used: 243 (correlation-filtered D_* engineered columns from Problem 1's Notebook 03).

## Evaluation (real, measured)

- Severe-to-Low observed default-rate ratio: 48.65931445603577x (monotonicity validated).
- Chi-square (tier vs. actual default): p = 0.0. Cramer's V: 0.6415662408634579. Z-test: p = 0.0.
- Split-half score PSI: 6.8687392670068315e-06 (stable).
- Standalone `severity_scorer.py` self-test against the full real holdout: 91,783/91,783 checked, 0 hard mismatches, 0 boundary ties, 0.0% boundary-tie rate.

## Limitations

- Weights/cutpoints are fit once on this dataset's real correlation structure -- not re-validated against an external portfolio.
- No demographic/protected-attribute data exists in this dataset, so this severity score has not been fairness-audited by protected attribute (same limitation as Problem 1/2).
- LGD-by-tier values feed directly into Problem 3's ECL calculation and Problem 4's own financial-impact report -- both should be re-run together if this scorer is ever retrained, to avoid the two silently disagreeing (the architectural fix applied after the real weight-rounding bug found in this problem's history).

## How this is tested going forward

`tests/` covers `severity_scorer.py`'s `score_customer()` against the real, measured `severity_scoring_bundle.json` -- tier-boundary behavior, missing-value handling (None and NaN), and full-precision weight/mean/std consumption. `tests/test_severity_scoring_service.py` additionally covers the deployable API below end-to-end, including that omitted features are imputed identically through the live HTTP path as through direct calls.

## Deployment

`src/severity_scoring_service.py` wraps `score_customer()` as a FastAPI service (`GET /health`, `GET /model-info`, `POST /score`, accepting any subset of the 243 real features -- missing ones are imputed to their real training mean). The real `severity_scoring_bundle.json` ships alongside it in `src/`, fully self-contained. Run locally with `uvicorn severity_scoring_service:app --port 8004` from `src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```
