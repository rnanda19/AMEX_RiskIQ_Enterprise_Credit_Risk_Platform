from fastapi.testclient import TestClient

from shared.tiers import assign_band

# Same real business_rule bands as conftest.py's fixture policy (kept as a
# separate local copy, not a cross-import from conftest, so this test file
# has no import-path dependency on how pytest happens to resolve the
# sibling `tests` packages under Problem1_.../tests and Problem2_.../tests
# when both are collected in one pytest run).
_REAL_BUSINESS_RULE_THRESHOLDS = [
    {"risk_tier": "Prime", "tier_order": 1, "pd_lower": 0.0, "pd_upper": 0.05},
    {"risk_tier": "Near-Prime", "tier_order": 2, "pd_lower": 0.05, "pd_upper": 0.15},
    {"risk_tier": "Subprime", "tier_order": 3, "pd_lower": 0.15, "pd_upper": 0.35},
    {"risk_tier": "High Risk", "tier_order": 4, "pd_lower": 0.35, "pd_upper": 1.01},
]


def _expected_tier_for(pd_value):
    return assign_band(
        pd_value, _REAL_BUSINESS_RULE_THRESHOLDS,
        lower_key="pd_lower", upper_key="pd_upper",
        label_key="risk_tier", order_key="tier_order",
    )


AUTH = {"X-API-Key": "pytest-only-test-key"}  # must match conftest.py's TEST_API_KEY


def test_health_reports_champion_model(risk_tier_app):
    client = TestClient(risk_tier_app.app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "champion_model": "logistic_regression"}


def test_policy_info_reports_real_tier_order_and_thresholds(risk_tier_app):
    client = TestClient(risk_tier_app.app)
    resp = client.get("/policy-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["n_tiers"] == 4
    assert body["tier_order"] == ["Prime", "Near-Prime", "Subprime", "High Risk"]
    assert body["primary_method"] == "business_rule"
    assert len(body["business_rule_thresholds"]) == 4


def test_policy_info_without_api_key_is_rejected(risk_tier_app):
    client = TestClient(risk_tier_app.app)
    resp = client.get("/policy-info")
    assert resp.status_code == 401


def test_risk_tier_returns_a_tier_consistent_with_the_real_policy_bands(risk_tier_app):
    """Whatever PD the (genuinely fit) model returns, the tier in the
    response must be exactly what assign_band() would independently compute
    for that same PD against the real business-rule bands -- this catches a
    real class of bug (service using a stale/wrong policy) that a test
    asserting one hardcoded expected tier would miss."""
    client = TestClient(risk_tier_app.app)
    resp = client.post(
        "/risk-tier",
        params={"customer_id": "cust_001"},
        json={"balance": 800.0, "spend_last_month": 150.0, "region": "north"},
        headers=AUTH,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == "cust_001"
    assert body["tier_method"] == "business_rule"
    assert body["champion_model"] == "logistic_regression"
    assert 0.0 <= body["predicted_pd"] <= 1.0
    assert body["risk_tier"] == _expected_tier_for(body["predicted_pd"])


def test_risk_tier_without_api_key_is_rejected(risk_tier_app):
    client = TestClient(risk_tier_app.app)
    resp = client.post("/risk-tier", json={"balance": 800.0, "spend_last_month": 150.0, "region": "north"})
    assert resp.status_code == 401


def test_risk_tier_returns_top_reasons_that_explain_the_prediction(risk_tier_app):
    client = TestClient(risk_tier_app.app)
    resp = client.post(
        "/risk-tier",
        json={"balance": 5000.0, "spend_last_month": 900.0, "region": "north"},
        headers=AUTH,
    )
    assert resp.status_code == 200
    reasons = resp.json()["top_reasons"]
    assert 1 <= len(reasons) <= 3
    magnitudes = [abs(r["contribution_to_predicted_pd"]) for r in reasons]
    assert magnitudes == sorted(magnitudes, reverse=True)


def test_risk_tier_handles_missing_features_via_median_imputation(risk_tier_app):
    client = TestClient(risk_tier_app.app)
    resp = client.post("/risk-tier", json={}, headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["risk_tier"] == _expected_tier_for(body["predicted_pd"])
    assert body["top_reasons"] == []


def test_risk_tier_handles_unseen_category_gracefully(risk_tier_app):
    client = TestClient(risk_tier_app.app)
    resp = client.post(
        "/risk-tier",
        json={"balance": 300.0, "spend_last_month": 50.0, "region": "never_seen_before"},
        headers=AUTH,
    )
    assert resp.status_code == 200
    assert 0.0 <= resp.json()["predicted_pd"] <= 1.0
