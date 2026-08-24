"""Pytest fixture for the risk-tier FastAPI service -- same pattern as
Problem1_Credit_Scoring_PD_Prediction/tests/conftest.py (see that file's
docstring for why AMEX_PROJECT_ROOT override + a genuinely-fit tiny model
is used instead of mocking). This fixture additionally writes a
risk_tier_policy.json using Problem 2's REAL band thresholds (copied from
docs/risk_tier_policy.json's business_rule method), so tier assignment in
these tests reflects the actual deployed policy, not an invented one.
"""
import importlib.util
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression

REAL_BUSINESS_RULE_THRESHOLDS = [
    {"risk_tier": "Prime", "tier_order": 1, "pd_lower": 0.0, "pd_upper": 0.05},
    {"risk_tier": "Near-Prime", "tier_order": 2, "pd_lower": 0.05, "pd_upper": 0.15},
    {"risk_tier": "Subprime", "tier_order": 3, "pd_lower": 0.15, "pd_upper": 0.35},
    {"risk_tier": "High Risk", "tier_order": 4, "pd_lower": 0.35, "pd_upper": 1.01},
]


@pytest.fixture()
def risk_tier_app(tmp_path, monkeypatch):
    project_root = tmp_path / "AMEX_Enterprise_Credit_Risk_Platform"
    artifacts_dir = project_root / "artifacts"
    model_dev_dir = project_root / "pillars" / "model_development"
    models_subdir = model_dev_dir / "models"
    risk_tier_policy_dir = project_root / "pillars" / "risk_tier_policy"
    models_subdir.mkdir(parents=True)
    artifacts_dir.mkdir(parents=True)
    risk_tier_policy_dir.mkdir(parents=True)

    numeric_feature_cols = ["balance", "spend_last_month"]
    categorical_encode_cols = ["region"]
    all_feature_cols = numeric_feature_cols + categorical_encode_cols

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
        json.dump({
            "pillar_dirs": {
                "model_development": str(model_dev_dir),
                "risk_tier_policy": str(risk_tier_policy_dir),
            }
        }, f)
    with open(artifacts_dir / "notebook_05_summary.json", "w", encoding="utf-8") as f:
        json.dump({
            "champion_model": "logistic_regression",
            "champion_metrics": {"holdout_auc": 0.9620396555226549, "holdout_amex_metric": 0.7935631597243085},
        }, f)
    with open(risk_tier_policy_dir / "risk_tier_policy.json", "w", encoding="utf-8") as f:
        json.dump({
            "n_tiers": 4,
            "tier_order": ["Prime", "Near-Prime", "Subprime", "High Risk"],
            "primary_method": "business_rule",
            "bucketing_methods": {"business_rule": {"pd_thresholds": REAL_BUSINESS_RULE_THRESHOLDS}},
        }, f)

    monkeypatch.setenv("AMEX_PROJECT_ROOT", str(project_root))

    service_path = (
        Path(__file__).resolve().parents[1] / "src" / "fastapi_service" / "risk_tier_service.py"
    )
    spec = importlib.util.spec_from_file_location("amex_risk_tier_service_under_test", service_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    yield module
    del sys.modules[spec.name]
