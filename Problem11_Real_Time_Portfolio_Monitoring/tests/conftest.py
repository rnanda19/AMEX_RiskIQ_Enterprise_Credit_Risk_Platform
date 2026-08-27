import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "portfolio_monitoring_deployment_policy.json"


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured portfolio_monitoring_deployment_policy.json written by Notebook 60's
    actual run -- real control-limit sigma, baseline window, and monitored columns."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
