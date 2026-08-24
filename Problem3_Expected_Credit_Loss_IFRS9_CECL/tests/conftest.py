import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

BUNDLE_PATH = REPO_ROOT / "reports" / "validation_deployment" / "ecl_scoring_bundle.json"


@pytest.fixture(scope="session")
def real_bundle():
    """The real, measured ecl_scoring_bundle.json written by Notebook 32's actual run --
    not a synthetic fixture. Every test in this package exercises the real frozen policy."""
    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
