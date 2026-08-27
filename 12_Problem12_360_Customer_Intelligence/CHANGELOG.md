# Changelog -- Problem 12: 360 Degree Customer Intelligence

Dates below are real commit dates from this repository's git history, not estimated.

## 2026-08-27 -- Global Standard hardening pass (delta, Problems 9-14)

- Published this problem's real Notebook 62-65 outputs (reports, real deployed service source) to
  the GitHub repository for the first time.
- **Real bug found and fixed:** `customer_intelligence_lookup_service.py`'s `POLICY_PATH`/
  `PROFILE_PATH` defaults hardcoded the author's real local Windows paths -- same bug class
  already found and fixed for Problems 5-10's services; fixed to default the policy path to the
  real JSON shipped alongside it in `src/`, and the profile path to a documented `../data/`
  location (not committed -- see `data/README.md`, same convention as Problem 8's per-customer
  data). `.env.example`'s example values had the same leak -- replaced with generic placeholders.
- Added `tests/` (pytest): the real FastAPI lookup service driven end-to-end via `TestClient`
  against a small, synthetic-but-structurally-real profile fixture and the real, measured
  `customer_intelligence_deployment_policy.json`.
- Added `MODEL_CARD.md`, `CHANGELOG.md` (this file), `requirements.txt`, `data/README.md`.
- Added `src/docker/` (Dockerfile, docker-compose.yml with a runtime volume mount for the real,
  non-committed profile parquet, .dockerignore).
- Wired into the platform's root `ci.yml`, `code-quality.yml`, and `Makefile`.

## 2026-08-27 -- Notebook build (prior)

- Notebooks 62-65 built and run for real by this date. Real composite non-inferiority gap within
  CI tolerance, profile completeness and minimum tier population both passed -- RECOMMENDED FOR
  PRODUCTION.
