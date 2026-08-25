import importlib.util
import os
import sys
from pathlib import Path

import joblib
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = REPO_ROOT / "models"
SERVICE_PATH = REPO_ROOT / "src" / "dynamic_behavioral_service.py"


@pytest.fixture(scope="session")
def dbs_app():
    """Imports the exact dynamic_behavioral_service.py file shipped in src/, pointed at the real
    trained W=3 model + preprocessing artifacts shipped in models/ -- not a mock, the real thing."""
    os.environ["AMEX_DBS_MODELS_DIR"] = str(MODELS_DIR)
    spec = importlib.util.spec_from_file_location("dynamic_behavioral_service", SERVICE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["dynamic_behavioral_service"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def preprocessing_artifacts():
    return joblib.load(MODELS_DIR / "preprocessing_artifacts.joblib")
