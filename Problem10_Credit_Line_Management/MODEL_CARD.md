# Model Card -- Credit Line Management

## Model details

- **Technique:** a rule-based composition of two already-real, already-validated upstream signals -- Problem 1's real static PD (at origination) and Problem 6's real dynamic PD (current behavior) -- into a risk-level x trend 3x3 action-tier matrix. Not a trained classifier itself.
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `55_credit_line_management_modeling.ipynb`, validated by `56_credit_line_management_validation_deployment.ipynb`.
- **Frozen policy:** real cutpoints and the real action-tier matrix are frozen in `docs/credit_line_deployment_policy.json` (also shipped self-contained in `src/`).

## Intended use

Compose a customer's real static PD and real dynamic PD into a risk-level (Low/Medium/High) x trend (Better/Stable/Worse) classification and recommend a real credit-line action (e.g. increase, hold, reduce) for a credit-line management operations team.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real eligible population: 447,695. Train split: 358,126. Holdout split: 89,569.
- This dataset has no true credit-limit or balance-to-limit utilization field; "trend" is honestly
  reinterpreted as `PD_TREND = DYNAMIC_PD (Problem 6, current) - STATIC_PD (Problem 1, origination)`
  for the same customer, documented explicitly in the deployment policy rather than silently assumed.

## Evaluation (real, measured)

- Risk-level monotonicity (reproduced): strictly increasing, top-to-bottom default-rate ratio
  461.02x (Low 0.15% -> Medium 7.10% -> High 69.78%) -- **PASSED**.
- Trend coherence (reproduced): **FAILED** -- 0 of 3 real trend-coherence cells passed.
- Minimum tier population (reproduced): **FAILED** -- the (Low Risk, Trending Worse) cell has only
  432 real customers, under the minimum-tier-population threshold.
- Dynamic PD ROC-AUC (Problem 6, inherited): 0.9541.
- **Deployment status: NOT RECOMMENDED FOR PRODUCTION** -- 2 of 3 real hard-gate KPIs failed on
  this run. Reported honestly rather than rounded up; this is the one system in the platform's
  9-problem value-creation total that is deliberately excluded for exactly this reason (see
  `Executive_Capstone_Report/` and the root `README.md`'s Platform-at-a-Glance table).

## Limitations

- Real backtest, with confidence intervals, did not clear its own KPI bar -- see above. Not
  deployed to production in this platform's current, honest state.
- The utilization-trend reinterpretation (PD delta, not a true balance/limit ratio) is a
  documented ASSUMPTION forced by what this dataset actually contains -- see
  `utilization_trend_reinterpretation` in the deployment policy.

## How this is tested going forward

`tests/` drives the real deployed FastAPI recommendation service end-to-end via `TestClient`
against the real, measured `credit_line_deployment_policy.json` -- covering `/health`,
`/policy-info` (asserting the real, honestly NOT-recommended result), the auth gate, the real
risk-level/trend cutpoint boundaries, and the full real action-tier matrix.

## Deployment

`src/credit_line_scoring_service.py` defaults `AMEX_P10_POLICY_PATH` to the real frozen policy
JSON shipped alongside it in `src/` (self-contained -- no local machine path needed; a hardcoded
personal Windows path was found and fixed here during this hardening pass, the same class of bug
already fixed for Problems 5-9 -- see `CHANGELOG.md`). Run locally with
`uvicorn credit_line_scoring_service:app --port 8010` from `src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```

Deployed here for completeness and honest transparency, matching this platform's standard of
shipping every real result -- including the ones that did not clear their KPI bar.
