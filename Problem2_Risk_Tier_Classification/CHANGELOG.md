# Changelog — Problem 2: Risk Tier Classification

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-25 — Authentication + explainability hardening

- Added real API-key authentication (`X-API-Key` header) to
  `/policy-info` and `/risk-tier` — `/health` stays open. Same design
  as Problem 1's service (see that CHANGELOG entry for the fallback-key
  and warning-log behavior).
- Added real, per-request reason codes to `/risk-tier`: the same exact
  marginal-contribution technique as Problem 1's PD service, applied to
  the same champion model, so a customer's tier placement carries the
  same real explanation its underlying PD does.
- **Real bug found and fixed**: `risk_tier_service.py`'s
  `AMEX_PROJECT_ROOT` default still hardcoded the author's real local
  Windows path — same bug, same fix as Problem 1 (see that entry).
- Added `.env.example` (previously missing) and 3 new regression tests
  (8 total for this problem) covering both fixes.

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
