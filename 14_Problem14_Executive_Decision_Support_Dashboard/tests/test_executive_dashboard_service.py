import os

from fastapi.testclient import TestClient

# Must be set before executive_dashboard_service (and its module-level `app`) is imported below.
os.environ["API_KEY"] = "pytest-only-test-key"

from executive_dashboard_service import app  # noqa: E402

client = TestClient(app)
AUTH = {"X-API-Key": "pytest-only-test-key"}


def test_health_reports_the_real_problems_loaded(real_dashboard_data):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["problems_loaded"] == len(real_dashboard_data["rows"])


def test_executive_summary_without_api_key_is_rejected():
    resp = client.get("/executive-summary")
    assert resp.status_code == 401


def test_executive_summary_matches_the_real_dashboard_data_exactly(real_dashboard_data):
    resp = client.get("/executive-summary", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json() == real_dashboard_data


def test_executive_summary_reports_the_real_total_platform_net_value(real_policy, real_dashboard_data):
    resp = client.get("/executive-summary", headers=AUTH)
    body = resp.json()
    assert body["total_platform_net_value_usd"] == real_policy["total_platform_net_value_usd"]
    assert body["included_problems"] == real_policy["included_problems"]
    assert body["excluded_problems"] == real_policy["excluded_problems"]
    # The one system deliberately excluded for a real, honest KPI miss.
    assert 10 in body["excluded_problems"]


def test_problem_without_api_key_is_rejected():
    resp = client.get("/problem/4")
    assert resp.status_code == 401


def test_problem_lookup_matches_the_real_row_for_every_real_problem(real_dashboard_data):
    for row in real_dashboard_data["rows"]:
        resp = client.get(f"/problem/{row['problem_number']}", headers=AUTH)
        assert resp.status_code == 200
        assert resp.json() == row


def test_problem_10_is_honestly_not_recommended(real_dashboard_data):
    row = next(r for r in real_dashboard_data["rows"] if r["problem_number"] == 10)
    resp = client.get("/problem/10", headers=AUTH)
    assert resp.status_code == 200
    assert resp.json()["recommended_for_production"] is False
    assert row["recommended_for_production"] is False


def test_unknown_problem_number_is_404():
    resp = client.get("/problem/999", headers=AUTH)
    assert resp.status_code == 404
