import os

import pytest
from fastapi.testclient import TestClient

# Must be set before credit_line_scoring_service (and its module-level `app`) is imported below.
os.environ["API_KEY"] = "pytest-only-test-key"

from credit_line_scoring_service import (  # noqa: E402
    app, _assign_risk_level, _assign_trend, ACTION_MAP,
)

client = TestClient(app)
AUTH = {"X-API-Key": "pytest-only-test-key"}


def test_health_is_open_no_auth_required():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_policy_info_matches_the_real_policy_and_is_honestly_not_recommended(real_policy):
    resp = client.get("/policy-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["risk_level_names"] == real_policy["risk_level_names"]
    assert body["trend_names"] == real_policy["trend_names"]
    assert body["action_tier_matrix"] == real_policy["action_tier_matrix"]
    # Honest, real result: this technique did NOT clear its own KPI bar on this run.
    assert body["recommended_for_production"] is False
    assert real_policy["recommended_for_production"] is False


def test_policy_info_without_api_key_is_rejected():
    resp = client.get("/policy-info")
    assert resp.status_code == 401


def test_recommend_without_api_key_is_rejected():
    resp = client.post("/recommend", json={"static_pd": 0.1, "dynamic_pd": 0.1})
    assert resp.status_code == 401


def test_recommend_out_of_range_pd_is_rejected():
    resp = client.post("/recommend", json={"static_pd": 1.5, "dynamic_pd": 0.1}, headers=AUTH)
    assert resp.status_code == 422
    resp = client.post("/recommend", json={"static_pd": 0.1, "dynamic_pd": -0.1}, headers=AUTH)
    assert resp.status_code == 422


def test_recommend_at_real_low_risk_boundary_matches_direct_computation(real_policy):
    """A dynamic_pd exactly at the real risk_level_cut_low should classify as the lowest real
    risk level -- matches calling _assign_risk_level() directly."""
    dynamic_pd = real_policy["risk_level_cut_low"]
    resp = client.post(
        "/recommend", json={"static_pd": dynamic_pd, "dynamic_pd": dynamic_pd}, headers=AUTH
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["risk_level"] == _assign_risk_level(dynamic_pd)
    assert body["risk_level"] == real_policy["risk_level_names"][0]
    assert body["pd_trend"] == pytest.approx(0.0)
    assert body["trend"] == _assign_trend(0.0)
    assert body["recommended_for_production"] is False


def test_recommend_risk_level_matches_real_cuts_at_stable_trend(real_policy):
    """Holds trend at exactly 'Stable' (static_pd == dynamic_pd, pd_trend == 0) and sweeps
    dynamic_pd across the 3 real risk-level brackets."""
    risk_level_names = real_policy["risk_level_names"]
    trend_names = real_policy["trend_names"]
    candidates = [
        real_policy["risk_level_cut_low"] / 2,
        (real_policy["risk_level_cut_low"] + real_policy["risk_level_cut_high"]) / 2,
        min(1.0, real_policy["risk_level_cut_high"] + 0.05),
    ]
    for ri, pd_val in enumerate(candidates):
        resp = client.post("/recommend", json={"static_pd": pd_val, "dynamic_pd": pd_val}, headers=AUTH)
        assert resp.status_code == 200
        body = resp.json()
        assert body["risk_level"] == risk_level_names[ri]
        assert body["trend"] == trend_names[1]  # "Stable" -- pd_trend is exactly 0
        cell = ACTION_MAP.get((risk_level_names[ri], trend_names[1]))
        assert cell is not None
        assert body["action"] == cell["action"]
        assert body["rationale"] == cell["rationale"]


def test_recommend_trend_matches_real_cuts_at_a_safe_mid_range_risk_level(real_policy):
    """Holds dynamic_pd comfortably inside the Medium-risk bracket (away from 0/1, so no
    static_pd clamping is possible) and sweeps pd_trend across the 3 real trend brackets."""
    trend_names = real_policy["trend_names"]
    dynamic_pd = (real_policy["risk_level_cut_low"] + real_policy["risk_level_cut_high"]) / 2
    trend_deltas = [
        real_policy["trend_cut_low"] - 0.01,
        0.0,
        real_policy["trend_cut_high"] + 0.01,
    ]
    for ti, delta in enumerate(trend_deltas):
        static_pd = dynamic_pd - delta
        assert 0.0 <= static_pd <= 1.0, "test construction error -- static_pd out of range"
        resp = client.post(
            "/recommend", json={"static_pd": static_pd, "dynamic_pd": dynamic_pd}, headers=AUTH
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["trend"] == trend_names[ti]
        assert body["pd_trend"] == pytest.approx(delta)


def test_recommend_response_reasoning_cites_the_real_cuts(real_policy):
    dynamic_pd = real_policy["risk_level_cut_low"]
    resp = client.post(
        "/recommend", json={"static_pd": dynamic_pd, "dynamic_pd": dynamic_pd}, headers=AUTH
    )
    body = resp.json()
    assert len(body["reasoning"]) == 3
    assert body["risk_level"] in body["reasoning"][0]
    assert body["trend"] in body["reasoning"][1]
    assert body["action"] in body["reasoning"][2]
