# Changelog -- Problem 9: Collections Optimization

Dates below are real commit dates from this repository's git history, not estimated.

## 2026-08-27 -- Global Standard hardening pass (delta, Problems 9-14)

- Published this problem's real Notebook 50-53 outputs (reports, real trained model, real deployed
  service source) to the GitHub repository for the first time -- previously only on the author's
  own machine.
- **Real bug found and fixed:** `collections_scoring_service.py`'s `POLICY_PATH`/`MODEL_PATH`
  defaults hardcoded the author's real local Windows path (`C:\Users\rnand\...`) -- a privacy
  leak, since this file is published publicly. Same bug class already found and fixed for
  Problems 5-8's services; fixed here to default to the real policy JSON and trained model now
  shipped alongside it in `src/`. `.env.example` had the same leak in its example values --
  replaced with generic placeholders.
- Added `tests/` (pytest): the real FastAPI scoring service driven end-to-end via `TestClient`
  against the real trained model and real, measured `collections_deployment_policy.json`.
- Added `MODEL_CARD.md`, `CHANGELOG.md` (this file), `requirements.txt`.
- Added `src/docker/` (Dockerfile, docker-compose.yml, .dockerignore) -- container packaging for
  `collections_scoring_service.py`, mirroring Problem 8's self-contained Dockerfile pattern.
- Wired into the platform's root `ci.yml` (unit tests), `code-quality.yml` (lint/format/security),
  and `Makefile`.

## 2026-08-25 -- Notebook build (prior)

- Notebooks 50-53 built and run for real by this date. Real holdout ROC-AUC 0.8236 (reproduced,
  bit-identical), meets the KPI target (>= 0.60) -- RECOMMENDED FOR PRODUCTION.
