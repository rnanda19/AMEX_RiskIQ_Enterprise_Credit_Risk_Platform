"""Tests for shared/tiers.py, using Problem 2's real risk_tier_policy.json
band shape (pd_lower/pd_upper/risk_tier/tier_order) as the fixture, so this
is a faithful re-check of assign_tier()'s actual real-world usage, not an
abstract shape nobody uses."""
import pytest

from shared.tiers import assign_band

REAL_BUSINESS_RULE_BANDS = [
    {"risk_tier": "Prime", "tier_order": 1, "pd_lower": 0.0, "pd_upper": 0.05},
    {"risk_tier": "Near-Prime", "tier_order": 2, "pd_lower": 0.05, "pd_upper": 0.15},
    {"risk_tier": "Subprime", "tier_order": 3, "pd_lower": 0.15, "pd_upper": 0.35},
    {"risk_tier": "High Risk", "tier_order": 4, "pd_lower": 0.35, "pd_upper": 1.01},
]


def _assign(pd_value):
    return assign_band(
        pd_value, REAL_BUSINESS_RULE_BANDS,
        lower_key="pd_lower", upper_key="pd_upper",
        label_key="risk_tier", order_key="tier_order",
    )


@pytest.mark.parametrize("pd_value,expected_tier", [
    (0.0, "Prime"),
    (0.049, "Prime"),
    (0.05, "Near-Prime"),   # lower bound is inclusive -- boundary belongs to the higher tier
    (0.10, "Near-Prime"),
    (0.15, "Subprime"),
    (0.34999, "Subprime"),
    (0.35, "High Risk"),
    (0.99, "High Risk"),
    (1.0, "High Risk"),
])
def test_real_business_rule_bands_assign_correct_tier(pd_value, expected_tier):
    assert _assign(pd_value) == expected_tier


def test_value_above_policy_range_falls_back_to_last_band():
    """1.01 is the documented upper edge (exclusive) of the top band -- a
    value at or beyond it isn't inside ANY band's half-open interval, so it
    falls back to the last (highest-order) band, matching the original
    implementation's real fallback behavior."""
    assert _assign(1.5) == "High Risk"


def test_negative_value_also_falls_back_to_last_band():
    """A value below the lowest band's lower bound also matches no band and
    falls back to the last band -- this is the original's real (if
    slightly surprising) behavior for out-of-range input, preserved here
    rather than silently changed."""
    assert _assign(-0.1) == "High Risk"


def test_unsorted_input_bands_are_sorted_before_assignment():
    """Bands passed out of tier_order should still assign correctly --
    assign_band() sorts internally, same as the original."""
    shuffled = [REAL_BUSINESS_RULE_BANDS[2], REAL_BUSINESS_RULE_BANDS[0],
                REAL_BUSINESS_RULE_BANDS[3], REAL_BUSINESS_RULE_BANDS[1]]
    result = assign_band(0.02, shuffled, "pd_lower", "pd_upper", "risk_tier", "tier_order")
    assert result == "Prime"
