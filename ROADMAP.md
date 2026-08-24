# Roadmap

Two tracks, running independently: the **problem roadmap** (new modeling
problems, Phase 1 through Phase 5) and the **hardening track** (testing,
CI/CD, shared code, governance — added on top of already-built problems).
See `AMEX_Consolidated_Master_Plan.docx` (delivered 2026-08-24) for the full
narrative version of both.

## Hardening track — status

| Item | Status | Where |
|---|---|---|
| Root `shared/` library (metrics, config loader, PSI) | Done, 2026-08-24 | `shared/` |
| `shared/` unit tests | Done, 2026-08-24 (15 tests) | `shared/tests/` |
| Root CI workflow (notebook syntax check, unit tests, lint) | Done, 2026-08-24 | `.github/workflows/ci.yml` |
| Problem 1 tests (FastAPI service, monitoring job) | Done, 2026-08-24 (9 tests) | `Problem1_Credit_Scoring_PD_Prediction/tests/` |
| Problem 1 `CONTRIBUTING.md` / `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | repo root, `Problem1_.../` |
| Problem 2 tests | **Not started** | — |
| Problem 3, 4 hardening (not yet in this repo — Phase 2, local only) | **Not started** | pushed to GitHub first, then hardened |
| Wire existing notebooks to import from `shared/` instead of inline copies | **Deliberately deferred** — see below | — |
| Docker build test / FastAPI container smoke test | **Not started** | — |
| Pre-commit hooks (pyflakes, notebook syntax check, before every commit) | **Not started** | — |

### Why the notebooks aren't wired to `shared/` yet

`shared/metrics.py`, `shared/config.py`, and `shared/monitoring.py` are
extracted, byte-verified-identical copies of the logic already inside
`05_model_development.ipynb` and `12_monitoring.ipynb`. Rewiring those
notebooks to `from shared.metrics import amex_metric_numpy` instead of
defining it inline would mean re-running every downstream notebook and
re-verifying every number is unchanged — real work, and real risk to
already-verified, already-pushed output, for zero change in what gets
computed. This is next once Problem 2 has its own equivalent tests in
place (so a regression anywhere is caught immediately, not discovered
after the fact).

### Immediate next steps (in order)

1. Problem 2 tests — same pattern as Problem 1 (fixture-based service
   tests where `Problem2_Risk_Tier_Classification/src/` has standalone
   Python services; CLI tests for any monitoring/batch script).
2. Push Problem 3 and Problem 4 (currently local-only, Phase 2, not yet in
   this GitHub repo) as their own subfolders, then apply the same
   `tests/` + `CONTRIBUTING.md` pattern to them.
3. Docker build/smoke test for Problem 1's `src/docker/Dockerfile` (can't
   run `docker build` in every CI environment without a Docker-in-Docker
   step — evaluate `hadolint` as a lighter-weight static Dockerfile
   linter first).
4. Pre-commit hook: run `check_notebook_syntax.py` + `pyflakes` on
   `git commit`, so a broken notebook or an unused import is caught
   before it's even pushed, not just in CI after the fact.
5. Wire Problem 1's notebooks to `shared/` (see above) — only after step 1
   gives Problem 2 the same safety net.

## Problem roadmap — status (verified against real build history)

| Phase | Problems | Status |
|---|---|---|
| Phase 1 — Foundation | Problem 1 (PD Prediction), Problem 2 (Risk Tier Classification) | Complete, pushed to GitHub (25 notebooks) |
| Phase 2 — Regulatory & Loss Provisioning | Problem 3 (ECL/IFRS9/CECL) ✅, Problem 4 (Delinquency/Loss Severity) ✅, Problem 5 (Early Payment Default) — not built | 2 of 3 complete (8 notebooks) |
| Phase 3 — Behavioral Intelligence | Problems 6, 7, 8 | Not started |
| Phase 4 — Operational Risk Management | Problems 9, 10, 11 | Not started |
| Phase 5 — Customer & Business Intelligence | Problems 12, 13, 14 | Not started |

Next problem-roadmap item: Problem 5 (Early Payment Default Detection),
same 4-notebook Phase 2 pattern as Problems 3 and 4, depends only on
Problem 1's champion model.
