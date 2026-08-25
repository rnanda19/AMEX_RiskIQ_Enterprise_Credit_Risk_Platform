from fastapi.testclient import TestClient

from ecl_calculator import compute_ecl
from ecl_scoring_service import app

client = TestClient(app)


def test_health_endpoint_reports_ok_and_tier_order(real_bundle):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["tier_order"] == real_bundle["tier_order"]


def test_model_info_matches_the_real_bundle(real_bundle):
    r = client.get("/model-info")
    assert r.status_code == 200
    body = r.json()
    assert body["lgd_by_tier"] == real_bundle["lgd_by_tier"]
    assert body["ead_per_account_usd"] == real_bundle["ead_per_account_usd"]


def test_score_endpoint_matches_direct_computation_exactly(real_bundle):
    """The API must produce bit-identical results to calling compute_ecl() directly -- it is a
    thin wrapper, not a reimplementation."""
    for tier in real_bundle["tier_order"]:
        for pd_12m in (0.02, 0.15, 0.6):
            r = client.post("/score", json={"pd_12m": pd_12m, "severity_tier": tier, "customer_id": "T1"})
            assert r.status_code == 200
            api_result = r.json()
            direct_result = compute_ecl(pd_12m, tier, real_bundle)
            for key in ("ifrs9_stage", "ecl_ifrs9_usd", "ecl_cecl_usd"):
                assert api_result[key] == direct_result[key], f"mismatch on {key} for pd={pd_12m}, tier={tier}"


def test_unknown_severity_tier_returns_422():
    r = client.post("/score", json={"pd_12m": 0.1, "severity_tier": "Not A Real Tier"})
    assert r.status_code == 422


def test_pd_out_of_range_is_rejected_by_pydantic():
    r = client.post("/score", json={"pd_12m": 1.5, "severity_tier": "Low Severity"})
    assert r.status_code == 422
    r = client.post("/score", json={"pd_12m": -0.1, "severity_tier": "Low Severity"})
    assert r.status_code == 422


def test_customer_id_is_echoed_back_when_provided():
    r = client.post("/score", json={"pd_12m": 0.1, "severity_tier": "Low Severity", "customer_id": "ABC-123"})
    assert r.json()["customer_id"] == "ABC-123"


def test_customer_id_is_none_when_omitted():
    r = client.post("/score", json={"pd_12m": 0.1, "severity_tier": "Low Severity"})
    assert r.json()["customer_id"] is None
