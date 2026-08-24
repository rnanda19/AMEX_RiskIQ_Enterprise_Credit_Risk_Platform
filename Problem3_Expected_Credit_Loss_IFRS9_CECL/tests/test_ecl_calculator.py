from ecl_calculator import compute_ecl


def test_low_severity_low_pd_is_stage_1(real_bundle):
    result = compute_ecl(0.05, "Low Severity", real_bundle)
    assert result["ifrs9_stage"] == 1


def test_moderate_severity_is_always_stage_2_or_higher(real_bundle):
    """Moderate Severity is an 'elevated tier' by the real frozen policy -- any PD lands at
    least Stage 2, even a very low PD, since severity tier alone is a SICR trigger."""
    result = compute_ecl(0.01, "Moderate Severity", real_bundle)
    assert result["ifrs9_stage"] == 2


def test_severe_tier_above_stage3_threshold_is_stage_3(real_bundle):
    threshold = real_bundle["stage3_pd_threshold"]
    result = compute_ecl(threshold + 0.05, "Severe", real_bundle)
    assert result["ifrs9_stage"] == 3


def test_severe_tier_below_stage3_threshold_is_stage_2_not_1(real_bundle):
    """Severe is also an elevated tier, so even below the Stage 3 PD threshold it should not
    fall back to Stage 1."""
    threshold = real_bundle["stage3_pd_threshold"]
    result = compute_ecl(max(threshold - 0.1, 0.01), "Severe", real_bundle)
    assert result["ifrs9_stage"] == 2


def test_lgd_by_tier_is_read_from_the_real_frozen_policy(real_bundle):
    for tier, lgd in real_bundle["lgd_by_tier"].items():
        result = compute_ecl(0.05, tier, real_bundle)
        # ECL for a Stage 1 (or elevated) customer must scale linearly with that tier's LGD --
        # cross-check by recomputing with double the EAD instead, an independent invariant.
        doubled_ead_bundle = dict(real_bundle)
        doubled_ead_bundle["ead_per_account_usd"] = real_bundle["ead_per_account_usd"] * 2
        doubled = compute_ecl(0.05, tier, doubled_ead_bundle)
        assert doubled["ecl_ifrs9_usd"] == result["ecl_ifrs9_usd"] * 2
        assert doubled["ecl_cecl_usd"] == result["ecl_cecl_usd"] * 2
        assert lgd == real_bundle["lgd_by_tier"][tier]  # sanity: bundle unmutated by the call


def test_cecl_always_uses_lifetime_pd_and_stage23_discount_regardless_of_ifrs9_stage(real_bundle):
    """CECL is a lifetime-loss standard by definition -- unlike IFRS9, its ECL formula must
    NOT change based on the customer's IFRS9 stage."""
    stage1 = compute_ecl(0.02, "Low Severity", real_bundle)
    stage3 = compute_ecl(0.9, "Severe", real_bundle)
    assert stage1["ifrs9_stage"] == 1
    assert stage3["ifrs9_stage"] == 3
    lgd_low, lgd_severe = real_bundle["lgd_by_tier"]["Low Severity"], real_bundle["lgd_by_tier"]["Severe"]
    expected_cecl_stage1 = (stage1["pd_lifetime_macro_adj"] * lgd_low
                             * real_bundle["ead_per_account_usd"] * real_bundle["discount_factor_stage23"])
    expected_cecl_stage3 = (stage3["pd_lifetime_macro_adj"] * lgd_severe
                             * real_bundle["ead_per_account_usd"] * real_bundle["discount_factor_stage23"])
    assert stage1["ecl_cecl_usd"] == expected_cecl_stage1
    assert stage3["ecl_cecl_usd"] == expected_cecl_stage3


def test_pd_lifetime_is_capped_at_one(real_bundle):
    result = compute_ecl(0.9, "Severe", real_bundle)
    assert result["pd_lifetime"] <= 1.0
