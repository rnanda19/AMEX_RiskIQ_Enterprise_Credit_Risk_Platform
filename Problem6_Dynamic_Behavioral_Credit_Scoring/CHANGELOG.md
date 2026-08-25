# Changelog -- Problem 6: Dynamic / Behavioral Credit Scoring

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-25 -- Phase 3 hardening pass (this commit)

- Added `tests/` (pytest, 6 tests): the real FastAPI service (`/health`,
  `/model-info`, `/score`) driven end-to-end against the real, trained
  W=3 model and preprocessing artifacts included in `models/`, including
  a bit-exact match against direct model inference.
- Added `MODEL_CARD.md`, `CHANGELOG.md` (this file), `requirements.txt`.
- Added `src/docker/` (Dockerfile, docker-compose.yml, .dockerignore) --
  container packaging for `dynamic_behavioral_service.py`, mirroring
  Problem 5's Dockerfile pattern (build context is the problem root,
  since the image needs both `src/` and the real `models/` artifacts).
- **Real bug found and fixed:** `dynamic_behavioral_service.py`'s
  `MODELS_DIR` default hardcoded the author's real local Windows path
  (`C:\Users\rnand\...`) -- a privacy leak, since this file is published
  publicly. This is the exact same bug class already found and fixed
  once for Problem 5's `early_default_service.py` during the Phase 2
  hardening pass; it had crept back in for this problem's own service
  and was live on GitHub before this commit. Fixed to default to this
  repo's own `models/` folder instead (self-contained).
- **Real bug found and fixed:** the service's own header comment (and
  this problem's originally-intended port) was `8003`, which collides
  with Problem 3's `ecl_scoring_service.py` (also `8003`) -- running
  both services' containers simultaneously would fail. Reassigned to
  `8006`, the next free port across the platform's now-8-service set
  (8000-8005 already assigned to Problems 1-5 and 8).

## 2026-08-25 -- Phase 3 notebook-output publication (prior commit)

- Initial publication of this problem's real notebook outputs (reports,
  trained model, preprocessing artifacts, deployed service source) to
  the GitHub repository, alongside Problems 7 and 8 (Phase 3 push). All
  4 notebooks (38-41) were built and run for real by this date.
