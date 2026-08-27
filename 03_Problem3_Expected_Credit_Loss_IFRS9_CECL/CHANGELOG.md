# Changelog -- Problem 3: Expected Credit Loss (IFRS9/CECL)

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-25 -- Authentication + explainability hardening

- Added real API-key authentication (`X-API-Key` header) to
  `/model-info` and `/score` -- `/health` stays open.
- Added `explain_ecl()` to `ecl_calculator.py` and wired it into
  `/score`'s new `top_reasons` field: a real, exact narration of which
  branch of the IFRS9 staging rule fired and which frozen LGD value
  drove the ECL amount -- more exact than any sampled attribution
  method, since this technique is a fully interpretable rule engine
  with nothing left to approximate.
- Added `.env.example` and 7 new tests (20 total for this problem)
  covering both the auth gate and `explain_ecl()`.

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
