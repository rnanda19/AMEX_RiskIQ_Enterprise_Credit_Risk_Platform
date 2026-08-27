import os

import numpy as np
import pytest
from fastapi.testclient import TestClient

# Must be set before collections_scoring_service (and its module-level `app`) is imported below.
os.environ["API_KEY"] = "pytest-only-test-key"

from collections_scoring_service import app, MODEL, MONITORED_FEATURES  # noqa: E402

client = TestClient(app)
AUTH = {"X-API-Key": "pytest-only-test-key"}


def test_health_is_open_no_auth_required():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_model_info_matches_the_real_policy(real_policy):
    resp = client.get("/model-info", headers=AUTH)
    assert resp.status_code == 200
    body = resp.json()
    assert body["monitored_features"] == real_policy["monitored_features"]
    assert body["treatment_tiers"] == real_policy["treatment_tier_policy"]["tiers"]
    # Honest, real result: this technique meets its KPI target and IS recommended.
    assert body["meets_kpi_target"] is True
    assert body["recommended_for_production"] is True
    assert real_policy["meets_kpi_target"] is True
    assert real_policy["recommended_for_production"] is True


def test_model_info_without_api_key_is_rejected():
    resp = client.get("/model-info")
    assert resp.status_code == 401


def test_score_without_api_key_is_rejected(mean_statement):
    resp = client.post("/score", json={"current_statement": mean_statement})
    assert resp.status_code == 401


def test_score_matches_the_real_trained_model_exactly(mean_statement):
    """The API's propensity score must be bit-identical to calling the real, loaded
    XGBoost model's predict_proba() directly on the same input -- no drift, no re-derivation."""
    resp = client.post(
        "/score", json={"customer_id": "T1", "current_statement": mean_statement}, headers=AUTH
    )
    assert resp.status_code == 200
    body = resp.json()

    x_row = np.array([[mean_statement[c] for c in MONITORED_FEATURES]], dtype=np.float32)
    direct_propensity = float(MODEL.predict_proba(x_row)[:, 1][0])
    assert body["propensity_to_cure"] == pytest.approx(direct_propensity, abs=1e-6)
    assert 0.0 <= body["propensity_to_cure"] <= 1.0
    assert body["treatment_tier"] in {"Automated Nudge", "Priority Outreach"}
    assert body["meets_kpi_target"] is True
    assert body["recommended_for_production"] is True


def test_score_top_reasons_are_bounded_and_sorted_by_magnitude(mean_statement):
    resp = client.post("/score", json={"current_statement": mean_statement}, headers=AUTH)
    reasons = resp.json()["top_reasons"]
    assert len(reasons) <= 3
    magnitudes = [abs(r["contribution_to_propensity"]) for r in reasons]
    assert magnitudes == sorted(magnitudes, reverse=True)


def test_score_tiers_around_the_real_0_5_reference(mean_statement, real_policy):
    """The deployed API tiers on a fixed 0.5 propensity reference (documented known gap vs.
    Notebook 51's live population-median split -- see MODEL_CARD.md); this just verifies that
    documented, real behavior is what actually ships."""
    resp = client.post("/score", json={"current_statement": mean_statement}, headers=AUTH)
    body = resp.json()
    if body["propensity_to_cure"] >= 0.5:
        assert body["treatment_tier"] == "Automated Nudge"
    else:
        assert body["treatment_tier"] == "Priority Outreach"
