#!/usr/bin/env python3
"""Generate the small, synthetic-but-structurally-real profile fixture used to
docker-run Problem 12's and Problem 13's real containers in CI (see
.github/workflows/docker-verify.yml).

This is NOT new or different data -- it is the exact same fixture (same column
names, dtypes, and two-row shape) already committed and used by that problem's
own pytest suite. See:
  - 12_Problem12_360_Customer_Intelligence/tests/conftest.py
  - 13_Problem13_Risk_Adjusted_Profitability_Modeling/tests/conftest.py

The real per-customer parquet files this fixture stands in for (~29-38MB each)
are deliberately excluded from this public repo -- see each problem's own
data/README.md.
"""
import argparse
from pathlib import Path

import polars as pl

P12_FIXTURE_ROWS = [
    {
        "customer_ID": "CUST-COLLECTIONS-ELIGIBLE",
        "STATIC_PD": 0.42,
        "DYNAMIC_PD": 0.55,
        "PD_TREND": 0.13,
        "RISK_LEVEL": "High Risk",
        "TREND_SEGMENT": "Trending Worse",
        "CREDIT_LINE_ACTION": "Reduce Limit",
        "COLLECTIONS_ELIGIBLE": True,
        "PROPENSITY_TO_CURE": 0.18,
        "TREATMENT_TIER": "Priority Outreach",
        "UNIFIED_RISK_SCORE": 0.51,
        "UNIFIED_RISK_GRADE": "High Risk",
    },
    {
        "customer_ID": "CUST-NOT-ELIGIBLE",
        "STATIC_PD": 0.02,
        "DYNAMIC_PD": 0.01,
        "PD_TREND": -0.01,
        "RISK_LEVEL": "Low Risk",
        "TREND_SEGMENT": "Trending Better",
        "CREDIT_LINE_ACTION": "Increase Limit",
        "COLLECTIONS_ELIGIBLE": False,
        "PROPENSITY_TO_CURE": None,
        "TREATMENT_TIER": None,
        "UNIFIED_RISK_SCORE": 0.014,
        "UNIFIED_RISK_GRADE": "Low Risk",
    },
]

P13_FIXTURE_ROWS = [
    {
        "customer_ID": "CUST-HIGH-PROFIT",
        "UNIFIED_RISK_SCORE": 0.02,
        "SPEND_PERCENTILE_RANK": 0.95,
        "REVENUE_MULTIPLIER": 1.75,
        "REVENUE_PER_ACCOUNT_USD": 113.75,
        "PD_ADJUSTED_REVENUE_USD": 111.48,
        "EXPECTED_LOSS_USD": 45.0,
        "PROFITABILITY_SCORE": 66.48,
        "PROFITABILITY_TIER": "High Profitability",
    },
    {
        "customer_ID": "CUST-LOW-PROFIT",
        "UNIFIED_RISK_SCORE": 0.85,
        "SPEND_PERCENTILE_RANK": 0.05,
        "REVENUE_MULTIPLIER": 0.42,
        "REVENUE_PER_ACCOUNT_USD": 27.30,
        "PD_ADJUSTED_REVENUE_USD": 4.10,
        "EXPECTED_LOSS_USD": 1912.50,
        "PROFITABILITY_SCORE": -1908.40,
        "PROFITABILITY_TIER": "Low Profitability",
    },
]

FIXTURES = {"p12": P12_FIXTURE_ROWS, "p13": P13_FIXTURE_ROWS}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", required=True, choices=sorted(FIXTURES))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    pl.DataFrame(FIXTURES[args.module]).write_parquet(args.out)
    print(f"Wrote {len(FIXTURES[args.module])}-row fixture to {args.out}")


if __name__ == "__main__":
    main()
