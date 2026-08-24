# Model Card -- Early Payment Default Detection

## Model details

- **Model:** XGBoost, same architecture and hyperparameters as Problem 1's champion (`n_estimators=400, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, tree_method="hist"`), retrained on a feature set restricted to each customer's first K=3 chronological statements.
- **Random seed:** 42 (fixed platform-wide).
- **Trained by:** `35_early_payment_default_modeling.ipynb`, deterministically reproduced by `36_early_payment_default_validation_deployment.ipynb`.
- **Metric definition:** the official AMEX competition metric (0.5 x Normalized Weighted Gini + 0.5 x Top-4% Capture Rate), identical implementation to Problem 1.

## Intended use

Score default risk for a customer using only their first 3 monthly statements, so a credit-risk team can flag and intervene on high-risk accounts months before a full-history model could score the same account. Explicitly scoped: this model assumes exactly 3 early statements are available -- accounts with more history should go to Problem 1's full-history champion instead (see the deployment limitation in `36_early_payment_default_validation_deployment.ipynb`, Section 10).

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real train customers: 367,130. Real holdout customers: 91,783.
- Real feature count at K=3: 1,804 (base stats + trend/delta + ratio + interaction terms, restricted to each customer's first 3 statements).
- Real coverage: 97.56% of customers have >= 3 statements (the remaining ~2.4% cannot be scored this early).

## Evaluation (real, measured)

- Holdout AUC: 0.9265274920113401 (96.31% retention of Problem 1's full-history 0.9620396555226549).
- Holdout AMEX metric: 0.65550906419563.
- Holdout top-4% capture rate: 0.45796516031305223.
- 95% bootstrap AUC CI (2,000 resamples): [0.9247892198513004, 0.9281912251702001].
- Mean calibration gap (predicted-PD decile vs. observed default rate): 0.002580582342769738 (target < 0.05, PASS).
- Split-half score PSI: 0.0004464256552751534 (target < 0.10, PASS).
- Live API self-test: predicted PD matched a direct computation exactly (diff 0.0) across the real holdout sample.
- **Deployment status: RECOMMENDED FOR PRODUCTION** (all validation checks passed on the real run).

## Limitations

- Scope-restricted by design: only tested at K in {3, 6, 9, 12} against Problem 1's champion ARCHITECTURE, not a full model-zoo re-tournament at each window length (an explicit, stated scope decision to avoid ~4-7x compute for a question this build isn't asking).
- Interaction-term feature selection is held fixed across all K (reuses Problem 1's real top-5-correlated columns) as an explicit ASSUMPTION, to avoid confounding "does K matter" with "did we pick different features."
- No demographic/protected-attribute data exists in this dataset (same limitation as Problem 1/2).

## How this is tested going forward

`tests/` drives the REAL trained model end-to-end via the FastAPI `TestClient` (not a synthetic fixture -- this problem's model is small enough to ship in this repository), covering `/health`, `/model-info`, and `/score` against the real preprocessing artifacts.
