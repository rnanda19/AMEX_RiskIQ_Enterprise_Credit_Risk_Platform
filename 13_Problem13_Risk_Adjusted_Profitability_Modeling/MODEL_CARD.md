# Model Card -- Risk-Adjusted Profitability Modeling

## Model details

- **Technique:** a real, precomputed PD-adjusted profitability score per customer: `(1 - Problem 12's real UNIFIED_RISK_SCORE) x an ASSUMPTION-scaled revenue estimate, minus expected loss (unified risk score x EAD x LGD, EAD/LGD inherited from Problem 4)`. Not a trained classifier -- a validated financial composition built on one real upstream signal plus explicit, labeled revenue assumptions.
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `67_profitability_modeling_modeling.ipynb`, validated by `68_profitability_modeling_validation_deployment.ipynb`.
- **Frozen policy:** real tier cutpoints, revenue assumptions (each individually labeled ASSUMPTION with its rationale), and reproduction metrics are frozen in `docs/profitability_deployment_policy.json` (also shipped self-contained in `src/`). The real per-customer profile (`profitability_scored_profile.parquet`) is **not** committed to this repository -- see `data/README.md`.

## Intended use

Serve each real customer's precomputed PD-adjusted profitability score and tier (Low/Medium/High Profitability) for a profitability-aware credit-risk operations view.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1), composed on top of Problem 12's real unified risk score.
- Real eligible population: 447,695. Train split: 358,126. Holdout split: 89,569.

## Evaluation (real, measured)

- Profitability-tier monotonicity (reproduced): real default rate Low Profitability 70.63% ->
  Medium 5.92% -> High 0.29% -- **PASSED**.
- Risk-adjustment materiality (reproduced): Spearman correlation between unified risk score and
  profitability score -0.9784 (p < 0.001), far past the -0.15 threshold -- **PASSED**.
- Minimum tier population (reproduced): **PASSED**, no undersized tiers.
- **Deployment status: RECOMMENDED FOR PRODUCTION** -- all 3 real hard-gate KPIs passed.
- Dollar figures rest partly on explicit ASSUMPTION revenue inputs (average monthly
  revenue-per-account $65, revenue-multiplier floor/ceiling 0.4x/1.8x by real relative spend
  rank) -- each individually labeled and editable, not silently treated as measured fact.

## Limitations

- Absolute dollar figures are only as accurate as the labeled revenue ASSUMPTIONs -- the *relative
  ranking* (Spearman -0.978) is the real, measured, high-confidence result; the *dollar scale* is
  not.
- No demographic/protected-attribute data exists in this dataset (same limitation as Problem 1/2).

## How this is tested going forward

`tests/` drives the real deployed FastAPI lookup service end-to-end via `TestClient` against a
small, synthetic-but-structurally-real profile fixture (real column names/dtypes/value ranges;
the full ~38MB real per-customer parquet is not committed) and the real, measured
`profitability_deployment_policy.json` -- covering `/health`, `/policy-info` (asserting the real
RECOMMENDED result and the labeled revenue assumptions), the auth gate, a known-customer lookup,
and the 404 path for an unknown customer.

## Deployment

`src/profitability_scoring_lookup_service.py` defaults `AMEX_P13_POLICY_PATH` to the real frozen
policy JSON shipped alongside it in `src/`, and `AMEX_P13_PROFILE_PATH` to
`../data/profitability_scored_profile.parquet` (a hardcoded personal Windows path was found and
fixed here during this hardening pass -- see `CHANGELOG.md`). Regenerate the real profile parquet
locally (see `data/README.md`) before serving real traffic. Run locally with
`uvicorn profitability_scoring_lookup_service:app --port 8013` from `src/`, or build the container
(the real profile parquet is mounted at runtime, not baked into the image):

```bash
cd src/docker
docker compose up --build
```
