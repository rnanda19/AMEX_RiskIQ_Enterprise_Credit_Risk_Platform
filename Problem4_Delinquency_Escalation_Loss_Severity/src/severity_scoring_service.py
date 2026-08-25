# AMEX Enterprise Credit Risk Platform -- Delinquency Escalation Severity Scoring API.
# Wraps severity_scorer.score_customer() (Notebook 27's real, frozen weighted-sum severity
# model -- 243 real D_* engineered features) as a deployable FastAPI service, mirroring
# Problem 5's early_default_service.py pattern.
# Run with:
#     uvicorn severity_scoring_service:app --host 0.0.0.0 --port 8004
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, create_model

from severity_scorer import load_bundle, score_customer

# Self-contained default: the bundle ships alongside this file. Override with
# AMEX_SEVERITY_BUNDLE_PATH to point elsewhere.
BUNDLE_PATH = Path(os.environ.get("AMEX_SEVERITY_BUNDLE_PATH", str(Path(__file__).parent / "severity_scoring_bundle.json")))
bundle = load_bundle(BUNDLE_PATH)

# One optional float field per real feature the model was fit on -- a missing field is treated
# exactly like a missing statement value (imputed to that feature's real training mean), same as
# score_customer()'s own _is_missing() handling.
_schema_fields = {feat: (Optional[float], None) for feat in bundle["features"]}
CustomerFeatures = create_model("CustomerFeatures", **_schema_fields)


class SeverityResponse(BaseModel):
    customer_id: Optional[str] = None
    severity_score: float
    severity_tier: str
    lgd: float


app = FastAPI(
    title="AMEX Enterprise Credit Risk Platform -- Delinquency Escalation Severity Scoring API",
    description="Scores one customer's real D_* engineered features into a 3-tier escalation "
                "severity score and LGD. See /model-info for the real frozen policy (weights, "
                "cutpoints, tier LGDs) this service applies, from Notebook 27's real run.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "tier_order": bundle["tier_order"], "n_features": len(bundle["features"])}


@app.get("/model-info")
def model_info():
    return {
        "tier_order": bundle["tier_order"],
        "lgd_by_tier": bundle["lgd_by_tier"],
        "cut_low": bundle["cut_low"],
        "cut_high": bundle["cut_high"],
        "n_features": len(bundle["features"]),
        "generated_at_utc": bundle.get("generated_at_utc"),
    }


@app.post("/score", response_model=SeverityResponse)
def score(features: CustomerFeatures, customer_id: Optional[str] = None):
    feature_dict = features.model_dump() if hasattr(features, "model_dump") else features.dict()
    try:
        result = score_customer(feature_dict, bundle)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Severity scoring failed: " + str(exc))
    return SeverityResponse(customer_id=customer_id, **result)
