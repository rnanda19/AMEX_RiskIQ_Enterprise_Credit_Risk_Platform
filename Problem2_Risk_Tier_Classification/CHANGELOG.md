# Changelog — Problem 2: Risk Tier Classification

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-24 — Enterprise hardening (this pass)

- Added `tests/` (pytest): risk-tier FastAPI service (health, policy-info,
  tier assignment consistency against the real business-rule bands,
  missing-feature imputation, unseen-category handling) — 5 tests, all
  passing against real code paths via synthetic-but-structurally-real
  fixtures.
- Added `MODEL_CARD.md`.
- Contributed the generalization basis for root-level `shared/tiers.py`
  (`assign_band`, generalized from this problem's own `assign_tier()`) —
  logic preserved exactly (same half-open-interval, same out-of-range
  fallback), tested against this problem's real
  `docs/risk_tier_policy.json` band values. This problem's own
  `risk_tier_service.py` is not yet wired to import from `shared/` (see
  root `ROADMAP.md`).

## 2026-08-24 — GitHub Pages / License / Initial publication

Same repo-wide changes as
`Problem1_Credit_Scoring_PD_Prediction/CHANGELOG.md` (GitHub Pages enabled,
MIT → All Rights Reserved, initial commit) — this problem was part of the
same combined Phase 1 release, not published separately.
