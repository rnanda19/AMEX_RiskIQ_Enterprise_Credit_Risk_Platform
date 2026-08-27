import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

BUNDLE_PATH = REPO_ROOT / "reports" / "validation_deployment" / "severity_scoring_bundle.json"


@pytest.fixture(scope="session")
def real_bundle():
    """The real, measured severity_scoring_bundle.json written by Notebook 28's actual run --
    full float precision, not a synthetic fixture. See MODEL_CARD.md for why full precision
    (not a rounded display copy) matters here specifically."""
    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def at_mean_features(real_bundle):
    """Every feature set to its own real measured mean -- every z-score is exactly 0, so the
    resulting severity_score should be exactly 0.0 regardless of weights/directions."""
    return {f: real_bundle["means"][f] for f in real_bundle["features"]}
