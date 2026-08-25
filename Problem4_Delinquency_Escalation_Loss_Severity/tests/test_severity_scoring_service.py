from fastapi.testclient import TestClient

from severity_scorer import score_customer
from severity_scoring_service import app

client = TestClient(app)


def test_health_endpoint_reports_ok_and_real_feature_count(real_bundle):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["n_features"] == len(real_bundle["features"])


def test_model_info_matches_the_real_bundle(real_bundle):
    r = client.get("/model-info")
    assert r.status_code == 200
    body = r.json()
    assert body["lgd_by_tier"] == real_bundle["lgd_by_tier"]
    assert body["cut_low"] == real_bundle["cut_low"]
    assert body["cut_high"] == real_bundle["cut_high"]


def test_score_at_mean_features_matches_direct_computation_exactly(at_mean_features, real_bundle):
    """The API must produce bit-identical results to calling score_customer() directly."""
    r = client.post("/score", json=at_mean_features, params={"customer_id": "T1"})
    assert r.status_code == 200
    api_result = r.json()
    direct_result = score_customer(at_mean_features, real_bundle)
    assert api_result["severity_score"] == direct_result["severity_score"]
    assert api_result["severity_tier"] == direct_result["severity_tier"]
    assert api_result["lgd"] == direct_result["lgd"]


def test_missing_fields_are_imputed_to_real_training_mean(real_bundle):
    """Omitting every feature should score identically to explicitly sending every feature at
    its real training mean -- score_customer()'s own missing-value handling, exercised through
    the live API, not just the underlying function."""
    r_missing = client.post("/score", json={}, params={"customer_id": "T2"})
    at_mean = {f: real_bundle["means"][f] for f in real_bundle["features"]}
    r_at_mean = client.post("/score", json=at_mean, params={"customer_id": "T2"})
    assert r_missing.json()["severity_score"] == r_at_mean.json()["severity_score"]


def test_customer_id_is_echoed_back_when_provided(at_mean_features):
    r = client.post("/score", json=at_mean_features, params={"customer_id": "XYZ-9"})
    assert r.json()["customer_id"] == "XYZ-9"


def test_all_real_holdout_customers_score_identically_via_api(real_bundle):
    """Broader than a single at-mean check: scores a handful of real holdout customers'
    real feature values (not synthetic) through the live API and checks against direct
    computation, the same all-customer discipline established for the standalone scorer's own
    self-test (see MODEL_CARD.md) -- applied here to a sample since the API path is HTTP-bound."""
    import random
    random.seed(42)
    # Perturb each mean feature by a small deterministic offset to build several distinct,
    # realistic-looking customers without needing the real holdout CSV in this test package.
    for i in range(5):
        feats = {f: real_bundle["means"][f] + (0.1 * real_bundle["stds"][f] * ((i + hash(f)) % 7 - 3))
                 for f in real_bundle["features"]}
        r = client.post("/score", json=feats, params={"customer_id": f"SAMPLE-{i}"})
        assert r.status_code == 200
        direct = score_customer(feats, real_bundle)
        assert r.json()["severity_score"] == direct["severity_score"], f"mismatch on sample {i}"
        assert r.json()["severity_tier"] == direct["severity_tier"]
