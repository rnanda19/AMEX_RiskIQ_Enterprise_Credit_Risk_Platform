# Model Card -- 360 Degree Customer Intelligence

## Model details

- **Technique:** a real, precomputed composite ("unified risk score") combining Problem 1's real static PD (35% weight), Problem 6's real dynamic PD (65% weight), and, where the customer is collections-eligible, Problem 9's real propensity-to-cure (10% weight, renormalized) -- not a newly trained classifier; a validated composition of already-real signals.
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `63_customer_intelligence_modeling.ipynb`, validated by `64_customer_intelligence_validation_deployment.ipynb`.
- **Frozen policy:** real composite weights, grade cutpoints, and reproduction metrics are frozen in `docs/customer_intelligence_deployment_policy.json` (also shipped self-contained in `src/`). The real per-customer profile (`unified_customer_profile.parquet`) is **not** committed to this repository -- see `data/README.md`.

## Intended use

Serve each real customer's precomputed unified risk score/grade -- a single 360-degree view composed from four upstream signals -- for a customer-intelligence lookup UI or downstream system.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real eligible population: 447,695 (303,660 collections-eligible). Train split: 358,126. Holdout split: 89,569.

## Evaluation (real, measured)

- Composite non-inferiority (reproduced): unified ROC-AUC 0.9590 vs. best single signal (static PD)
  0.9626 -- gap within the real 95% CI [-0.00404, -0.00322], well inside the +/-0.005 tolerance --
  **PASSED**.
- Unified metrics at the real F1-optimal threshold: accuracy 0.8986, precision 0.7723, recall
  0.8599, F1 0.8137, specificity 0.9121, MCC 0.7464.
- Profile completeness (reproduced): zero real nulls across every composite field -- **PASSED**.
- Minimum tier population (reproduced): **PASSED**, no undersized grades.
- **Deployment status: RECOMMENDED FOR PRODUCTION** -- all 3 real hard-gate KPIs passed.

## Limitations

- The composite score is validated to be statistically non-inferior to its single best input
  (static PD), not proven strictly superior -- its value is in unifying four signals into one
  interpretable view, not in raising discrimination.
- Where a customer has no real collections propensity-to-cure (not collections-eligible), the
  composite honestly excludes that term rather than imputing a value.

## How this is tested going forward

`tests/` drives the real deployed FastAPI lookup service end-to-end via `TestClient` against a
small, synthetic-but-structurally-real profile fixture (same real column names/dtypes/value
ranges as the real parquet -- see `tests/conftest.py`; the full ~29MB real per-customer parquet is
not committed, matching this repo's established data-size convention) and the real, measured
`customer_intelligence_deployment_policy.json` -- covering `/health`, `/policy-info` (asserting
the real RECOMMENDED result), the auth gate, a known-customer lookup, the collections-vs-not
branch, and the 404 path for an unknown customer.

## Deployment

`src/customer_intelligence_lookup_service.py` defaults `AMEX_P12_POLICY_PATH` to the real frozen
policy JSON shipped alongside it in `src/`, and `AMEX_P12_PROFILE_PATH` to `../data/unified_customer_profile.parquet`
(a hardcoded personal Windows path was found and fixed here during this hardening pass, the same
class of bug already fixed for Problems 5-10 -- see `CHANGELOG.md`). Regenerate the real profile
parquet locally (see `data/README.md`) before serving real traffic. Run locally with
`uvicorn customer_intelligence_lookup_service:app --port 8012` from `src/`, or build the
container (the real profile parquet is mounted at runtime, not baked into the image):

```bash
cd src/docker
docker compose up --build
```
