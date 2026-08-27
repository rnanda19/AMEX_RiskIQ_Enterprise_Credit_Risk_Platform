import numpy as np
import pytest
from fastapi.testclient import TestClient

AUTH = {"X-API-Key": "pytest-only-test-key"}  # must match conftest.py's TEST_API_KEY


def _at_median_payload(preprocessing_artifacts):
    """One synthetic customer built from the real, measured feature medians/first-known-category
    -- exercises the full real preprocessing + real trained model path, not a mocked response."""
    payload = {}
    for col in preprocessing_artifacts["numeric_feature_cols"]:
        payload[col] = float(preprocessing_artifacts["feature_medians"].get(col, 0.0))
    for col in preprocessing_artifacts["categorical_encode_cols"]:
        classes = preprocessing_artifacts["label_encoders"][col]["classes"]
        payload[col] = classes[0] if classes else None
    return payload


def test_health_reports_the_real_early_window_k(epd_app):
    client = TestClient(epd_app.app)
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["early_window_k"] == 3


def test_model_info_reports_the_real_measured_metrics(epd_app):
    client = TestClient(epd_app.app)
    resp = client.get("/model-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["early_window_k"] == 3
    assert body["recommended_for_production"] is True
    assert 0.0 < body["holdout_auc"] < 1.0
    assert body["holdout_auc"] == 0.9265274920113401


def test_model_info_without_api_key_is_rejected(epd_app):
    client = TestClient(epd_app.app)
    resp = client.get("/model-info")
    assert resp.status_code == 401


def test_score_returns_a_valid_probability_using_the_real_trained_model(epd_app, preprocessing_artifacts):
    client = TestClient(epd_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    resp = client.post("/score", json=payload, params={"customer_id": "TEST-CUSTOMER-001"}, headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == "TEST-CUSTOMER-001"
    assert 0.0 <= body["predicted_pd"] <= 1.0
    assert body["early_window_k"] == 3


def test_score_without_api_key_is_rejected(epd_app, preprocessing_artifacts):
    client = TestClient(epd_app.app)
    resp = client.post("/score", json=_at_median_payload(preprocessing_artifacts))
    assert resp.status_code == 401


def test_score_returns_top_reasons_that_explain_the_prediction(epd_app, preprocessing_artifacts):
    client = TestClient(epd_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    # Push one numeric feature well off its median so it has a real, non-baseline value.
    numeric_cols = preprocessing_artifacts["numeric_feature_cols"]
    if numeric_cols:
        payload[numeric_cols[0]] = float(payload[numeric_cols[0]]) + 1000.0
    resp = client.post("/score", json=payload, headers=AUTH)
    assert resp.status_code == 200
    reasons = resp.json()["top_reasons"]
    magnitudes = [abs(r["contribution_to_predicted_pd"]) for r in reasons]
    assert magnitudes == sorted(magnitudes, reverse=True)
    assert len(reasons) <= 3


def test_score_is_deterministic_for_the_same_real_input(epd_app, preprocessing_artifacts):
    client = TestClient(epd_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    pd_1 = client.post("/score", json=payload, headers=AUTH).json()["predicted_pd"]
    pd_2 = client.post("/score", json=payload, headers=AUTH).json()["predicted_pd"]
    assert pd_1 == pd_2


def test_score_matches_a_direct_computation_against_the_same_real_model(epd_app, preprocessing_artifacts):
    """The same regression check Notebook 36's own self-test performs: build the feature
    vector exactly as the service does, score it directly with the real loaded model, and
    require the API's answer to match exactly -- catches the exact class of bug (categorical
    fields silently omitted from the payload) found and fixed during this problem's build."""
    client = TestClient(epd_app.app)
    payload = _at_median_payload(preprocessing_artifacts)
    api_pd = client.post("/score", json=payload, headers=AUTH).json()["predicted_pd"]

    all_feature_cols = preprocessing_artifacts["all_feature_cols"]
    categorical_encode_cols = preprocessing_artifacts["categorical_encode_cols"]
    label_encoders = preprocessing_artifacts["label_encoders"]
    feature_medians = preprocessing_artifacts["feature_medians"]

    x = np.zeros((1, len(all_feature_cols)), dtype=np.float32)
    for i, col in enumerate(all_feature_cols):
        val = payload.get(col)
        if col in categorical_encode_cols:
            classes = label_encoders[col]["classes"]
            mapping = {cat: idx for idx, cat in enumerate(classes)}
            x[0, i] = mapping.get(val, -1)
        else:
            x[0, i] = val if val is not None else feature_medians[col]
    direct_pd = float(epd_app.model.predict_proba(x)[:, 1][0])

    assert api_pd == pytest.approx(direct_pd, abs=1e-9)


def test_missing_optional_fields_fall_back_to_real_medians_without_error(epd_app, preprocessing_artifacts):
    """Every field is Optional in the real schema -- an empty payload must not 500."""
    client = TestClient(epd_app.app)
    resp = client.post("/score", json={}, headers=AUTH)
    assert resp.status_code == 200
    assert 0.0 <= resp.json()["predicted_pd"] <= 1.0
    assert resp.json()["top_reasons"] == []
