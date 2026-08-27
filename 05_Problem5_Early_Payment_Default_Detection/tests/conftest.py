import importlib.util
import os
import sys
from pathlib import Path

import joblib
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = REPO_ROOT / "models"
SERVICE_PATH = REPO_ROOT / "src" / "early_default_service.py"
TEST_API_KEY = "pytest-only-test-key"


@pytest.fixture(scope="session")
def epd_app():
    """Imports the exact early_default_service.py file shipped in src/, pointed at the real
    trained model + preprocessing artifacts shipped in models/ -- not a mock, the real thing."""
    os.environ["AMEX_EPD_MODELS_DIR"] = str(MODELS_DIR)
    os.environ["API_KEY"] = TEST_API_KEY
    spec = importlib.util.spec_from_file_location("early_default_service", SERVICE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["early_default_service"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def preprocessing_artifacts():
    return joblib.load(MODELS_DIR / "preprocessing_artifacts.joblib")
