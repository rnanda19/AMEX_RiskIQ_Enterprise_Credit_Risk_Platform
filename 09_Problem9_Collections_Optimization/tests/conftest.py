import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

POLICY_PATH = REPO_ROOT / "src" / "collections_deployment_policy.json"


@pytest.fixture(scope="session")
def real_policy():
    """The real, measured collections_deployment_policy.json written by Notebook 52's actual
    run -- real feature means, tier cutpoints, and reproduction metrics."""
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def mean_statement(real_policy):
    """Every monitored feature set to its own real measured mean."""
    means = real_policy["feature_weights"]["means"]
    return {f: means[f] for f in real_policy["monitored_features"]}
