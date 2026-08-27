import numpy as np
import pytest
from fastapi.testclient import TestClient

AUTH = {"X-API-Key": "pytest-only-test-key"}  # must match conftest.py's TEST_API_KEY


def _at_median_payload(preprocessing_artifacts):
    """One synthetic customer built from the real, measured feature medians -- exercises the
    full real preprocessing + real trained W=3 model path, not a mocked response."""
    return {col: float(preprocessing_artifacts["feature_medians"].get(col, 0.0)) for col in
            preprocessing_artifacts["all_feature_cols"]}


def test_health_reports_the_real_trailing_window_w(dbs_app):
    client = TestClient(dbs_app.app)
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["trailing_window_w"] == 3


def test_model_info_reports_the_real_measured_metrics(dbs_app):
    client = TestClient(dbs_app.app)
    resp = client.get("/model-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["trailing_window_w"] == 3
    assert body["recommended_for_production"] is True
    assert 0.0 < body["holdout_auc"] < 1.0
    assert body["holdout_auc"] == 0.9540951936013714


def test_model_info_without_api_key_is_rejected(dbs_app):
    client = TestClient(dbs_app.app)
    resp = client.get("/model-info")
    assert resp.status_code == 401


def test_score_returns_a_valid_probability_using_the_real_trained_model(dbs_app, preprocessing_artifacts):
    client = TestClient(dbs_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    resp = client.post("/score", json=payload, params={"customer_id": "TEST-CUSTOMER-001"}, headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == "TEST-CUSTOMER-001"
    assert 0.0 <= body["predicted_pd"] <= 1.0
    assert body["trailing_window_w"] == 3


def test_score_without_api_key_is_rejected(dbs_app, preprocessing_artifacts):
    client = TestClient(dbs_app.app)
    resp = client.post("/score", json=_at_median_payload(preprocessing_artifacts))
    assert resp.status_code == 401


def test_score_returns_top_reasons_that_explain_the_prediction(dbs_app, preprocessing_artifacts):
    client = TestClient(dbs_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    feat = preprocessing_artifacts["all_feature_cols"][0]
    payload[feat] = float(payload[feat]) + 1000.0
    resp = client.post("/score", json=payload, headers=AUTH)
    assert resp.status_code == 200
    reasons = resp.json()["top_reasons"]
    magnitudes = [abs(r["contribution_to_predicted_pd"]) for r in reasons]
    assert magnitudes == sorted(magnitudes, reverse=True)
    assert len(reasons) <= 3


def test_score_is_deterministic_for_the_same_real_input(dbs_app, preprocessing_artifacts):
    client = TestClient(dbs_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    pd_1 = client.post("/score", json=payload, headers=AUTH).json()["predicted_pd"]
    pd_2 = client.post("/score", json=payload, headers=AUTH).json()["predicted_pd"]
    assert pd_1 == pd_2


def test_score_matches_a_direct_computation_against_the_same_real_model(dbs_app, preprocessing_artifacts):
    """Build the feature vector exactly as the service does, score it directly with the real
    loaded model, and require the API's answer to match exactly."""
    client = TestClient(dbs_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    api_pd = client.post("/score", json=payload, headers=AUTH).json()["predicted_pd"]

    all_feature_cols = preprocessing_artifacts["all_feature_cols"]
    feature_medians = preprocessing_artifacts["feature_medians"]
    x = np.zeros((1, len(all_feature_cols)), dtype=np.float32)
    for i, col in enumerate(all_feature_cols):
        val = payload.get(col)
        x[0, i] = val if val is not None else feature_medians[col]
    direct_pd = float(dbs_app.model.predict_proba(x)[:, 1][0])

    assert api_pd == pytest.approx(direct_pd, abs=1e-9)


def test_missing_optional_fields_fall_back_to_real_medians_without_error(dbs_app):
    """Every field is Optional in the real schema -- an empty payload must not 500."""
    client = TestClient(dbs_app.app)
    resp = client.post("/score", json={}, headers=AUTH)
    assert resp.status_code == 200
    assert 0.0 <= resp.json()["predicted_pd"] <= 1.0
    assert resp.json()["top_reasons"] == []
