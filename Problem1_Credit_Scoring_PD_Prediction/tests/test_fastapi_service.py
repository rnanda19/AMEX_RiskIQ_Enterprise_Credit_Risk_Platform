from fastapi.testclient import TestClient


def test_health_reports_champion_model(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "champion_model": "logistic_regression"}


def test_model_info_reports_feature_counts_and_metrics(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.get("/model-info")
    assert resp.status_code == 200
    body = resp.json()
    assert body["champion_model"] == "logistic_regression"
    assert body["feature_count"] == 3
    assert body["numeric_feature_count"] == 2
    assert body["categorical_feature_count"] == 1
    assert body["holdout_auc"] == 0.9620396555226549


def test_predict_returns_a_probability_in_range(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.post(
        "/predict",
        params={"customer_id": "cust_001"},
        json={"balance": 800.0, "spend_last_month": 150.0, "region": "north"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == "cust_001"
    assert body["champion_model"] == "logistic_regression"
    assert 0.0 <= body["predicted_pd"] <= 1.0


def test_predict_handles_missing_features_via_median_imputation(fastapi_app):
    """Every field is Optional -- a request with no fields at all must not
    500, it should impute every numeric field from feature_medians and fall
    back to the '__missing__' category encoding, exactly as the real
    scoring path documents."""
    client = TestClient(fastapi_app.app)
    resp = client.post("/predict", json={})
    assert resp.status_code == 200
    assert 0.0 <= resp.json()["predicted_pd"] <= 1.0


def test_predict_unseen_category_does_not_crash(fastapi_app):
    """An unseen region value should map to -1 (the documented fallback for
    a category the encoder never saw), not raise."""
    client = TestClient(fastapi_app.app)
    resp = client.post(
        "/predict",
        json={"balance": 300.0, "spend_last_month": 50.0, "region": "never_seen_before"},
    )
    assert resp.status_code == 200
    assert 0.0 <= resp.json()["predicted_pd"] <= 1.0
