# Changelog — Problem 1: Credit Scoring / PD Prediction

Dates below are real commit dates from this repository's git history, not
estimated.

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
