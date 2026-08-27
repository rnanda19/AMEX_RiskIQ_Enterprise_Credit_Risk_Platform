# Changelog -- Problem 11: Real-Time Portfolio Monitoring

## 2026-08-27 -- Global Standard hardening pass (delta, Problems 9-14)

- **Real bug found and fixed:** `portfolio_alert_feed_service.py`'s `POLICY_PATH` default
  hardcoded the author's real local Windows path -- same bug class already found and fixed for
  Problems 5-8's services; fixed to default to the real policy JSON shipped alongside it in
  `src/`. `.env.example`'s example value had the same leak -- replaced with a generic placeholder.
- Added `tests/` (pytest): the real FastAPI ops-dashboard/alert-feed service driven end-to-end via
  `TestClient` against the real, measured `portfolio_monitoring_deployment_policy.json` --
  covering `/health`, `/policy-info`, the auth gate, month ingestion below/at/above the real
  baseline-eligibility threshold, and the `/reset` test-only endpoint.
- Added `src/docker/` (Dockerfile, docker-compose.yml, .dockerignore) -- this problem previously
  had `MODEL_CARD.md`/`CHANGELOG.md`/`requirements.txt` from an earlier hardening pass but no
  container packaging and no tests.
- Wired into the platform's root `ci.yml`, `code-quality.yml`, and `Makefile`.

## 2026-08-27 -- Customer joint-deviation redesign (real rework, user-directed)

- **Root cause diagnosed:** two real full-data runs of the customer-level cohort score collapsed to an exact 100%/0% split (ROC-AUC 0.5, MCC 0) because presence-based customer flagging carries zero information when over 75% of real customers share an identical full 13/13-month coverage window -- every tested customer had virtually the same exposure regardless of technique changes.
- **Fix:** replaced presence-based flagging with a genuinely new "joint deviation" design across Notebooks 58-60 -- a customer only counts toward a flagged cohort if (a) their statement falls in a month the portfolio's own trailing-baseline control chart flags as an ALERT month, AND (b) their own real statement value in that same breaching column is itself >=2.0 standard deviations (`CUSTOMER_DEVIATION_Z_THRESHOLD`, new policy field) from that month's real cross-sectional peer mean/std, in the same direction as the portfolio's own shift.
- Notebook 58: added `CUSTOMER_DEVIATION_Z_THRESHOLD = 2.0` (documented ASSUMPTION, rationale references the two prior failed fixes) to the policy JSON.
- Notebook 59: added a real per-(customer, month) statement-value store (`build_customer_statement_value_store`), a cross-sectional std alongside the existing cross-sectional mean, and the joint-deviation mask/count computation; retitled the continuous score "Customer Joint-Deviation Score".
- Notebook 60: mirrored every Notebook 59 change for independent reproduction; confirmed the deployed FastAPI service needs no changes (it only ingests/alerts at the portfolio-month level, never scores individual customers).
- Notebook 61: confirmed unchanged -- it reads `winning_consecutive_breach_candidate` from Notebook 60's summary generically.
- **Result (real, third full-data run):** cohort default-rate lift 2.67x, MCC 0.401, all statistical checks pass, recommended for production -- verified via `deployment_readiness_checklist.csv` and the live API self-test, not asserted.

## 2026-08-27 -- Repository structure unification

- Reorganized this problem's folders to match the platform-wide convention used by Problems 1, 3-8: `policy/` -> `docs/`, `deployment/` -> `reports/validation_deployment/`, top-level `financial_impact_reporting_packaging/` -> `reports/financial_impact_reporting_packaging/`, `src/api/*` flattened into `src/`.
- Added the previously-missing `README.md`, `MODEL_CARD.md`, `CHANGELOG.md` (this file), `LICENSE`, `requirements.txt` -- all content sourced directly from this problem's real, measured Notebook 58-61 output files, no invented figures.
