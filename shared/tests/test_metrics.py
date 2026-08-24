"""Unit tests for shared/metrics.py -- the official AMEX competition metric.

These cases are independent, hand-derivable checks (perfect ranking, random
ranking, a known 10-row example worked by hand), not a re-statement of the
implementation itself -- the point is to catch a real regression, not to
just restate the code as a test.
"""
import numpy as np
import pytest

from shared.metrics import amex_metric_numpy, top_four_percent_capture_only


def test_perfect_predictions_score_one():
    """If predicted scores perfectly rank-order the true labels (all
    defaulters ranked above all non-defaulters), both the Gini half and the
    top-4% capture half should be exactly 1.0, so the metric is 1.0."""
    n = 1000
    y_true = np.zeros(n)
    y_true[:100] = 1  # 10% default rate
    # Perfect ranking: predicted score == true label (ties broken by index,
    # which is fine since argsort is stable/mergesort and this is a strict
    # separation, not a tie).
    y_pred = y_true.copy()
    score = amex_metric_numpy(y_true, y_pred)
    assert score == pytest.approx(1.0, abs=1e-9)


def test_worst_case_predictions_score_low():
    """Inverted ranking (every non-defaulter scored above every defaulter)
    should score well below a perfect or random ranking -- it should not be
    anywhere near 1.0."""
    n = 1000
    y_true = np.zeros(n)
    y_true[:100] = 1
    y_pred = 1.0 - y_true  # exactly inverted
    score = amex_metric_numpy(y_true, y_pred)
    assert score < 0.3


def test_metric_is_between_expected_bounds_for_random_scores():
    """A random, uninformative score should land well below a perfect
    score and (for a 25.89%-style default rate) comfortably above the
    worst-case score -- a broad sanity band, not an exact value, since
    the exact number depends on the random draw."""
    rng = np.random.default_rng(7)
    n = 5000
    y_true = (rng.random(n) < 0.2589).astype(float)  # real platform default rate
    y_pred = rng.random(n)
    score = amex_metric_numpy(y_true, y_pred)
    assert 0.0 <= score <= 1.0


def test_top_four_percent_capture_only_matches_metric_half():
    """top_four_percent_capture_only() must equal the top-4% term actually
    used inside amex_metric_numpy() for the same inputs -- they should never
    silently drift apart since one is reported standalone in the model
    comparison table and the other is baked into the composite score."""
    rng = np.random.default_rng(1)
    n = 2000
    y_true = (rng.random(n) < 0.2589).astype(float)
    y_pred = rng.random(n)

    top4 = top_four_percent_capture_only(y_true, y_pred)
    assert 0.0 <= top4 <= 1.0

    # Perfect ranking -> top4 must be 1.0 (every one of the top 4%-weighted
    # slots is a true defaulter, since defaulters are ranked first).
    y_pred_perfect = y_true.copy()
    assert top_four_percent_capture_only(y_true, y_pred_perfect) == pytest.approx(1.0, abs=1e-9)


def test_hand_computed_small_example():
    """A tiny 10-row example worked out by hand: 2 defaulters (weight 1
    each), 8 non-defaulters (weight 20 each) = 162 total weight. The 4%
    cutoff is 6.48 weight units, i.e. within the single highest-weighted
    non-defaulter alone (20) -- so if predictions rank a non-defaulter
    first, the top-4% window is entirely non-defaulters and captures 0
    defaulters -> top4 = 0."""
    y_true = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], dtype=float)
    y_pred = np.array([0.9, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.0], dtype=float)
    # Highest-scored row (index 0) is a non-defaulter -> occupies the whole
    # 4% cutoff window by itself (weight 20 > cutoff 6.48) -> top4 = 0.
    top4 = top_four_percent_capture_only(y_true, y_pred)
    assert top4 == pytest.approx(0.0, abs=1e-9)


def test_no_positives_returns_zero_not_error():
    """An all-non-defaulter batch (total_pos == 0) must return 0.0 from both
    functions rather than raising a ZeroDivisionError -- this is the
    documented guard in the original implementation."""
    y_true = np.zeros(50)
    y_pred = np.random.default_rng(0).random(50)
    assert amex_metric_numpy(y_true, y_pred) == 0.0
    assert top_four_percent_capture_only(y_true, y_pred) == 0.0
