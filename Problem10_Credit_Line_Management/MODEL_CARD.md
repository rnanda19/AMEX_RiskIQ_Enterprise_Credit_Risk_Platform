# Model Card -- Credit Line Management

## Model details

- **Technique:** a rule-based composition of two real, already-validated Problem 6 dynamic-PD reads for the same customer -- the current real trailing window and an immediately-preceding, non-overlapping real trailing window (same model, two time points) -- into a risk-level x trend 3x3 action-tier matrix. Not a trained classifier itself. (Redefined 2026-08-27: the original version composed Problem 1's static PD with Problem 6's dynamic PD; see the 2026-08-27 addendum below.)
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `55_credit_line_management_modeling.ipynb`, validated by `56_credit_line_management_validation_deployment.ipynb`.
- **Frozen policy:** real cutpoints and the real action-tier matrix are frozen in `docs/credit_line_deployment_policy.json` (also shipped self-contained in `src/`).

## Intended use

Compose a customer's real current dynamic PD and real immediately-preceding dynamic PD (same Problem 6 model, two time points) into a risk-level (Low/Medium/High) x trend (Better/Stable/Worse) classification and recommend a real credit-line action (e.g. increase, hold, reduce) for a credit-line management operations team.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real eligible population (original definition): 447,695. Real trend-eligible population (2026-08-27 redefinition, requires 2x Problem 6's winning window in real statements): 432,573.
- This dataset has no true credit-limit or balance-to-limit utilization field; "trend" is honestly
  reinterpreted as `PD_TREND = DYNAMIC_PD (current, real) - DYNAMIC_PD_EARLY (same Problem 6 model,
  real, immediately-preceding non-overlapping window)` for the same customer, documented explicitly
  in the deployment policy rather than silently assumed.

## Evaluation (real, measured)

**2026-08-27 addendum -- root cause found, PD_TREND redefined, real partial improvement:** the
original `PD_TREND = DYNAMIC_PD - STATIC_PD` definition was a cross-model residual -- Problem 1's
STATIC_PD model has a real holdout AUC of 0.9620, higher than Problem 6's real DYNAMIC_PD holdout AUC
of 0.9541, so it mostly re-exposed the stronger model's own signal, inverted. Redefined as a genuine
same-model, two-time-point trend (DYNAMIC_PD minus DYNAMIC_PD_EARLY). Real re-run of Notebooks 54-55
with this fix: risk-level monotonicity still **PASSED** (483.36x ratio, improved from 461.02x); trend
coherence **still FAILED overall**, but the High Risk tier -- the worst offender before, at a -21 point
real gap -- now genuinely passes; minimum tier population **still FAILED**, and got worse: the (Low
Risk, Trending Worse) cell shrank to just 7 real customers (from 432), and a new undersized cell
appeared, (High Risk, Stable) at 852. Notebooks 56/57 (deployment reproduction, financial impact) are
updated to match this redefinition but have not yet been re-run with real data to produce a final,
consistent deployment artifact -- the figures immediately below are from the prior (pre-redesign) run.

- Risk-level monotonicity (reproduced, pre-redesign run): strictly increasing, top-to-bottom default-rate ratio
  461.02x (Low 0.15% -> Medium 7.10% -> High 69.78%) -- **PASSED**.
- Trend coherence (reproduced, pre-redesign run): **FAILED** -- 0 of 3 real trend-coherence cells passed.
- Minimum tier population (reproduced, pre-redesign run): **FAILED** -- the (Low Risk, Trending Worse) cell has only
  432 real customers, under the minimum-tier-population threshold.
- Dynamic PD ROC-AUC (Problem 6, inherited): 0.9541.
- **Deployment status: NOT RECOMMENDED FOR PRODUCTION** -- real hard-gate KPIs failed on both the
  original run and the redesigned run (see addendum above). Reported honestly rather than rounded up;
  this is the one system in the platform's 9-problem value-creation total that is deliberately excluded
  for exactly this reason (see `Executive_Rollup_Report/` and the root `README.md`'s
  Platform-at-a-Glance table).

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
