# Model Card — Risk Tier Classification

## Model details

This problem does not train its own classifier — it reuses Problem 1's
champion PD model and adds a policy layer on top (a discrete tier
assignment from the continuous PD score). See
`Problem1_Credit_Scoring_PD_Prediction/MODEL_CARD.md` for the underlying
model's own card.

- **Champion model reused (measured, from Problem 1):** XGBoost
- **Champion holdout AUC (measured, from Problem 1):** 0.9620396555226549
- **Champion holdout AMEX metric (measured, from Problem 1):** 0.7935631597243085
- **Tiers defined:** 4 (Prime, Near-Prime, Subprime, High Risk)
- **Primary bucketing method:** `business_rule` — fixed PD thresholds
  (`docs/risk_tier_policy.json`), chosen for continuity with Notebook 13's
  illustrative BI bands. A second method, `quantile` (equal-population
  quartiles of the real holdout PD distribution), is computed and compared
  but not used as the deployed default.
- **Assignment logic:** `shared/tiers.py::assign_band` (generalized from
  the service's own `assign_tier()`) — half-open interval `[pd_lower,
  pd_upper)`, sorted by `tier_order`; a PD value outside every band's range
  falls back to the highest-order (`High Risk`) band.

## Business-rule thresholds (real policy, `docs/risk_tier_policy.json`)

| Tier | PD range |
|---|---|
| Prime | [0.00, 0.05) |
| Near-Prime | [0.05, 0.15) |
| Subprime | [0.15, 0.35) |
| High Risk | [0.35, 1.01) |

## Intended use

Translate a continuous PD score into an actionable underwriting/pricing
grade, since credit policy is written in discrete risk grades, not raw
probabilities. Served in real time via
`src/fastapi_service/risk_tier_service.py` (`/risk-tier` endpoint).

## Evaluation (measured, Notebook 21)

- **Chi-square (tier vs. actual default), p-value:** 0.0
- **Cramér's V (effect size):** 0.7636626665627394
- **Fair-lending / disparate-impact testing:** Not Possible — Data
  Limitation (this Kaggle dataset carries no demographic/protected-attribute
  fields; see Notebook 21's own report for the full, honest statement
  rather than restating it here to avoid drift).

## Limitations

- The `business_rule` thresholds are an explicit `ASSUMPTION`, chosen for
  continuity with an earlier illustrative notebook's bands, not derived
  from an external regulatory or industry standard — see
  `docs/risk_tier_policy.json`'s own `description` field for each method.
- Tier population is whatever the real score distribution puts in each
  band under `business_rule` — it is not guaranteed balanced (unlike the
  `quantile` method, which guarantees equal-population quartiles by
  construction but is not the deployed default).

## How this is tested going forward

`Problem2_Risk_Tier_Classification/tests/` covers the serving path (health,
policy-info, tier assignment — including a check that the returned tier is
exactly what `shared/tiers.py::assign_band` independently computes for the
same PD, so a stale/mismatched policy would fail the test) against a small,
genuinely-fit synthetic model, same pattern as Problem 1. Re-running
`20_risk_tier_model_development.ipynb` / `21_risk_tier_validation.ipynb`
against the real dataset remains the only source of truth for the
evaluation numbers on this card.
