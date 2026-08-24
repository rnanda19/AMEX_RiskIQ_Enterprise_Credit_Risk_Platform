# Models

Unlike Problem 1/2's full-size champion model (excluded by this package's 20MB size-safety cap), this problem's K=3 model and its preprocessing artifacts are both small enough to include directly.

| File | Size | Description |
|---|---|---|
| `early_default_xgboost_k3.joblib` | ~1.9 MB | The real, trained XGBoost model (K=3 early window), same architecture as Problem 1's champion. |
| `preprocessing_artifacts.joblib` | ~84 KB | Label encoders, feature medians, and column lists needed to preprocess a raw customer record before scoring. |

## Registered result (real, from Notebook 36's real run)

| Model | Window K | Holdout AUC | Holdout AMEX Metric | Recommended for Production |
|---|---|---|---|---|
| xgboost | 3 | 0.9265274920113401 | 0.65550906419563 | True |

`tests/` loads these exact files (via `AMEX_EPD_MODELS_DIR`) and drives the real FastAPI service end-to-end.
