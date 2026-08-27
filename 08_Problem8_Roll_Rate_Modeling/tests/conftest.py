import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "roll_rate_deployment_policy.json"


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured roll_rate_deployment_policy.json written by Notebook 48's actual run --
    full float precision feature weights/means/stds and the real empirical transition matrix."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def at_mean_statement(real_policy):
    """Every monitored feature set to its own real measured mean -- every z-score term is
    exactly 0, so the resulting severity_score should be exactly 0.0 regardless of weights."""
    means = real_policy["feature_weights"]["means"]
    return {f: means[f] for f in real_policy["monitored_features"]}
