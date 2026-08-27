import json
import os
import sys
import tempfile
from pathlib import Path

import polars as pl
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "customer_intelligence_deployment_policy.json"

# A small, synthetic-but-structurally-real profile fixture: same real column names/dtypes as
# the real ~29MB unified_customer_profile.parquet (see ../data/README.md for why the real file
# isn't committed), with two rows exercising the real collections-eligible vs. not branch the
# deployed service actually has to handle.
_FIXTURE_DIR = tempfile.mkdtemp(prefix="p12_profile_fixture_")
_FIXTURE_PATH = Path(_FIXTURE_DIR) / "unified_customer_profile.parquet"

_FIXTURE_ROWS = [
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
pl.DataFrame(_FIXTURE_ROWS).write_parquet(_FIXTURE_PATH)

# Must be set before customer_intelligence_lookup_service (which reads this at import time via
# its module-level PROFILE_PATH / `pl.read_parquet(...)`) is imported by the test module below.
os.environ["AMEX_P12_PROFILE_PATH"] = str(_FIXTURE_PATH)


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured customer_intelligence_deployment_policy.json written by Notebook 64's
    actual run -- real composite weights and grade cutpoints."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def fixture_rows():
    return _FIXTURE_ROWS
