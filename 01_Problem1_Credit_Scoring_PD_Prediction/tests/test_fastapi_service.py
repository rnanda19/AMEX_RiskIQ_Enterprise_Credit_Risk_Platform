from fastapi.testclient import TestClient

# Must match conftest.py's TEST_API_KEY exactly -- kept as a separate local constant, not a
# cross-import of a bare `conftest` module, since every Problem's tests/ directory has its own
# conftest.py and a plain `import conftest` risks resolving to a DIFFERENT problem's module (by
# name collision in sys.modules) when pytest collects across problems at once, as `make test-all`
# does.
AUTH = {"X-API-Key": "pytest-only-test-key"}


def test_health_reports_champion_model(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "champion_model": "logistic_regression"}


def test_model_info_reports_feature_counts_and_metrics(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.get("/model-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["champion_model"] == "logistic_regression"
    assert body["feature_count"] == 3
    assert body["numeric_feature_count"] == 2
    assert body["categorical_feature_count"] == 1
    assert body["holdout_auc"] == 0.9620396555226549


def test_model_info_without_api_key_is_rejected(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.get("/model-info")
    assert resp.status_code == 401


def test_predict_returns_a_probability_in_range(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.post(
        "/predict",
        params={"customer_id": "cust_001"},
        json={"balance": 800.0, "spend_last_month": 150.0, "region": "north"},
        headers=AUTH,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == "cust_001"
    assert body["champion_model"] == "logistic_regression"
    assert 0.0 <= body["predicted_pd"] <= 1.0


def test_predict_without_api_key_is_rejected(fastapi_app):
    """The single largest gap named in the platform's own model-risk benchmark: no service had
    any authentication. This is the regression test for the fix."""
    client = TestClient(fastapi_app.app)
    resp = client.post("/predict", json={"balance": 800.0, "spend_last_month": 150.0, "region": "north"})
    assert resp.status_code == 401


def test_predict_with_wrong_api_key_is_rejected(fastapi_app):
    client = TestClient(fastapi_app.app)
    resp = client.post("/predict", json={}, headers={"X-API-Key": "not-the-right-key"})
    assert resp.status_code == 401


def test_predict_handles_missing_features_via_median_imputation(fastapi_app):
    """Every field is Optional -- a request with no fields at all must not
    500, it should impute every numeric field from feature_medians and fall
    back to the '__missing__' category encoding, exactly as the real
    scoring path documents."""
    client = TestClient(fastapi_app.app)
    resp = client.post("/predict", json={}, headers=AUTH)
    assert resp.status_code == 200
    assert 0.0 <= resp.json()["predicted_pd"] <= 1.0


def test_predict_unseen_category_does_not_crash(fastapi_app):
    """An unseen region value should map to -1 (the documented fallback for
    a category the encoder never saw), not raise."""
    client = TestClient(fastapi_app.app)
    resp = client.post(
        "/predict",
        json={"balance": 300.0, "spend_last_month": 50.0, "region": "never_seen_before"},
        headers=AUTH,
    )
    assert resp.status_code == 200
    assert 0.0 <= resp.json()["predicted_pd"] <= 1.0


def test_predict_returns_top_reasons_that_explain_the_prediction(fastapi_app):
    """Real, per-request explainability: /predict must return the specific factors that moved
    THIS customer's own score, not an empty or generic list -- the fix for the platform's other
    named hard blocker (no CFPB-style adverse-action reason codes on any service)."""
    client = TestClient(fastapi_app.app)
    resp = client.post(
        "/predict",
        json={"balance": 5000.0, "spend_last_month": 900.0, "region": "north"},
        headers=AUTH,
    )
    assert resp.status_code == 200
    reasons = resp.json()["top_reasons"]
    assert 1 <= len(reasons) <= 3
    for r in reasons:
        assert set(r.keys()) == {"factor", "contribution_to_predicted_pd"}
        assert r["factor"] in {"balance", "spend_last_month", "region"}
    # Ranked by |contribution|, largest first.
    magnitudes = [abs(r["contribution_to_predicted_pd"]) for r in reasons]
    assert magnitudes == sorted(magnitudes, reverse=True)


def test_predict_at_baseline_returns_no_reasons(fastapi_app):
    """A request that matches the training-set baseline everywhere (all fields omitted, so every
    feature is imputed to its own median/'__missing__' encoding) has no feature that differs from
    baseline -- top_reasons must come back empty rather than fabricating a reason that isn't real."""
    client = TestClient(fastapi_app.app)
    resp = client.post("/predict", json={}, headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["top_reasons"] == []
