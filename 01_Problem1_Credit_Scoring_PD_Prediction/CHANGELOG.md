# Changelog — Problem 1: Credit Scoring / PD Prediction

Dates below are real commit dates from this repository's git history, not
estimated.

## 2026-08-25 — Authentication + explainability hardening

- Added real API-key authentication (`X-API-Key` header, checked with
  `secrets.compare_digest`) to `/model-info` and `/predict` — `/health`
  stays open, matching standard load-balancer/k8s-probe practice. Falls
  back to a published, clearly-labeled dev-only key if `API_KEY` is
  unset, with a loud log warning; a real deployment must set it.
- Added real, per-request reason codes to `/predict`: an exact,
  live-computed marginal-contribution explanation (re-scores the same
  customer with one feature at a time reset to its training-set
  baseline and reports the resulting change in predicted PD) — not
  cached, not sampled. Answers the CFPB Circular 2022-03 "specific,
  principal reason" requirement this service previously had no answer
  for.
- **Real bug found and fixed**: `main.py`'s `AMEX_PROJECT_ROOT` default
  still hardcoded the author's real local Windows path — the same
  privacy-leak bug class already found and fixed for Problem 5 (Phase 2)
  and Problems 6/7/8 (Phase 3), but never previously caught here. Fixed
  by requiring the env var explicitly (a clear `RuntimeError` if unset)
  rather than defaulting to any local path — there is no safe
  repo-relative default here since the real champion model isn't
  committed to this public repo (see `models/README.md`).
- Added `.env.example` (previously missing for this problem) and 6 new
  regression tests (14 total for this problem) covering both fixes.

## 2026-08-24 — Enterprise hardening (this pass)

- Added `tests/` (pytest): FastAPI service (health/model-info/predict,
  including missing-feature imputation and unseen-category handling) and
  the monitoring job CLI (exit-code contract, PSI reporting, log
  append-without-duplicate-header) — 9 tests, all passing against real
  code paths via synthetic-but-structurally-real fixtures.
- Added `MODEL_CARD.md`.
- Contributed the extraction basis for root-level `shared/metrics.py`
  (`amex_metric_numpy`, `top_four_percent_capture_only`) and
  `shared/monitoring.py` (`psi_bin_share`) — byte-verified-identical to
  this problem's own `05_model_development.ipynb` / monitoring job logic.
  This problem's own notebooks are not yet wired to import from `shared/`
  (see root `ROADMAP.md`).

## 2026-08-24 — GitHub Pages enabled

- Enabled GitHub Pages on the repo; added "Live Dashboards" links in the
  root and this folder's README pointing at
  `reports/executive_reports/Financial_Impact_Dashboard.html` and
  `reports/powerbi_dashboard/PowerBI_Dashboard_Preview.html`.

## 2026-08-24 — License change

- Replaced the MIT license with an "All Rights Reserved" notice at repo
  root and in this folder — repo stays public for viewing, but is no
  longer licensed for reuse/redistribution.

## 2026-08-24 — Initial publication

- Initial commit: 18 notebooks (Business Understanding through Repository
  Packaging), FastAPI service, Docker deployment, monitoring job, Power BI
  data model, and the full executive/technical/compliance report set,
  pushed to GitHub as part of the combined AMEX RiskIQ Phase 1 release
  (Problem 1 + Problem 2).
