import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "executive_dashboard_deployment_policy.json"
DATA_PATH = REPO_ROOT / "src" / "executive_dashboard_data.json"


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured executive_dashboard_deployment_policy.json written by Notebook 72's
    actual run -- real included/excluded problem lists and total platform net value."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def real_dashboard_data():
    """The real, measured executive_dashboard_data.json -- Notebook 71's real per-problem
    rollup of all 13 prior problems."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
