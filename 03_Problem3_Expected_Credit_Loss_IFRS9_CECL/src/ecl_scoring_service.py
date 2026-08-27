# AMEX Enterprise Credit Risk Platform -- Expected Credit Loss (IFRS9/CECL) Scoring API.
# Wraps ecl_calculator.compute_ecl() (Notebook 32's real, frozen ECL policy) as a deployable
# FastAPI service, mirroring Problem 5's real_default_service.py pattern. This service does NOT
# compute PD or severity tier itself -- it expects both as inputs, exactly as Notebook 31's own
# real pipeline does (PD from Problem 1's deployed model, severity tier from Problem 4's).
# API_KEY (see .env.example) gates every endpoint below except /health.
# Run with:
#     uvicorn ecl_scoring_service:app --host 0.0.0.0 --port 8003
import logging
import os
import secrets
from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from ecl_calculator import compute_ecl, explain_ecl, load_bundle

# Self-contained default: the bundle ships alongside this file (see Notebook 32's real output,
# copied here). Override with AMEX_ECL_BUNDLE_PATH to point elsewhere.
BUNDLE_PATH = Path(os.environ.get("AMEX_ECL_BUNDLE_PATH", str(Path(__file__).parent / "ecl_scoring_bundle.json")))
bundle = load_bundle(BUNDLE_PATH)

# ---------------------------------------------------------------------------
# Authentication -- real, enforced on every endpoint below except /health.
# Duplicated verbatim across all 8 platform services (not imported from
# shared/) so each service stays self-contained for its own Docker build
# context, matching the self-contained-policy-copy pattern already used
# elsewhere in this repo. Set API_KEY in your environment before deploying
# anywhere reachable by anyone but you -- the fallback below is published
# publicly in this file and must never be treated as a real secret.
# ---------------------------------------------------------------------------
_auth_logger = logging.getLogger(__name__ + ".auth")
_DEV_DEFAULT_API_KEY = "dev-only-CHANGE-ME-before-deploying"
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def _configured_api_key() -> str:
    key = os.environ.get("API_KEY")
    if not key:
        _auth_logger.warning(
            "API_KEY is not set -- falling back to the published dev-only default. Set API_KEY "
            "before deploying this service anywhere reachable by anyone but you."
        )
        return _DEV_DEFAULT_API_KEY
    return key


def require_api_key(presented: str = Security(_api_key_header)) -> str:
    expected = _configured_api_key()
    if not presented or not secrets.compare_digest(presented, expected):
        raise HTTPException(status_code=401, detail="Missing or invalid X-API-Key header.")
    return presented


class ECLRequest(BaseModel):
    customer_id: Optional[str] = None
    pd_12m: float = Field(..., ge=0.0, le=1.0, description="Customer's real 12-month PD from Problem 1's champion model")
    severity_tier: str = Field(..., description="One of the real severity tiers from Problem 4's model")


class ReasonCode(BaseModel):
    factor: str
    detail: str


class ECLResponse(BaseModel):
    customer_id: Optional[str] = None
    ifrs9_stage: int
    ecl_ifrs9_usd: float
    ecl_cecl_usd: float
    pd_lifetime: float
    pd_12m_macro_adj: float
    pd_lifetime_macro_adj: float
    top_reasons: List[ReasonCode] = []


app = FastAPI(
    title="AMEX Enterprise Credit Risk Platform -- Expected Credit Loss (IFRS9/CECL) API",
    description="Computes IFRS9-staged and CECL Expected Credit Loss for one customer, given "
                "their real PD and severity tier. See /model-info for the real frozen policy "
                "this service applies (Notebook 30's ECL policy, Notebook 32's deployment bundle).",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "tier_order": bundle["tier_order"]}


@app.get("/model-info", dependencies=[Depends(require_api_key)])
def model_info():
    return {
        "tier_order": bundle["tier_order"],
        "lgd_by_tier": bundle["lgd_by_tier"],
        "ead_per_account_usd": bundle["ead_per_account_usd"],
        "sicr_pd_multiple": bundle["sicr_pd_multiple"],
        "stage3_pd_threshold": bundle["stage3_pd_threshold"],
        "lifetime_pd_multiplier": bundle["lifetime_pd_multiplier"],
        "macro_scenarios": bundle["macro_scenarios"],
        "portfolio_avg_pd_12m": bundle["portfolio_avg_pd_12m"],
        "generated_at_utc": bundle.get("generated_at_utc"),
    }


@app.post("/score", response_model=ECLResponse, dependencies=[Depends(require_api_key)])
def score(request: ECLRequest):
    if request.severity_tier not in bundle["tier_order"]:
        raise HTTPException(
            status_code=422,
            detail=f"severity_tier must be one of {bundle['tier_order']}, got {request.severity_tier!r}",
        )
    try:
        result = compute_ecl(request.pd_12m, request.severity_tier, bundle)
        reasons = explain_ecl(request.pd_12m, request.severity_tier, bundle)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="ECL computation failed: " + str(exc))
    return ECLResponse(customer_id=request.customer_id, top_reasons=reasons, **result)
