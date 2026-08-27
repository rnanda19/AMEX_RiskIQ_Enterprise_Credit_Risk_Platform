# Changelog -- Problem 8: Roll-Rate Modeling

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-25 -- Authentication + explainability hardening (second pass)

- Added real API-key authentication (`X-API-Key` header) to
  `/model-info` and `/score` -- `/health` stays open.
- Added `top_contributing_features()`: because the severity score is
  already a linear sum of per-feature terms, each term's own value IS
  its exact contribution -- this recomputes and ranks those terms, same
  technique as Problem 4's analogous weighted composite score.
- Replaced the real local Windows path shown as the example value in
  `.env.example` with a generic placeholder (information-leak cleanup,
  same as Problem 5 -- see that problem's CHANGELOG entry).
- Added 3 new tests (11 total for this problem) covering the auth gate
  and reason codes.

## 2026-08-25 -- Phase 3 hardening pass (this commit)

- Added `tests/` (pytest, 8 tests): the real FastAPI scoring service
  (`/health`, `/model-info`, `/score`) driven end-to-end against the
  real, measured `roll_rate_deployment_policy.json`, including an
  exact-zero severity score at real feature means, a bit-exact match
  against calling `compute_severity_score()`/`assign_state()` directly,
  real transition-matrix lookups, the unknown-previous-state 400 error
  path, and several deterministically-perturbed real customers.
- Added `MODEL_CARD.md`, `CHANGELOG.md` (this file), `requirements.txt`.
- Added `src/docker/` (Dockerfile, docker-compose.yml, .dockerignore) --
  container packaging for `roll_rate_scoring_service.py`, mirroring
  Problem 4's self-contained Dockerfile pattern (the real frozen policy
  JSON ships alongside the service code, no separate `models/` folder
  needed).
- Copied the real `roll_rate_deployment_policy.json` into `src/`
  (alongside `docs/`'s original copy) so the deployable service and its
  Docker image are fully self-contained -- the exact same fix pattern
  already applied once during the Phase 2 hardening pass for
  `ecl_calculator.py` and `severity_scorer.py`.
- **Real bug found and fixed:** `roll_rate_scoring_service.py`'s
  `POLICY_PATH` default hardcoded the author's real local Windows path
  (`C:\Users\rnand\...`) -- a privacy leak, since this file is published
  publicly. This is the exact same bug class already found and fixed
  once for Problem 5's `early_default_service.py` during the Phase 2
  hardening pass; it had crept back in for this problem's own service
  and was live on GitHub before this commit. Fixed to default to the
  real policy JSON now shipped alongside it in `src/`. (This problem's
  originally-intended port, `8005`, was already free -- no port
  reassignment needed, unlike Problems 6 and 7.)

## 2026-08-25 -- Phase 3 notebook-output publication (prior commit)

- Initial publication of this problem's real notebook outputs (reports,
  deployed service source) to the GitHub repository, alongside Problems
  6 and 7 (Phase 3 push). All 4 notebooks (46-49) were built and run for
  real by this date, RECOMMENDED FOR PRODUCTION -- both hard-gate KPIs
  (monotonicity and coherence) met on this run.
