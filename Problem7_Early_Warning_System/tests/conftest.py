import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "early_warning_deployment_policy.json"


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured early_warning_deployment_policy.json written by Notebook 44's actual
    run -- the real winning candidate, its real metrics, and the real monitored-feature list."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def deviating_statements(real_policy):
    """A deterministic, structurally-real statement history: 4 baseline statements with varying
    (not constant) values per monitored feature so a real standard deviation exists, followed by
    one latest statement that deviates enough to trip every feature -- exercises the real z-score
    computation end-to-end. Not real customer data (none is available in this test package), same
    established practice this repo already uses for its other JSON-policy-driven services (see
    Problem 4's tests/conftest.py) to exercise real code paths deterministically."""
    features = real_policy["monitored_features"]
    baseline = [
        {feat: float(i) for feat in features}
        for i in range(4)
    ]
    latest = {feat: 100.0 for feat in features}
    return baseline + [latest]
