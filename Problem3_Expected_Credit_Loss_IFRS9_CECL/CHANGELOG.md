# Changelog -- Problem 3: Expected Credit Loss (IFRS9/CECL)

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-24 -- Phase 2 publication + hardening (this pass)

- Initial publication of this problem to the GitHub repository, alongside
  Problems 4 and 5 (Phase 2 push) -- all 4 notebooks (30-33) were already
  built and run for real by this date; this commit packages that real
  output (reports, charts, the scoring bundle, the standalone
  `ecl_calculator.py`) into the repository structure matching Phase 1's
  Problem 1/2 packages.
- Added `tests/` (pytest): `ecl_calculator.py`'s staging and ECL-formula
  logic against the real, measured `ecl_scoring_bundle.json`.
- Added `MODEL_CARD.md`.
