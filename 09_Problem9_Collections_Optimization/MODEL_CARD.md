# Model Card -- Collections Optimization

## Model details

- **Technique:** a real, trained XGBoost binary classifier (`collections_propensity_xgboost.joblib`) predicting propensity-to-cure on a customer's current statement, composed with a treatment-tier rule.
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `51_collections_optimization_modeling.ipynb`, validated by `52_collections_optimization_validation_deployment.ipynb`.
- **Frozen policy:** real feature weights/means, tier cutpoints, and reproduction metrics are frozen in `docs/collections_deployment_policy.json` (also shipped self-contained in `src/`, alongside the trained model itself).

## Intended use

Score a customer's current statement for propensity-to-cure (returning to current from a delinquent/severe state) and recommend a real treatment tier (Priority Outreach / Automated Nudge / Monitor) for a collections operations team.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real train-eligible statements: 2,699,966. Real holdout-eligible statements: 677,582.
- Real train cure rate: 5.32%. Real holdout cure rate: 5.28%.

## Evaluation (real, measured)

- Holdout ROC-AUC (reproduced, bit-identical): 0.8236 (target >= 0.60, PASS).
- Holdout PR-AUC (reproduced): 0.2655.
- Metrics at the real F1-optimal threshold (0.1554): accuracy 0.9185, precision 0.2933, recall 0.3856, F1 0.3332, specificity 0.9482, MCC 0.2937.
- Treatment tier population split (real): Automated Nudge 338,791 / Priority Outreach 261,281 / Monitor 77,510.
- **Deployment status: RECOMMENDED FOR PRODUCTION** -- reproduction passed and the persisted model was independently re-verified against its reported holdout metric.

## Limitations

- The class is rare (~5% real cure rate), so precision at the F1-optimal threshold is modest (0.29) -- appropriate for a triage/prioritization tool, not a hard accept/reject gate.
- The deployed API's `/score` endpoint tiers using a fixed 0.5 propensity reference rather than Notebook 51's live population-median split -- a real, documented known gap (a batch-scoring endpoint that reuses the real measured median is the honest way to reproduce the exact tier split; a single stateless call cannot see the live population).
- No demographic/protected-attribute data exists in this dataset (same limitation as Problem 1/2).

## How this is tested going forward

`tests/` drives the real deployed FastAPI scoring service end-to-end via `TestClient`, loading the real trained model and real frozen policy shipped in `src/` -- covering `/health`, `/model-info` (asserting the real RECOMMENDED result), the auth gate, and `/score` against real feature-mean baselines with exact reproduction of the model's own `predict_proba` output and occlusion-based reason codes.

## Deployment

`src/collections_scoring_service.py` defaults `AMEX_P9_POLICY_PATH` / `AMEX_P9_MODEL_PATH` to the real frozen policy JSON and real trained model shipped alongside it in `src/` (self-contained -- no local machine path needed; a hardcoded personal Windows path was found and fixed here during this hardening pass, the same class of bug already fixed for Problems 5, 6, 7, 8 -- see `CHANGELOG.md`). Run locally with `uvicorn collections_scoring_service:app --port 8009` from `src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```
