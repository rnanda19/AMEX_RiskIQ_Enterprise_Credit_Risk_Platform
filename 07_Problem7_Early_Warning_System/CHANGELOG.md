# Changelog -- Problem 7: Early Warning System

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-25 -- Authentication + explainability hardening (second pass)

- Added real API-key authentication (`X-API-Key` header) to
  `/model-info` and `/score` -- `/health` stays open.
- Added `top_reason_codes()`: this service already computes an exact
  per-feature z-score deviation as part of its own scoring, so the new
  `top_reasons` field simply ranks those already-real values by
  magnitude -- no new approximation technique needed.
- Replaced the real local Windows path shown as the example value in
  `.env.example` with a generic placeholder (information-leak cleanup,
  same as Problem 5 -- see that problem's CHANGELOG entry).
- Added 3 new tests (10 total for this problem) covering the auth gate
  and reason codes.

## 2026-08-25 -- Phase 3 hardening pass (this commit)

- Added `tests/` (pytest, 7 tests): the real FastAPI alert service
  (`/health`, `/model-info`, `/score`) driven end-to-end against the
  real, measured `early_warning_deployment_policy.json`, including a
  bit-exact match against calling `compute_early_warning()` directly,
  the alert-threshold boundary logic, the too-few-statements 422 error
  path, and the zero-variance-baseline division-guard.
- Added `MODEL_CARD.md`, `CHANGELOG.md` (this file), `requirements.txt`.
- Added `src/docker/` (Dockerfile, docker-compose.yml, .dockerignore) --
  container packaging for `real_time_alert_service.py`, mirroring
  Problem 4's self-contained Dockerfile pattern (the real frozen policy
  JSON ships alongside the service code, no separate `models/` folder
  needed).
- Copied the real `early_warning_deployment_policy.json` into `src/`
  (alongside `docs/`'s original copy) so the deployable service and its
  Docker image are fully self-contained -- the exact same fix pattern
  already applied once during the Phase 2 hardening pass for
  `ecl_calculator.py` and `severity_scorer.py`.
- **Real bug found and fixed:** `real_time_alert_service.py`'s
  `POLICY_PATH` default hardcoded the author's real local Windows path
  (`C:\Users\rnand\...`) -- a privacy leak, since this file is published
  publicly. This is the exact same bug class already found and fixed
  once for Problem 5's `early_default_service.py` during the Phase 2
  hardening pass; it had crept back in for this problem's own service
  and was live on GitHub before this commit. Fixed to default to the
  real policy JSON now shipped alongside it in `src/`.
- **Real bug found and fixed:** the service's own header comment (and
  this problem's originally-intended port) was `8004`, which collides
  with Problem 4's `severity_scoring_service.py` (also `8004`) --
  running both services' containers simultaneously would fail.
  Reassigned to `8007`, the next free port across the platform's now-8-
  service set.

## 2026-08-25 -- Phase 3 notebook-output publication (prior commit)

- Initial publication of this problem's real notebook outputs (reports,
  deployed service source) to the GitHub repository, alongside Problems
  6 and 8 (Phase 3 push). All 4 notebooks (42-45) were built and run for
  real by this date, honestly concluding NOT RECOMMENDED FOR PRODUCTION
  -- no candidate cleared the KPI target on this run.
