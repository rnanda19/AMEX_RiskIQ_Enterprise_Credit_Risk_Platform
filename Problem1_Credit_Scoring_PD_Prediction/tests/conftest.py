"""Pytest fixtures for the FastAPI scoring service.

The real service (src/fastapi_service/main.py) loads its config, champion
model, and preprocessing artifacts from AMEX_PROJECT_ROOT at import time.
main.py already supports overriding that root via the AMEX_PROJECT_ROOT
environment variable (documented in its own header comment) -- that hook
exists for exactly this purpose, so this fixture builds a tiny, synthetic
-but-structurally-real project tree (a genuinely fit 2-feature logistic
regression, not a mocked object) and points the service at it, rather than
requiring the real multi-GB trained artifacts to run CI.
"""
import importlib.util
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression


@pytest.fixture()
def fastapi_app(tmp_path, monkeypatch):
    project_root = tmp_path / "AMEX_Enterprise_Credit_Risk_Platform"
    artifacts_dir = project_root / "artifacts"
    model_dev_dir = project_root / "pillars" / "model_development"
    models_subdir = model_dev_dir / "models"
    models_subdir.mkdir(parents=True)
    artifacts_dir.mkdir(parents=True)

    numeric_feature_cols = ["balance", "spend_last_month"]
    categorical_encode_cols = ["region"]
    all_feature_cols = numeric_feature_cols + categorical_encode_cols

    # A genuinely fit model (2 numeric + 1 encoded categorical -> 3 columns),
    # not a stub -- predict_proba below is real sklearn inference.
    rng = np.random.default_rng(42)
    X = rng.random((50, 3))
    y = (X[:, 0] > 0.5).astype(int)
    model = LogisticRegression().fit(X, y)
    joblib.dump(model, models_subdir / "logistic_regression.joblib")

    preprocessing_artifacts = {
        "label_encoders": {"region": {"classes": ["north", "south", "__missing__"]}},
        "feature_medians": {"balance": 500.0, "spend_last_month": 120.0},
        "scaler": {"mean": np.zeros(3), "std": np.ones(3)},
        "all_feature_cols": all_feature_cols,
        "categorical_encode_cols": categorical_encode_cols,
        "numeric_feature_cols": numeric_feature_cols,
    }
    joblib.dump(preprocessing_artifacts, models_subdir / "preprocessing_artifacts.joblib")

    with open(artifacts_dir / "project_config.json", "w", encoding="utf-8") as f:
        json.dump({"pillar_dirs": {"model_development": str(model_dev_dir)}}, f)
    with open(artifacts_dir / "notebook_05_summary.json", "w", encoding="utf-8") as f:
        json.dump({
            "champion_model": "logistic_regression",
            "champion_metrics": {"holdout_auc": 0.9620396555226549, "holdout_amex_metric": 0.7935631597243085},
        }, f)

    monkeypatch.setenv("AMEX_PROJECT_ROOT", str(project_root))

    # Fresh module import each test (not the cached sys.modules copy) so it
    # re-reads AMEX_PROJECT_ROOT for this test's own tmp_path.
    main_path = (
        Path(__file__).resolve().parents[1] / "src" / "fastapi_service" / "main.py"
    )
    spec = importlib.util.spec_from_file_location("amex_fastapi_main_under_test", main_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    yield module
    del sys.modules[spec.name]
