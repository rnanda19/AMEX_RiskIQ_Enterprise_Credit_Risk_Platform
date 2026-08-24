# Changelog -- Problem 5: Early Payment Default Detection

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-24 -- Phase 2 publication + hardening (this pass)

- Initial publication of this problem to the GitHub repository, alongside
  Problems 3 and 4 (Phase 2 push) -- all 4 notebooks (34-37) were built
  and run for real by this date, completing Problem 5 and Phase 2 as a
  whole. This commit packages that real output into the repository
  structure matching Phase 1's Problem 1/2 packages.
- Added `tests/` (pytest): the real FastAPI service (`/health`,
  `/model-info`, `/score`) driven end-to-end against the real, trained
  K=3 model and preprocessing artifacts included in `models/`.
- Added `MODEL_CARD.md`.
- (Context, not a change in this pass) During this problem's original
  build, Notebook 34's first design used a single percentile-derived
  `EARLY_WINDOW_K`, which collapsed to the dataset's real statement-count
  ceiling (13) on the real run -- defeating the point of an early-warning
  study. Fixed by replacing it with a fixed candidate set (K in
  {3,6,9,12}) tested as a curve against the full-history baseline, which
  is the design shipped here. Two further real-run path-resolution bugs
  (stale `pillar_dirs` entries in `project_config.json` for pillars that
  predate the Phase 1 folder reorg) were found and fixed in Notebook 35
  before the final real run.
