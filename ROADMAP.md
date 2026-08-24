# Roadmap

Two tracks, running independently: the **problem roadmap** (new modeling
problems, Phase 1 through Phase 5) and the **hardening track** (testing,
CI/CD, shared code, governance — added on top of already-built problems).
See `AMEX_Consolidated_Master_Plan.docx` (delivered 2026-08-24) for the full
narrative version of both.

## Hardening track — status

| Item | Status | Where |
|---|---|---|
| Root `shared/` library (metrics, config loader, PSI, tier/band assignment) | Done, 2026-08-24 | `shared/` |
| `shared/` unit tests | Done, 2026-08-24 (27 tests) | `shared/tests/` |
| Root CI workflow (notebook syntax check, unit tests, lint) | Done, 2026-08-24 (updated for Problems 3-5) | `.github/workflows/ci.yml` |
| Problem 1 tests (FastAPI service, monitoring job) | Done, 2026-08-24 (9 tests) | `Problem1_Credit_Scoring_PD_Prediction/tests/` |
| Problem 1 `CONTRIBUTING.md` / `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | repo root, `Problem1_.../` |
| Problem 2 tests (risk-tier FastAPI service) | Done, 2026-08-24 (5 tests) | `Problem2_Risk_Tier_Classification/tests/` |
| Problem 2 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | `Problem2_.../` |
| Problem 3 tests (`ecl_calculator.py`, driven by the real scoring bundle) | Done, 2026-08-24 (7 tests) | `Problem3_.../tests/` |
| Problem 3 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | `Problem3_.../` |
| Problem 4 tests (`severity_scorer.py`, driven by the real scoring bundle) | Done, 2026-08-24 (6 tests) | `Problem4_.../tests/` |
| Problem 4 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | `Problem4_.../` |
| Problem 5 tests (real FastAPI service, driven by the real trained model) | Done, 2026-08-24 (6 tests) | `Problem5_.../tests/` |
| Problem 5 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | `Problem5_.../` |
| **Push this commit to GitHub** | **Not started — needs a fresh PAT** | — |
| Wire existing notebooks to import from `shared/` instead of inline copies | **Deliberately deferred** — see below | — |
| Docker build test / FastAPI container smoke test | **Not started** | — |
| Pre-commit hooks (pyflakes, notebook syntax check, before every commit) | **Not started** | — |

Total: 60 tests passing across `shared/` and all five problems as of
2026-08-24 (`python -m pytest shared/tests Problem*/tests`).

### Why the notebooks aren't wired to `shared/` yet

`shared/metrics.py`, `shared/config.py`, and `shared/monitoring.py` are
extracted, byte-verified-identical copies of the logic already inside
`05_model_development.ipynb` and `12_monitoring.ipynb`. Rewiring those
notebooks to `from shared.metrics import amex_metric_numpy` instead of
defining it inline would mean re-running every downstream notebook and
re-verifying every number is unchanged — real work, and real risk to
already-verified, already-pushed output, for zero change in what gets
computed. This is next once every Phase 1/2 problem has its own
equivalent tests in place (now true) so a regression anywhere is caught
immediately, not discovered after the fact.

### Immediate next steps (in order)

1. ~~Problem 2 tests~~ — done, 2026-08-24.
2. ~~Push Problems 3, 4, 5 to GitHub with the same hardening pattern~~ —
   packaged and committed locally, 2026-08-24; **push itself still needs
   a fresh PAT** (the prior ones were revoked after Phase 1's push).
3. Docker build/smoke test for Problem 1's and Problem 2's `src/docker/Dockerfile`s
   (can't run `docker build` in every CI environment without a
   Docker-in-Docker step — evaluate `hadolint` as a lighter-weight static
   Dockerfile linter first). Problems 3-5 have no Dockerfile of their own
   yet (their deployable artifacts are a plain script / FastAPI app, not
   containerized).
4. Pre-commit hook: run `check_notebook_syntax.py` + `pyflakes` on
   `git commit`, so a broken notebook or an unused import is caught
   before it's even pushed, not just in CI after the fact.
5. Wire all five problems' notebooks to `shared/` (see above) — now that
   every problem has its own test safety net.
6. Kaggle notebook(s) and LinkedIn write-ups showcasing the platform
   (tracked outside this repo — see the project's own working notes).

## Problem roadmap — status (verified against real build history)

| Phase | Problems | Status |
|---|---|---|
| Phase 1 — Foundation | Problem 1 (PD Prediction), Problem 2 (Risk Tier Classification) | Complete, pushed to GitHub (25 notebooks) |
| Phase 2 — Regulatory & Loss Provisioning | Problem 3 (ECL/IFRS9/CECL), Problem 4 (Delinquency/Loss Severity), Problem 5 (Early Payment Default) | **Complete** (12 notebooks), packaged and committed locally, 2026-08-24 -- push pending a fresh PAT |
| Phase 3 — Behavioral Intelligence | Problems 6, 7, 8 | Not started |
| Phase 4 — Operational Risk Management | Problems 9, 10, 11 | Not started |
| Phase 5 — Customer & Business Intelligence | Problems 12, 13, 14 | Not started |

Next problem-roadmap item: Phase 3 (Problems 6-8, Behavioral Intelligence)
— not yet scoped in detail.
