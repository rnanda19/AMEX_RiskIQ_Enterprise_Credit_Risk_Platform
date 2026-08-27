import os

from fastapi.testclient import TestClient

# Must be set before real_time_alert_service (and its module-level `app`) is imported below.
os.environ["API_KEY"] = "pytest-only-test-key"

from real_time_alert_service import app, compute_early_warning, top_reason_codes  # noqa: E402

client = TestClient(app)
AUTH = {"X-API-Key": "pytest-only-test-key"}


def test_health_reports_the_real_winning_min_deviation_count(real_policy):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["winning_min_deviation_count"] == real_policy["winning_min_deviation_count"]


def test_model_info_matches_the_real_policy_exactly(real_policy):
    resp = client.get("/model-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["z_threshold"] == real_policy["z_threshold"]
    assert body["min_statements_for_baseline"] == real_policy["min_statements_for_baseline"]
    assert body["monitored_feature_count"] == len(real_policy["monitored_features"])
    assert body["winning_candidate_metrics"] == real_policy["winning_candidate_metrics"]
    # REVISED 2026-08-27: after widening MIN_DEVIATION_COUNT_CANDIDATES, this technique's real
    # re-run cleared the KPI (recommended_for_production is now True) -- assert against the real
    # policy value dynamically rather than a hardcoded literal, so this test tracks whatever the
    # real, measured result honestly is instead of freezing one past outcome.
    assert body["recommended_for_production"] == real_policy["recommended_for_production"]


def test_model_info_without_api_key_is_rejected():
    resp = client.get("/model-info")
    assert resp.status_code == 401


def test_score_matches_a_direct_computation_against_the_real_policy(deviating_statements):
    """The API must produce bit-identical results to calling compute_early_warning() directly
    against the exact same statement history."""
    resp = client.post("/score", json={"customer_id": "T1", "statements": deviating_statements}, headers=AUTH)
    assert resp.status_code == 200
    api_body = resp.json()
    direct = compute_early_warning(deviating_statements)
    assert api_body["early_warning_score"] == direct["early_warning_score"]
    assert api_body["z_computable_feature_count"] == direct["z_computable_feature_count"]
    assert api_body["feature_deviations"] == direct["feature_deviations"]


def test_score_without_api_key_is_rejected(deviating_statements):
    resp = client.post("/score", json={"statements": deviating_statements})
    assert resp.status_code == 401


def test_score_top_reasons_matches_direct_top_reason_codes(deviating_statements):
    resp = client.post("/score", json={"statements": deviating_statements}, headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    direct_reasons = top_reason_codes(body["feature_deviations"])
    api_reasons = body["top_reasons"]
    assert [r["factor"] for r in api_reasons] == [r.factor for r in direct_reasons]
    z_values = [abs(r["z_score"]) for r in api_reasons]
    assert z_values == sorted(z_values, reverse=True)


def test_alert_flag_is_exactly_score_gte_winning_threshold(deviating_statements, real_policy):
    resp = client.post("/score", json={"statements": deviating_statements}, headers=AUTH)
    body = resp.json()
    expected_alert = body["early_warning_score"] >= real_policy["winning_min_deviation_count"]
    assert body["alert"] == expected_alert


def test_too_few_statements_returns_422(real_policy):
    features = real_policy["monitored_features"]
    too_short = [{feat: 1.0 for feat in features}]  # fewer than min_statements_for_baseline
    resp = client.post("/score", json={"statements": too_short}, headers=AUTH)
    assert resp.status_code == 422


def test_customer_id_is_echoed_back_when_provided(deviating_statements):
    resp = client.post("/score", json={"customer_id": "XYZ-9", "statements": deviating_statements}, headers=AUTH)
    assert resp.json()["customer_id"] == "XYZ-9"


def test_flat_baseline_with_no_variance_yields_zero_score(real_policy):
    """A baseline with zero variance per feature (std=0) cannot compute a z-score for that
    feature (division by zero is explicitly guarded against) -- every deviation should come back
    None and the early_warning_score should be 0, exercising that guard directly."""
    features = real_policy["monitored_features"]
    flat = [{feat: 5.0 for feat in features} for _ in range(5)]
    resp = client.post("/score", json={"statements": flat}, headers=AUTH)
    body = resp.json()
    assert body["early_warning_score"] == 0
    assert all(v is None for v in body["feature_deviations"].values())
    assert body["top_reasons"] == []
