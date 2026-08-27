import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "credit_line_deployment_policy.json"


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured credit_line_deployment_policy.json written by Notebook 56's actual
    run -- real risk-level/trend cutpoints and the real action-tier matrix."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
