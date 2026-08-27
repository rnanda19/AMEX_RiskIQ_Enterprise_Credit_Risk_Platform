import json
import os
import sys
import tempfile
from pathlib import Path

import polars as pl
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "profitability_deployment_policy.json"

# A small, synthetic-but-structurally-real profile fixture: same real column names/dtypes as
# the real ~38MB profitability_scored_profile.parquet (see ../data/README.md for why the real
# file isn't committed).
_FIXTURE_DIR = tempfile.mkdtemp(prefix="p13_profile_fixture_")
_FIXTURE_PATH = Path(_FIXTURE_DIR) / "profitability_scored_profile.parquet"

_FIXTURE_ROWS = [
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
pl.DataFrame(_FIXTURE_ROWS).write_parquet(_FIXTURE_PATH)

# Must be set before profitability_scoring_lookup_service (which reads this at import time via
# its module-level PROFILE_PATH / `pl.read_parquet(...)`) is imported by the test module below.
os.environ["AMEX_P13_PROFILE_PATH"] = str(_FIXTURE_PATH)


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured profitability_deployment_policy.json written by Notebook 68's actual
    run -- real tier cutpoints and labeled revenue ASSUMPTIONs."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def fixture_rows():
    return _FIXTURE_ROWS
