# Models

Trained model binaries are intentionally **excluded from this GitHub package** by default (the size-safety policy caps any single packaged file at 20.0 MB) -- regenerate them by running `05_model_development.ipynb` and `09_mlops.ipynb` locally against the real Kaggle data.

## Registered model versions (real, from Notebook 09's model registry)

| Model | Version | Registered (UTC) | Holdout AUC | Holdout AMEX Metric |
|---|---|---|---|---|
| xgboost | 1 | 2026-08-23T16:43:28.007715+00:00 | 0.9620396555226549 | 0.7935631597243085 |
