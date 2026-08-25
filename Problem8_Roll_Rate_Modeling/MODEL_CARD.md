# Model Card -- Roll-Rate Modeling

## Model details

- **Technique:** a fitted composite severity score (89 real correlation-filtered features, z-scored, weighted, direction-signed) cut into 3 states by 2 real cutpoints, plus an empirical Markov transition-probability matrix fit across consecutive statements -- NOT a trained classifier.
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `47_roll_rate_modeling_modeling.ipynb`, validated by `48_roll_rate_modeling_validation_deployment.ipynb`.
- **Frozen policy:** the real feature weights/means/stds, state cutpoints, and full empirical transition matrix are frozen in `docs/roll_rate_deployment_policy.json` (also shipped self-contained in `src/`).

## Intended use

Assign a customer's current statement a delinquency-severity state (Low/Moderate/Severe) and, given their previous state, look up the real empirically observed probability of transitioning to each next state -- a classic roll-rate view for collections prioritization, cross-validated against Problem 6's independently-trained dynamic PD.

## Training data

- Source: Kaggle -- American Express Default Prediction (same real customer population as Problem 1).
- Real holdout customers scored: 91,783. Transition-eligible consecutive-statement pairs: 90,783.
- Cross-stratified against Problem 6's real dynamic PD output (89,569 stratification-eligible customers, 98.66% coverage).

## Evaluation (real, measured)

- State population split (measured): Low Severity 31.7% / Moderate Severity 31.0% / Severe 37.4%.
- Monotonic default rate across states (reproduced): True -- Low 0.57% -> Moderate 9.16% -> Severe 61.24%.
- Severe/Low default-rate ratio (reproduced): 107.21x, 95% CI lower bound 92.78x (target >= 1.5x, PASS).
- Coherence gap P(Severe->Severe) - P(Low->Severe) (reproduced): 0.9557, 95% CI lower bound 0.9550 (target > 0, PASS).
- Escalation-magnitude ROC-AUC / PR-AUC (reproduced): 0.5126 / 0.2635.
- Cross-validation vs. Problem 6's real dynamic PD (measured): z = 8.80, p < 0.001 -- statistically significant agreement between the two independently-built techniques.
- Split-half severity-score PSI: 0.0001 (target < 0.10, PASS).
- **Deployment status: RECOMMENDED FOR PRODUCTION** -- both hard-gate KPIs (monotonicity and coherence) met on this run.

## Limitations

- The composite score's weights/cutpoints are fit once on this dataset's real correlation structure -- not re-validated against an external portfolio.
- Escalation-magnitude discrimination is real but modest (ROC-AUC 0.5126) -- this technique is strong at STATE assignment and transition-matrix coherence, weaker at predicting WHICH escalations will default, and should be read accordingly.
- No demographic/protected-attribute data exists in this dataset (same limitation as Problem 1/2).
- Does not double-count reserve-timing dollars against Problem 3's ECL work -- the SMART suggestions in `reports/financial_impact_reporting_packaging/` frame that overlap as a coordination point, not a second dollar estimate.

## How this is tested going forward

`tests/` drives the REAL deployed FastAPI scoring service end-to-end via `TestClient` against the real, measured `roll_rate_deployment_policy.json` -- covering `/health`, `/model-info` (asserting the real, RECOMMENDED result), an exact-zero severity score at real feature means, a bit-exact match between the API and calling `compute_severity_score()`/`assign_state()` directly, real transition-matrix lookups, the unknown-previous-state 400 error path, and several deterministically-perturbed real customers.

## Deployment

`src/roll_rate_scoring_service.py` defaults `AMEX_RR_POLICY_PATH` to the real frozen policy JSON shipped alongside it in `src/` (self-contained -- no local machine path needed; a hardcoded local Windows path was found and fixed here during this hardening pass, the same class of bug already fixed once for Problem 5 -- see `CHANGELOG.md`). Run locally with `uvicorn roll_rate_scoring_service:app --port 8005` from `src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```
