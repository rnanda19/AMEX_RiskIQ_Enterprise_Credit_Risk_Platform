import os
import time

import jwt
from fastapi.testclient import TestClient

# Must be set before real_time_alert_service (and its module-level `app`) is imported below.
os.environ["API_KEY"] = "pytest-only-test-key"

from real_time_alert_service import (  # noqa: E402
    JWT_ALGORITHM,
    JWT_AUDIENCE,
    JWT_ISSUER,
    JWT_SCOPE,
    REGISTERED_CLIENT_ID,
    app,
    compute_early_warning,
    top_reason_codes,
)

client = TestClient(app)
SHARED_SECRET = "pytest-only-test-key"


def _fetch_real_token(client_id=REGISTERED_CLIENT_ID, client_secret=SHARED_SECRET, grant_type="client_credentials"):
    """Drives the real /token endpoint end-to-end -- not a shortcut that fabricates a token the
    endpoint itself never issued."""
    return client.post(
        "/token",
        data={"grant_type": grant_type, "client_id": client_id, "client_secret": client_secret},
    )


def _bearer_auth():
    resp = _fetch_real_token()
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


AUTH = _bearer_auth()


def test_health_reports_the_real_winning_min_deviation_count(real_policy):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["winning_min_deviation_count"] == real_policy["winning_min_deviation_count"]


def test_token_endpoint_issues_a_real_bearer_token_for_the_registered_client():
    resp = _fetch_real_token()
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 900
    decoded = jwt.decode(
        body["access_token"], SHARED_SECRET, algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE, issuer=JWT_ISSUER
    )
    assert decoded["sub"] == REGISTERED_CLIENT_ID
    assert decoded["scope"] == JWT_SCOPE
    assert decoded["exp"] - decoded["iat"] == 900


def test_token_endpoint_rejects_wrong_client_secret():
    resp = _fetch_real_token(client_secret="not-the-real-secret")
    assert resp.status_code == 401


def test_token_endpoint_rejects_unknown_client_id():
    resp = _fetch_real_token(client_id="some-other-client")
    assert resp.status_code == 401


def test_token_endpoint_rejects_unsupported_grant_type():
    resp = _fetch_real_token(grant_type="password")
    assert resp.status_code == 400


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


def test_model_info_without_a_token_is_rejected():
    resp = client.get("/model-info")
    assert resp.status_code == 401


def test_model_info_with_the_old_x_api_key_header_alone_is_rejected():
    """Real regression check: the platform's old shared X-API-Key header must NOT authenticate
    this endpoint any more -- this pilot genuinely replaced it, not just added a second option."""
    resp = client.get("/model-info", headers={"X-API-Key": SHARED_SECRET})
    assert resp.status_code == 401


def test_model_info_with_an_invalid_token_is_rejected():
    resp = client.get("/model-info", headers={"Authorization": "Bearer not-a-real-jwt"})
    assert resp.status_code == 401


def test_model_info_with_an_expired_token_is_rejected():
    now = int(time.time())
    expired = jwt.encode(
        {
            "iss": JWT_ISSUER,
            "sub": REGISTERED_CLIENT_ID,
            "aud": JWT_AUDIENCE,
            "scope": JWT_SCOPE,
            "iat": now - 1000,
            "exp": now - 100,
        },
        SHARED_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    resp = client.get("/model-info", headers={"Authorization": f"Bearer {expired}"})
    assert resp.status_code == 401


def test_model_info_with_a_token_missing_the_required_scope_is_rejected():
    now = int(time.time())
    wrong_scope = jwt.encode(
        {
            "iss": JWT_ISSUER,
            "sub": REGISTERED_CLIENT_ID,
            "aud": JWT_AUDIENCE,
            "scope": "some-other-scope",
            "iat": now,
            "exp": now + 900,
        },
        SHARED_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    resp = client.get("/model-info", headers={"Authorization": f"Bearer {wrong_scope}"})
    assert resp.status_code == 403


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


def test_score_without_a_token_is_rejected(deviating_statements):
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
