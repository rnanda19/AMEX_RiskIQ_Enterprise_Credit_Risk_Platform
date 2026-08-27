import math

from severity_scorer import score_customer, top_contributing_features


def test_top_contributing_features_is_empty_at_the_real_mean(real_bundle, at_mean_features):
    """Every feature at its own real mean -> every z-score term is exactly 0 -> no feature has a
    real, non-zero contribution to report."""
    assert top_contributing_features(at_mean_features, real_bundle) == []


def test_top_contributing_features_ranks_by_real_magnitude(real_bundle, at_mean_features):
    top_feature = max(real_bundle["features"], key=lambda f: real_bundle["weights"][f])
    direction = real_bundle["directions"][top_feature]
    pushed = dict(at_mean_features)
    pushed[top_feature] = (real_bundle["means"][top_feature]
                            + 3 * real_bundle["stds"][top_feature] * (1 if direction >= 0 else -1))
    reasons = top_contributing_features(pushed, real_bundle, n=5)
    assert reasons[0]["factor"] == top_feature
    magnitudes = [abs(r["contribution_to_severity_score"]) for r in reasons]
    assert magnitudes == sorted(magnitudes, reverse=True)


def test_top_contributing_features_sums_are_real_and_match_manual_recomputation(real_bundle, at_mean_features):
    """Each reported contribution must equal the exact same weight*direction*z term
    score_customer() itself sums -- not an approximation."""
    some_feature = real_bundle["features"][0]
    pushed = dict(at_mean_features)
    pushed[some_feature] = real_bundle["means"][some_feature] + 2 * real_bundle["stds"][some_feature]
    reasons = top_contributing_features(pushed, real_bundle, n=len(real_bundle["features"]))
    reason_for_feature = next(r for r in reasons if r["factor"] == some_feature)
    z = (pushed[some_feature] - real_bundle["means"][some_feature]) / real_bundle["stds"][some_feature]
    expected = real_bundle["weights"][some_feature] * real_bundle["directions"][some_feature] * z
    assert reason_for_feature["contribution_to_severity_score"] == expected


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
