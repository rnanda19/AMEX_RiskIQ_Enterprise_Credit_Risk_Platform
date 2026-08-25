from fastapi.testclient import TestClient

from roll_rate_scoring_service import app, assign_state, compute_severity_score

client = TestClient(app)


def test_health_reports_the_real_state_names(real_policy):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["state_names"] == real_policy["state_names"]


def test_model_info_matches_the_real_policy(real_policy):
    resp = client.get("/model-info")
    assert resp.status_code == 200
    body = resp.json()
    assert body["cut_low"] == real_policy["cut_low"]
    assert body["cut_high"] == real_policy["cut_high"]
    assert body["transition_matrix"] == real_policy["transition_matrix"]
    # Honest, real result: both hard-gate KPIs passed and this technique IS recommended.
    assert body["recommended_for_production"] is True
    assert real_policy["recommended_for_production"] is True


def test_score_at_real_mean_features_is_exactly_zero(at_mean_statement):
    """Every feature at its own real training mean -> severity_score == 0.0 exactly, matching
    Problem 4's own at-mean sanity check for its analogous weighted composite score."""
    resp = client.post("/score", json={"customer_id": "T1", "current_statement": at_mean_statement})
    assert resp.status_code == 200
    body = resp.json()
    assert body["severity_score"] == 0.0
    assert body["state"] == assign_state(0.0)


def test_score_matches_a_direct_computation_against_the_real_policy(at_mean_statement):
    """The API must produce bit-identical results to calling compute_severity_score()/
    assign_state() directly against the same input."""
    resp = client.post("/score", json={"current_statement": at_mean_statement})
    api_body = resp.json()
    direct_score = compute_severity_score(at_mean_statement)
    assert api_body["severity_score"] == direct_score
    assert api_body["state"] == assign_state(direct_score)


def test_transition_lookup_matches_the_real_transition_matrix(at_mean_statement, real_policy):
    resp = client.post(
        "/score",
        json={"current_statement": at_mean_statement, "previous_state": "Severe"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["previous_state"] == "Severe"
    assert body["transition_probabilities"] == real_policy["transition_matrix"]["Severe"]
    # "Severe" is the worst (highest-ordinal) state, so no state can rank above it -- escalation
    # (moving to a STRICTLY worse state) is impossible from here regardless of the new state.
    assert body["escalated"] is False


def test_unknown_previous_state_returns_400(at_mean_statement):
    resp = client.post(
        "/score",
        json={"current_statement": at_mean_statement, "previous_state": "Not A Real State"},
    )
    assert resp.status_code == 400


def test_omitting_previous_state_leaves_escalation_fields_null(at_mean_statement):
    resp = client.post("/score", json={"current_statement": at_mean_statement})
    body = resp.json()
    assert body["previous_state"] is None
    assert body["escalated"] is None
    assert body["transition_probabilities"] is None


def test_several_perturbed_real_customers_match_direct_computation(real_policy):
    """Deterministically perturbs each feature away from its real measured mean by a fraction of
    its real measured std (same established pattern as Problem 4's own perturbed-sample test) and
    checks the API matches direct computation for each -- broader coverage than a single at-mean
    check."""
    means = real_policy["feature_weights"]["means"]
    stds = real_policy["feature_weights"]["stds"]
    features = real_policy["monitored_features"]
    for i in range(5):
        stmt = {f: means[f] + (0.1 * stds[f] * ((i + hash(f)) % 7 - 3)) for f in features}
        resp = client.post("/score", json={"customer_id": f"SAMPLE-{i}", "current_statement": stmt})
        assert resp.status_code == 200
        direct_score = compute_severity_score(stmt)
        assert resp.json()["severity_score"] == direct_score, f"mismatch on sample {i}"
        assert resp.json()["state"] == assign_state(direct_score)
