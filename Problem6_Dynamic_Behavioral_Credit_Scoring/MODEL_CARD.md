# Model Card -- Dynamic / Behavioral Credit Scoring

## Model details

- **Model:** XGBoost, same architecture class as Problem 1's champion, retrained on a feature set restricted to each customer's trailing (most recent) W=3 chronological statements.
- **Random seed:** 42 (fixed platform-wide).
- **Trained by:** `39_dynamic_behavioral_scoring_modeling.ipynb`, validated by `40_dynamic_behavioral_scoring_validation_deployment.ipynb`.
- **Metric definition:** the official AMEX competition metric (0.5 x Normalized Weighted Gini + 0.5 x Top-4% Capture Rate), identical implementation to Problem 1.

## Intended use

Re-score an EXISTING account's default risk monthly using only their most recent 3 statements, so recent behavioral deterioration is caught between full-history re-scoring cycles. A recency signal complementary to Problem 1's full-history champion, not a replacement for it -- explicitly an existing-book monitoring signal, not a new-account screen (see Problem 5 for that use case).

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real train / holdout customers: same split as Problem 1.
- Trailing window candidates evaluated: 3 (winner), plus wider windows per Notebook 38's real per-customer statement-count distribution.

## Evaluation (real, measured)

- Holdout AUC-ROC (reproduced, Notebook 40): 0.9541, 95% bootstrap CI lower bound 0.9528.
- Holdout PR-AUC (reproduced): 0.8796, 95% CI lower bound 0.8759.
- Holdout AMEX competition metric (reproduced): 0.7609.
- Precision / Recall / F1 @ F1-optimal threshold (0.411): 0.7636 / 0.8385 / 0.7993.
- Mean calibration gap (predicted-PD decile vs. observed default rate): 0.0037 (target < 0.05, PASS).
- Split-half score PSI: 0.0003 (target < 0.10, PASS).
- AUC retention vs. Problem 1's full-history champion: 99.2% (target >= 80%, PASS).
- **Deployment status: RECOMMENDED FOR PRODUCTION** (all validation checks passed on the real run).

## Limitations

- Trailing-window coverage is not universal: a customer needs >= 3 statements on record to be scored this way at all (see Notebook 38's real coverage figures).
- Retrains Problem 1's champion architecture/hyperparameter class rather than re-tuning from scratch at each candidate window -- an explicit, stated scope decision (same pattern as Problem 5).
- No demographic/protected-attribute data exists in this dataset (same limitation as Problem 1/2).

## How this is tested going forward

`tests/` drives the REAL trained W=3 model end-to-end via the FastAPI `TestClient` (not a synthetic fixture -- this problem's model is small enough to ship in this repository), covering `/health`, `/model-info`, and `/score` against the real preprocessing artifacts, including a bit-exact match against direct model inference.

## Deployment

`src/dynamic_behavioral_service.py` defaults `AMEX_DBS_MODELS_DIR` to this repo's own `models/` folder (self-contained -- no local machine path needed; a hardcoded local Windows path was found and fixed here during this hardening pass, the same class of bug already fixed once for Problem 5 -- see `CHANGELOG.md`). Run locally with `uvicorn dynamic_behavioral_service:app --port 8006` from `src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```

The build context is the problem root (not `src/`), since the image needs both `src/` and the real `models/` artifacts -- see `src/docker/Dockerfile`'s header comment.
