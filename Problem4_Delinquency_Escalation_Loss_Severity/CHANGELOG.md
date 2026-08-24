# Changelog -- Problem 4: Delinquency Escalation / Loss Severity

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-24 -- Phase 2 publication + hardening (this pass)

- Initial publication of this problem to the GitHub repository, alongside
  Problems 3 and 5 (Phase 2 push) -- all 4 notebooks (26-29) were already
  built and run for real by this date; this commit packages that real
  output into the repository structure matching Phase 1's Problem 1/2
  packages.
- Added `tests/` (pytest): `severity_scorer.py`'s tier-assignment and
  missing-value-handling logic against the real, measured
  `severity_scoring_bundle.json`.
- Added `MODEL_CARD.md`.
- (Context, not a change in this pass) During this problem's original
  build, 4 real bugs were found and fixed via its own self-test before
  final delivery: a NaN-vs-None missing-value gap, a summation-order
  mismatch between the saved weight-sorted CSV and the real alphabetical
  computation order, and -- the actual root cause once the first two were
  fixed -- `severity_feature_weights.csv`'s `normalized_weight` column
  being saved rounded to 5 decimal places for display but consumed
  directly as the real scoring weight downstream. Fixed architecturally:
  Notebook 27 now saves weight/mean/std at full float precision and
  Notebook 28 reads them directly rather than recomputing anything from a
  fresh reload.
