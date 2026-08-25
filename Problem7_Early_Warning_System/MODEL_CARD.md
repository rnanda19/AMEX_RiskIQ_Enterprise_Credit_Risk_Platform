# Model Card -- Early Warning System

## Model details

- **Technique:** rolling z-score deviation-count detector -- NOT a trained classifier. For each of 89 monitored features, computes a customer's own trailing baseline mean/std (from statements before the latest one, minimum 4 required) and flags a feature as "deviating" when the latest statement's value is >= 2.0 standard deviations away.
- **Random seed:** 42 (fixed platform-wide, applies to the candidate sweep's holdout sampling).
- **Built by:** `43_early_warning_system_modeling.ipynb`, validated by `44_early_warning_system_validation_deployment.ipynb`.
- **Frozen policy:** the real z-threshold, minimum-baseline-length, winning candidate, and full monitored-feature list are frozen in `docs/early_warning_deployment_policy.json` (also shipped self-contained in `src/`).

## Intended use

A lightweight, explainable, no-retraining-required complement to Problem 6's trained recency model -- flag an account when enough of its monitored features deviate from that SAME account's own recent baseline at once. Intended as a candidate cheap early-warning layer, not a replacement for Problem 1 or Problem 6.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real holdout customers scored: 88,389. Base holdout default rate: 25.62%.
- Candidate minimum-deviation-count thresholds swept: 1, 2, 3, 5, 8 (all real, reproduced).

## Evaluation (real, measured)

- Secondary threshold-free metrics (reproduced): ROC-AUC 0.6607, PR-AUC 0.4014, AUC retention vs. Problem 1's full-history champion 68.68%.
- Winning candidate (min. deviation count = 8, reproduced): 37,675 accounts alerted (42.6% of holdout), default rate among alerted 36.06%, lift 1.41x, precision 0.3606, recall 0.6000, F1 0.4504, MCC 0.2062.
- **No candidate met the KPI target on this run.**
- **Deployment status: NOT RECOMMENDED FOR PRODUCTION** -- reported honestly in every deliverable (report, dashboard, SMART suggestions, this card), not glossed over. Estimated Net Benefit / Cycle if deployed as-is anyway (measured, net of false-positive review cost): $4,224,135; illustrative ROI/payback 168,865% / ~0.0 months -- shown for completeness, but the statistical KPI gate was not cleared.

## Limitations

- This is a rule-based statistical detector, not a trained/calibrated model -- its "score" (deviation count) is not a probability and should not be interpreted as one.
- Requires >= 4 prior statements to form a baseline before it can evaluate a 5th (latest) statement; cannot score genuinely new accounts.
- A v2 enhancement attempt (an earlier draft of Notebooks 46-47) was built to try to improve on this result, showed genuine but insufficient improvement, and was deliberately abandoned -- see `ROADMAP.md` and this problem's own notebooks for that history.
- No demographic/protected-attribute data exists in this dataset (same limitation as Problem 1/2).

## How this is tested going forward

`tests/` drives the REAL deployed FastAPI alert service end-to-end via `TestClient` against the real, measured `early_warning_deployment_policy.json` -- covering `/health`, `/model-info` (asserting the real, honestly-not-recommended result), a bit-exact match between the API and calling `compute_early_warning()` directly, the alert-threshold boundary logic, the too-few-statements 422 error path, and the zero-variance-baseline guard.

## Deployment

`src/real_time_alert_service.py` defaults `AMEX_EWS_POLICY_PATH` to the real frozen policy JSON shipped alongside it in `src/` (self-contained -- no local machine path needed; a hardcoded local Windows path was found and fixed here during this hardening pass, the same class of bug already fixed once for Problem 5 -- see `CHANGELOG.md`). Run locally with `uvicorn real_time_alert_service:app --port 8007` from `src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```
