# Model Card -- Expected Credit Loss (IFRS9/CECL)

## Model details

- **Not a trained ML model** -- this problem's "model" is a deterministic ECL calculation engine (`src/ecl_calculator.py`) that combines Problem 1's real trained PD model output and Problem 4's real trained severity-tier model output through a frozen, rule-based staging rubric and standards-compliant formula. No parameters here are fit from data beyond what Problems 1 and 4 already produced.
- **Upstream champion PD model (measured, Problem 1):** XGBoost, holdout AUC 0.9620396555226549.
- **Upstream severity/LGD model (measured, Problem 4):** 3-tier Escalation Severity Score, LGD by tier 0.3015 / 0.45 / 0.648.
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `30_ecl_policy.ipynb` -> `33_financial_impact_reporting_packaging.ipynb`.

## Intended use

Compute regulator-facing Expected Credit Loss (IFRS9-staged and CECL lifetime) for a credit card portfolio, split out per customer, so a risk/finance team can compare provisioning under both standards against a flat-LGD baseline and size a macro-stress capital buffer.

## Staging methodology (outcome-free by design)

Stage 2 (SICR) and Stage 3 (credit-impaired) are computed ONLY from real PD (Problem 1) and real severity tier (Problem 4) -- never from the known default outcome. This closes a shortcut flagged by Problem 1's own Notebook 08 in its own limitations section. Stage 3 requires severity tier "Severe" AND PD above `stage3_pd_threshold`; Stage 2 requires PD above `portfolio_avg_pd_12m * sicr_pd_multiple` OR an elevated severity tier; everything else is Stage 1.

## Evaluation (real, measured)

- IFRS9 stage distribution on the real 91,783-customer holdout: Stage 1 30,281 / Stage 2 40,277 / Stage 3 21,225.
- Stage monotonicity vs. real observed default rate: validated (post-hoc check only, not used to derive the rubric).
- Chi-square (stage vs. actual default): p = 0.0. Cramer's V: 0.7289977841059684. Z-test: p = 0.0.
- Split-half score PSI: 1.278534602748648e-05 (stable, well under the 0.10 target).
- Standalone `ecl_calculator.py` self-test against the full real holdout: 91,783/91,783 customers checked, 0 hard mismatches, 0 boundary ties (see `Problem4/MODEL_CARD.md`'s bugfix history in project memory for why this all-customer, magnitude-classified self-test design exists).

## Limitations

- Lifetime-PD multiplier, discount rates, and macro-scenario weights are explicit ASSUMPTIONs (no ground truth exists in this dataset for multi-year forward PD or macro overlays) -- see `docs/ecl_policy.json` for the exact, editable values and source notes.
- EAD is a flat $5,000-per-account illustrative ASSUMPTION inherited from Problem 1's Notebook 08, not re-derived here.
- This model assumes Problem 1's and Problem 4's real deployed models are the PD/severity inputs -- it does not re-validate their individual accuracy (see each problem's own MODEL_CARD for that).

## How this is tested going forward

`tests/` covers `ecl_calculator.py`'s `compute_ecl()` against the real, measured `ecl_scoring_bundle.json` -- stage assignment logic, LGD-by-tier lookup, and the IFRS9-vs-CECL discount-factor distinction. `tests/test_ecl_scoring_service.py` additionally covers the deployable API below end-to-end, checking every response is bit-identical to calling `compute_ecl()` directly.

## Deployment

`src/ecl_scoring_service.py` wraps `compute_ecl()` as a FastAPI service (`GET /health`, `GET /model-info`, `POST /score`). The real `ecl_scoring_bundle.json` ships alongside it in `src/`, so the service is fully self-contained -- no external volume mount needed (unlike Problem 1's much larger champion model, which is intentionally mounted at runtime rather than baked into its image). Run locally with `uvicorn ecl_scoring_service:app --port 8003` from `src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```

See `src/docker/Dockerfile` for the exact build; its context is `src/` (one level up from `docker/`).
