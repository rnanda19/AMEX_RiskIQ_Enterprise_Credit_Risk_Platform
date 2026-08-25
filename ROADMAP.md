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
| Root CI workflow (notebook syntax check, unit tests) | Done, 2026-08-25 (split from lint — see below) | `.github/workflows/ci.yml` |
| Code-quality workflow (lint, format check, security scan) | Done, 2026-08-25 (new — pyflakes + `black --check`, both advisory; `bandit`, blocking, 0 findings) | `.github/workflows/code-quality.yml` |
| Problem 1 tests (FastAPI service, monitoring job) | Done, 2026-08-24 (9 tests) | `Problem1_Credit_Scoring_PD_Prediction/tests/` |
| Problem 1 `CONTRIBUTING.md` / `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | repo root, `Problem1_.../` |
| Problem 2 tests (risk-tier FastAPI service) | Done, 2026-08-24 (5 tests) | `Problem2_Risk_Tier_Classification/tests/` |
| Problem 2 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24 | `Problem2_.../` |
| Problem 3 tests (`ecl_calculator.py` + new deployable API, driven by the real scoring bundle) | Done, 2026-08-25 (14 tests, up from 7) | `Problem3_.../tests/` |
| Problem 3 deployable API (`ecl_scoring_service.py`) + Docker | Done, 2026-08-25 (new) | `Problem3_.../src/` |
| Problem 3 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24, updated 2026-08-25 | `Problem3_.../` |
| Problem 4 tests (`severity_scorer.py` + new deployable API, driven by the real scoring bundle) | Done, 2026-08-25 (12 tests, up from 6) | `Problem4_.../tests/` |
| Problem 4 deployable API (`severity_scoring_service.py`) + Docker | Done, 2026-08-25 (new) | `Problem4_.../src/` |
| Problem 4 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24, updated 2026-08-25 | `Problem4_.../` |
| Problem 5 tests (real FastAPI service, driven by the real trained model) | Done, 2026-08-24 (6 tests) | `Problem5_.../tests/` |
| Problem 5 Docker (service already existed; container packaging new) | Done, 2026-08-25 (new) | `Problem5_.../src/docker/` |
| Problem 5 `MODEL_CARD.md` / `CHANGELOG.md` | Done, 2026-08-24, updated 2026-08-25 | `Problem5_.../` |
| Root governance files (issue templates, PR template, `setup.py`, `pyproject.toml`, `Makefile`) | Done, 2026-08-25 | repo root, `.github/` |
| `BENCHMARKS.md` (real baseline-vs-model comparisons, all 5 problems) | Done, 2026-08-25 | repo root |
| **Push this commit to GitHub** | **Not started — needs a fresh PAT** | — |
| Wire existing notebooks to import from `shared/` instead of inline copies | **Deliberately deferred** — see below | — |
| Real `docker build`/smoke test of any Dockerfile (this sandbox has no Docker Hub registry access; static build-context verification passed for all 3 new Dockerfiles — see below) | **Blocked on environment, not on the work** | — |
| Repo-wide `black` reformatting | **Deliberately deferred** — advisory-only for now, see below | — |
| Pre-commit hooks (pyflakes, notebook syntax check, before every commit) | **Not started** | — |

Total: 73 tests passing across `shared/` and all five problems as of
2026-08-25 (`python -m pytest shared/tests Problem*/tests`, or `make test-all`).

### A real bug found (and fixed) while building this pass

Two, actually. (1) `ecl_calculator.py` and `severity_scorer.py` both defaulted their bundle path
to a file alongside themselves in `src/` that was never actually copied there (only shipped in
`reports/validation_deployment/`) — running either script standalone raised `FileNotFoundError`.
Fixed by copying the real bundle JSON into `src/` for both, verified by actually running each
script standalone before and after. (2) `early_default_service.py`'s `MODELS_DIR` default
hardcoded the author's real local Windows path (`C:\Users\rnand\...`) — a privacy leak, since
this file is published publicly. Fixed to default to the repo's own `models/` folder instead
(self-contained, matches how the real trained artifacts already ship in this repo).

A third finding, NOT fixed here (out of this pass's scope, flagged for awareness): Problem 1's
own `src/docker/Dockerfile` expects `main.py` and `requirements-api.txt` in its own build
context, but those files actually live in the sibling `src/fastapi_service/` folder — the
Dockerfile as packaged cannot build with `docker build .` or `docker-compose up` from
`src/docker/` as written. The 3 new Dockerfiles built in this pass (Problems 3/4/5) were
designed and statically verified against this exact failure mode (every `COPY` source path
checked to actually resolve against its stated build context) specifically because this bug was
found first.

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
2. ~~Package Problems 3, 4, 5 with the same hardening pattern as Phase 1,
   plus deployable APIs, Docker, and root governance files for all~~ —
   done, 2026-08-25. **Push to GitHub itself still needs a fresh PAT**
   (the prior ones were revoked after Phase 1's push).
3. Real `docker build`/compose smoke test for all 4 Dockerfiles (Problems
   1, 3, 4, 5) once run somewhere with real Docker Hub registry access —
   this pass could only statically verify build-context correctness, not
   actually pull a base image and build.
4. Fix Problem 1's `src/docker/Dockerfile` build-context bug (see above) —
   flagged, not fixed, in this pass.
5. Pre-commit hook: run `check_notebook_syntax.py` + `pyflakes` on
   `git commit`, so a broken notebook or an unused import is caught
   before it's even pushed, not just in CI after the fact.
6. Repo-wide `black` reformatting pass, once deliberately scheduled (not
   as a side effect of another change) — then flip `format-check` from
   advisory to blocking.
7. Wire all five problems' notebooks to `shared/` (see above) — now that
   every problem has its own test safety net.
8. Kaggle notebook(s) and LinkedIn write-ups showcasing the platform
   (tracked outside this repo — see the project's own working notes).

### On the "Global Standard" repository score

An earlier planning doc (`AMEX_Global_Standard_Structure_1.docx`) proposed a 10-category,
100-point scoring rubric for this repository (baseline 62/100, target 85-90/100) with attached
salary-band claims per score. That rubric is this project's own invented heuristic, not an
external or industry-verified benchmark — the salary figures in particular are not to be taken
at face value. What IS real: this pass added genuine substance the rubric's own categories
name — deployable APIs + Docker for Problems 3-5 (Production Readiness / DevOps), a security
scan with 0 real findings plus a doubled test count (Automated Testing & CI/CD), and a
consolidated real-comparisons file (Benchmarking & Comparison) — tracked here as real engineering
work, not as progress toward an unverified number.

## Problem roadmap — status (verified against real build history)

| Phase | Problems | Status |
|---|---|---|
| Phase 1 — Foundation | Problem 1 (PD Prediction), Problem 2 (Risk Tier Classification) | Complete, pushed to GitHub (25 notebooks) |
| Phase 2 — Regulatory & Loss Provisioning | Problem 3 (ECL/IFRS9/CECL), Problem 4 (Delinquency/Loss Severity), Problem 5 (Early Payment Default) | **Complete, pushed to GitHub 2026-08-25** (12 notebooks + Global Standard hardening pass) |
| Phase 3 — Behavioral Intelligence | Problems 6, 7, 8 | **In progress, 2026-08-25** — Problem 6 complete (Notebooks 38-41); Problem 7 complete (Notebooks 42-45), concluded NOT RECOMMENDED FOR PRODUCTION (honest result -- real default-rate lift below KPI target; a v2 enhancement attempt, Notebooks 46-47, was built, showed genuine but insufficient improvement, and was deliberately abandoned per user decision, freeing 46-49 for Problem 8); Problem 8 not yet built |
| Phase 4 — Operational Risk Management | Problems 9, 10, 11 | Not started |
| Phase 5 — Customer & Business Intelligence | Problems 12, 13, 14 | Not started |

## Phase 3 build plan — scoped 2026-08-25

Per `AMEX_Master_Execution_Plan_1.docx` Section 8, Phase 3 moves past a static
point-in-time PD snapshot to a continuously updated behavioral view:

| # | Problem | Depends on | Core technique (per master plan) | Deliverable |
|---|---|---|---|---|
| 6 | Dynamic / Behavioral Credit Scoring | #1, #4 | Windowed GBM on each customer's real multi-statement panel (reuses Problem 1's champion architecture, same scope-decision pattern as Problem 5 — LSTM explicitly noted as a future extension, not built here) | Monthly-refreshed dynamic PD |
| 7 | Early Warning System | #6 | Rolling z-score trend-deviation detection on Problem 6's real panel scores | Real-time alert service |
| 8 | Roll-Rate Modeling | #4, #6 | Markov transition matrix across Problem 4's real severity/delinquency buckets | Bucket-transition probability model |

Same 4-notebook-per-problem pattern as Phase 2 (Business Understanding &
Policy → Modeling → Validation & Deployment → Financial-Impact Reporting &
Packaging), continuing the numbering sequence: Notebooks 38-41 (Problem 6),
42-45 (Problem 7), 46-49 (Problem 8) — 12 notebooks total. Same standing
rules apply unchanged: zero-fabrication, Claude generates code only (user
runs every notebook locally), WARP optimization standard, `random_state=42`,
one notebook = one idempotent code cell, no local/absolute paths in any
publicly-shared file.

Repository-packaging skeleton for all 3 problems (`notebooks/`, `src/`,
`tests/`, `reports/`, `docs/`, `artifacts/`, `models/`, `data/`,
`.gitignore`, `LICENSE`) created and committed locally 2026-08-25 — content
is empty by design (no notebooks built yet); **not pushed to GitHub** until
each problem has real content, same practice as every prior phase. The
Global Standard hardening pass (deployable APIs, Docker, CI, root
governance files, BENCHMARKS.md entries) is deliberately deferred until
after all 3 problems' base notebooks are built and verified, matching how
Phase 2 was hardened only after Notebook 37 shipped.

Next problem-roadmap item: Notebook 46 (Problem 8, Business Understanding
& Policy).
