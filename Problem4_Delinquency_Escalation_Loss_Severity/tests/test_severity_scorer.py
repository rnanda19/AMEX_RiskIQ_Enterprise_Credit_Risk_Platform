import math

from severity_scorer import score_customer


def test_all_features_at_mean_gives_zero_score(real_bundle, at_mean_features):
    result = score_customer(at_mean_features, real_bundle)
    assert result["severity_score"] == 0.0


def test_zero_score_lands_in_the_real_cut_low_cut_high_band(real_bundle, at_mean_features):
    """With score == 0.0, the tier must be whichever real tier the measured cut_low/cut_high
    band actually places it in -- computed from the bundle, not hardcoded, so this test stays
    correct if the model is retrained and the cutpoints shift."""
    result = score_customer(at_mean_features, real_bundle)
    if 0.0 <= real_bundle["cut_low"]:
        expected_tier = real_bundle["tier_order"][0]
    elif 0.0 <= real_bundle["cut_high"]:
        expected_tier = real_bundle["tier_order"][1]
    else:
        expected_tier = real_bundle["tier_order"][2]
    assert result["severity_tier"] == expected_tier
    assert result["lgd"] == real_bundle["lgd_by_tier"][expected_tier]


def test_missing_feature_as_none_is_treated_as_the_real_mean(real_bundle, at_mean_features):
    partial = dict(at_mean_features)
    some_feature = real_bundle["features"][0]
    del partial[some_feature]  # .get() returns None for a key not present at all
    result_missing = score_customer(partial, real_bundle)
    result_full = score_customer(at_mean_features, real_bundle)
    assert result_missing["severity_score"] == result_full["severity_score"]


def test_missing_feature_as_nan_is_treated_the_same_as_none(real_bundle, at_mean_features):
    """Regression test for a real bug: pandas/numpy represent a missing statement value as
    float('nan'), not None, once loaded from CSV -- both must be handled identically."""
    as_none = dict(at_mean_features)
    as_nan = dict(at_mean_features)
    some_feature = real_bundle["features"][1]
    as_none[some_feature] = None
    as_nan[some_feature] = float("nan")
    result_none = score_customer(as_none, real_bundle)
    result_nan = score_customer(as_nan, real_bundle)
    assert result_none["severity_score"] == result_nan["severity_score"]
    assert not math.isnan(result_nan["severity_score"])


def test_higher_weighted_positive_direction_feature_raises_score(real_bundle, at_mean_features):
    """Push the single most-heavily-weighted feature two std devs above its mean, in its own
    real signed direction, and confirm the score moves in the expected direction -- a sanity
    check on the weight*direction*z formula using the real, measured weights."""
    top_feature = max(real_bundle["features"], key=lambda f: real_bundle["weights"][f])
    direction = real_bundle["directions"][top_feature]
    pushed = dict(at_mean_features)
    pushed[top_feature] = (real_bundle["means"][top_feature]
                            + 2 * real_bundle["stds"][top_feature] * (1 if direction >= 0 else -1))
    baseline = score_customer(at_mean_features, real_bundle)
    result = score_customer(pushed, real_bundle)
    assert result["severity_score"] > baseline["severity_score"]


def test_score_uses_alphabetical_summation_order_matching_notebook_27(real_bundle, at_mean_features):
    """Regression test for a real bug: summing the same terms in weight-sorted (not
    alphabetical) order produced a bit-level-different float result that could flip a tier
    near a cutpoint. Manually recompute in alphabetical order and require an exact match."""
    manual_score = 0.0
    for feat in sorted(real_bundle["features"]):
        z = (at_mean_features[feat] - real_bundle["means"][feat]) / real_bundle["stds"][feat]
        manual_score += real_bundle["weights"][feat] * real_bundle["directions"][feat] * z
    result = score_customer(at_mean_features, real_bundle)
    assert result["severity_score"] == manual_score
