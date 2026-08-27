# Changelog -- Problem 10: Credit Line Management

Dates below are real commit dates from this repository's git history, not estimated.

## 2026-08-27 -- PD_TREND redefinition (root-caused, NOT yet re-run with real data)

- **Root cause found for the real `trend_coherence` failure below:** the original `PD_TREND =
  DYNAMIC_PD - STATIC_PD` definition was a cross-model residual, not a genuine measure of change
  over time. Problem 1's `STATIC_PD` model has a real holdout AUC of 0.9620 -- HIGHER than Problem
  6's real `DYNAMIC_PD` holdout AUC of 0.9541 -- so within any `DYNAMIC_PD`-defined risk tier, a
  customer's `STATIC_PD` still carried real incremental signal about their true risk. Subtracting
  the stronger model's score from the weaker one mostly re-exposed the stronger model's signal,
  inverted, which is why the real observed gap between "Trending Worse" and "Trending Better" came
  out negative in all three risk tiers (as steep as -21 points, High Risk).
- **Redesigned** `PD_TREND` (Notebooks 54 Section 6/7, 55 Sections 5-6) as `DYNAMIC_PD` (current,
  real, most recent trailing window) minus `DYNAMIC_PD_EARLY` (the SAME Problem 6 model, real,
  applied to an immediately-preceding, non-overlapping trailing window of the same width) -- a
  genuine same-model, two-time-point trend, free of the cross-model confound. Costs real
  population: trend-eligibility now needs >= 2x Problem 6's winning window width in real
  statements, tighter than the plain dynamic-PD-only bar.
- Verified: `build_trailing_window_store()`'s new offset-window logic (the `k` parameter) checked
  against a synthetic multi-statement fixture in isolation, both notebooks re-validated for JSON
  structure and Python syntax (`scripts/check_notebook_syntax.py`, 0 errors across all 73
  notebooks). **NOT yet re-run against the real ~448K-customer dataset** -- this redefinition is
  a designed, syntax-and-logic-verified fix, not yet a validated result. Notebooks 56/57, the
  deployed service, tests, and this problem's real headline numbers below are all pending that
  real re-run.

## 2026-08-27 -- Global Standard hardening pass (delta, Problems 9-14)

- Published this problem's real Notebook 54-57 outputs (reports, real deployed service source) to
  the GitHub repository for the first time.
- **Real bug found and fixed:** `credit_line_scoring_service.py`'s `POLICY_PATH` default hardcoded
  the author's real local Windows path -- same bug class already found and fixed for Problems
  5-9's services; fixed to default to the real policy JSON now shipped alongside it in `src/`.
  `.env.example`'s example value had the same leak -- replaced with a generic placeholder.
- Added `tests/` (pytest): the real FastAPI recommendation service driven end-to-end via
  `TestClient` against the real, measured `credit_line_deployment_policy.json`, including the
  **honest NOT-recommended** result.
- Added `MODEL_CARD.md`, `CHANGELOG.md` (this file), `requirements.txt`.
- Added `src/docker/` (Dockerfile, docker-compose.yml, .dockerignore).
- Wired into the platform's root `ci.yml`, `code-quality.yml`, and `Makefile`.

## 2026-08-26 -- Notebook build (prior)

- Notebooks 54-57 built and run for real by this date. Real result: risk-level monotonicity
  passed, but trend coherence and minimum-tier-population both failed -- honestly reported as
  NOT RECOMMENDED FOR PRODUCTION, the one system excluded from the platform's value-creation total.
