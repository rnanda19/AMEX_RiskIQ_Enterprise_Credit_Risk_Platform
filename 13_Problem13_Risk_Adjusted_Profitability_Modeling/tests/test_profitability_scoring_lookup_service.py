import os

from fastapi.testclient import TestClient

# Must be set before profitability_scoring_lookup_service (and its module-level `app`) is
# imported below. conftest.py already set AMEX_P13_PROFILE_PATH to the fixture parquet.
os.environ["API_KEY"] = "pytest-only-test-key"

from profitability_scoring_lookup_service import app  # noqa: E402

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
    assert body["profitability_tier_names"] == real_policy["profitability_tier_names"]
    assert body["revenue_assumptions"] == real_policy["revenue_assumptions"]
    assert body["recommended_for_production"] is True
    assert real_policy["recommended_for_production"] is True


def test_policy_info_without_api_key_is_rejected():
    resp = client.get("/policy-info")
    assert resp.status_code == 401


def test_profitability_without_api_key_is_rejected():
    resp = client.get("/profitability/CUST-HIGH-PROFIT")
    assert resp.status_code == 401


def test_profitability_for_unknown_customer_is_404():
    resp = client.get("/profitability/NO-SUCH-CUSTOMER", headers=AUTH)
    assert resp.status_code == 404


def test_profitability_matches_the_real_precomputed_fixture_row(fixture_rows):
    row = fixture_rows[0]
    resp = client.get(f"/profitability/{row['customer_ID']}", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == row["customer_ID"]
    assert body["unified_risk_score"] == row["UNIFIED_RISK_SCORE"]
    assert body["profitability_score_usd"] == row["PROFITABILITY_SCORE"]
    assert body["profitability_tier"] == row["PROFITABILITY_TIER"]
    assert len(body["reasoning"]) == 4


def test_low_profitability_tier_row_reports_the_real_negative_score(fixture_rows):
    row = fixture_rows[1]
    resp = client.get(f"/profitability/{row['customer_ID']}", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["profitability_score_usd"] < 0
    assert body["profitability_tier"] == "Low Profitability"
    assert body["expected_loss_usd"] == row["EXPECTED_LOSS_USD"]
