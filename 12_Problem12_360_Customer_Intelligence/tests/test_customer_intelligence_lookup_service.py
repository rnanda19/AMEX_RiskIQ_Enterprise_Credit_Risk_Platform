import os

from fastapi.testclient import TestClient

# Must be set before customer_intelligence_lookup_service (and its module-level `app`) is
# imported below. conftest.py already set AMEX_P12_PROFILE_PATH to the fixture parquet.
os.environ["API_KEY"] = "pytest-only-test-key"

from customer_intelligence_lookup_service import app  # noqa: E402

client = TestClient(app)
AUTH = {"X-API-Key": "pytest-only-test-key"}


def test_health_reports_the_fixture_profiles_loaded():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["profiles_loaded"] == 2


def test_policy_info_matches_the_real_policy_and_is_honestly_recommended(real_policy):
    resp = client.get("/policy-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["unified_risk_grade_names"] == real_policy["unified_risk_grade_names"]
    assert body["unified_score_weights"] == real_policy["unified_score_weights"]
    assert body["recommended_for_production"] is True
    assert real_policy["recommended_for_production"] is True


def test_policy_info_without_api_key_is_rejected():
    resp = client.get("/policy-info")
    assert resp.status_code == 401


def test_profile_without_api_key_is_rejected():
    resp = client.get("/profile/CUST-COLLECTIONS-ELIGIBLE")
    assert resp.status_code == 401


def test_profile_for_unknown_customer_is_404():
    resp = client.get("/profile/NO-SUCH-CUSTOMER", headers=AUTH)
    assert resp.status_code == 404


def test_profile_for_collections_eligible_customer_includes_the_real_collections_term(fixture_rows):
    row = fixture_rows[0]
    resp = client.get(f"/profile/{row['customer_ID']}", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == row["customer_ID"]
    assert body["static_pd"] == row["STATIC_PD"]
    assert body["dynamic_pd"] == row["DYNAMIC_PD"]
    assert body["collections_eligible"] is True
    assert body["propensity_to_cure"] == row["PROPENSITY_TO_CURE"]
    assert body["treatment_tier"] == row["TREATMENT_TIER"]
    assert body["unified_risk_score"] == row["UNIFIED_RISK_SCORE"]
    assert body["unified_risk_grade"] == row["UNIFIED_RISK_GRADE"]
    assert "collections propensity" in body["rationale"]
    assert len(body["reasoning"]) == 4
    assert "propensity_to_cure" in body["reasoning"][2]


def test_profile_for_non_eligible_customer_honestly_excludes_the_collections_term(fixture_rows):
    row = fixture_rows[1]
    resp = client.get(f"/profile/{row['customer_ID']}", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["collections_eligible"] is False
    assert body["propensity_to_cure"] is None
    assert body["treatment_tier"] is None
    assert "collections term not applicable" in body["rationale"]
    assert "not currently collections-eligible" in body["reasoning"][2]
