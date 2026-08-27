import os

import pytest
from fastapi.testclient import TestClient

# Must be set before portfolio_alert_feed_service (and its module-level `app`) is imported below.
os.environ["API_KEY"] = "pytest-only-test-key"

from portfolio_alert_feed_service import app  # noqa: E402

client = TestClient(app)
AUTH = {"X-API-Key": "pytest-only-test-key"}


@pytest.fixture(autouse=True)
def reset_history():
    """Every test gets a clean in-memory history -- this service's real, documented state."""
    client.post("/reset", headers=AUTH)
    yield
    client.post("/reset", headers=AUTH)


def _month(month: str, means=None):
    return {
        "month": month,
        "n_statements": 10_000,
        "n_unique_customers": 8_000,
        "column_means": means or {"P_2": 0.5, "B_1": 1.0, "B_11": 0.2, "D_39": 0.1,
                                   "B_4": 0.3, "S_3": 0.4, "R_1": 0.1, "B_5": 0.2},
    }


def test_health_is_open_and_reports_zero_months_after_reset():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["n_months_ingested"] == 0
    assert body["current_alert_state"] is False


def test_policy_info_matches_the_real_policy_and_is_honestly_recommended(real_policy):
    resp = client.get("/policy-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["control_limit_k_sigma"] == real_policy["control_limit_k_sigma"]
    assert body["min_trailing_months_for_baseline"] == real_policy["min_trailing_months_for_baseline"]
    assert body["monitored_base_columns"] == real_policy["monitored_base_columns"]
    assert body["recommended_for_production"] is True
    assert real_policy["recommended_for_production"] is True


def test_policy_info_without_api_key_is_rejected():
    resp = client.get("/policy-info")
    assert resp.status_code == 401


def test_ingest_month_without_api_key_is_rejected():
    resp = client.post("/ingest-month", json=_month("2018-01-01"))
    assert resp.status_code == 401


def test_months_below_the_real_baseline_window_are_never_alert_eligible(real_policy):
    """The first min_trailing_months_for_baseline months can never be baseline_eligible --
    there isn't enough real trailing history yet."""
    min_months = real_policy["min_trailing_months_for_baseline"]
    for i in range(min_months):
        resp = client.post("/ingest-month", json=_month(f"2018-{i + 1:02d}-01"), headers=AUTH)
        assert resp.status_code == 200
        body = resp.json()
        assert body["baseline_eligible"] is False
        assert body["alert"] is False


def test_a_real_breaching_month_triggers_alert_once_baseline_eligible(real_policy):
    """Seed min_trailing_months stable months, then send one wildly deviating month -- with
    winning_consecutive_breach_candidate == 1 (the real, measured winning candidate), a single
    breaching month is enough to alert."""
    min_months = real_policy["min_trailing_months_for_baseline"]
    stable_means = {"P_2": 0.5, "B_1": 1.0, "B_11": 0.2, "D_39": 0.1, "B_4": 0.3, "S_3": 0.4, "R_1": 0.1, "B_5": 0.2}
    for i in range(min_months + 1):
        # tiny real-looking jitter so the baseline has nonzero std (required for a z-score)
        jittered = {k: v + (0.001 * ((i % 3) - 1)) for k, v in stable_means.items()}
        resp = client.post("/ingest-month", json=_month(f"2018-{i + 1:02d}-01", jittered), headers=AUTH)
        assert resp.status_code == 200

    breach_month = _month("2019-01-01", {k: v * 100 for k, v in stable_means.items()})
    resp = client.post("/ingest-month", json=breach_month, headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["baseline_eligible"] is True
    assert body["breach_count"] >= 1
    assert body["consecutive_breach_run_length"] >= real_policy["winning_consecutive_breach_candidate"]
    assert body["alert"] is True


def test_alert_feed_returns_full_real_history():
    client.post("/ingest-month", json=_month("2018-01-01"), headers=AUTH)
    client.post("/ingest-month", json=_month("2018-02-01"), headers=AUTH)
    resp = client.get("/alert-feed", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["n_months"] == 2
    assert [m["month"] for m in body["months"]] == ["2018-01-01", "2018-02-01"]


def test_reset_clears_history():
    client.post("/ingest-month", json=_month("2018-01-01"), headers=AUTH)
    resp = client.post("/reset", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["status"] == "reset"
    health = client.get("/health").json()
    assert health["n_months_ingested"] == 0
