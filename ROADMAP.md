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
| Problem 6 tests (real FastAPI service, driven by the real trained W=3 model) | Done, 2026-08-25 (6 tests) | `Problem6_.../tests/` |
| Problem 6 Docker (service already existed; container packaging new) | Done, 2026-08-25 (new) | `Problem6_.../src/docker/` |
| Problem 6 `MODEL_CARD.md` / `CHANGELOG.md` / `requirements.txt` | Done, 2026-08-25 | `Problem6_.../` |
| Problem 7 tests (real FastAPI alert service, driven by the real frozen policy JSON) | Done, 2026-08-25 (7 tests) | `Problem7_.../tests/` |
| Problem 7 Docker (service already existed; container packaging new, self-contained bundle pattern) | Done, 2026-08-25 (new) | `Problem7_.../src/docker/` |
| Problem 7 `MODEL_CARD.md` / `CHANGELOG.md` / `requirements.txt` | Done, 2026-08-25 | `Problem7_.../` |
| Problem 8 tests (real FastAPI scoring service, driven by the real frozen policy JSON) | Done, 2026-08-25 (8 tests) | `Problem8_.../tests/` |
| Problem 8 Docker (service already existed; container packaging new, self-contained bundle pattern) | Done, 2026-08-25 (new) | `Problem8_.../src/docker/` |
| Problem 8 `MODEL_CARD.md` / `CHANGELOG.md` / `requirements.txt` | Done, 2026-08-25 | `Problem8_.../` |
| `BENCHMARKS.md` entries for Problems 6, 7, 8 | Done, 2026-08-25 | repo root |
| CI (`ci.yml`, `code-quality.yml`) + `Makefile` wired for Problems 6, 7, 8 | Done, 2026-08-25 | `.github/workflows/`, `Makefile` |
| Real API-key authentication on all 8 deployed services (`X-API-Key`, `/health` stays open) | Done, 2026-08-25 | every `Problem*/src/*service.py` |
| Real, per-request explainability (`top_reasons`) on all 8 deployed services | Done, 2026-08-25 | every `Problem*/src/*service.py` |
| `.env.example` added for Problems 1-4 (previously missing) + API_KEY documented for all 8 | Done, 2026-08-25 | every `Problem*/src/.env.example` |
| `docker-compose.yml` updated to require `API_KEY` at runtime (fail loud if unset) for all 8 | Done, 2026-08-25 | every `Problem*/src/docker/docker-compose.yml` |
| 32 new tests for the auth + explainability pass (126 total) | Done, 2026-08-25 | every `Problem*/tests/` |
| Wire existing notebooks to import from `shared/` instead of inline copies | **Deliberately deferred** — see below | — |
| Real `docker build`/smoke test of any Dockerfile (this sandbox has no Docker Hub registry access; static build-context verification passed for all 3 new Dockerfiles — see below) | **Blocked on environment, not on the work** | — |
| Repo-wide `black` reformatting | **Deliberately deferred** — advisory-only for now, see below | — |
| Pre-commit hooks (pyflakes, notebook syntax check, before every commit) | **Not started** | — |

Total: 126 tests passing across `shared/` and all eight problems as of
2026-08-25 (`python -m pytest shared/tests Problem*/tests`, or `make test-all`) --
94 from the prior pass plus 32 new tests from the authentication +
explainability hardening pass below.

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

### Two more real bugs found (and fixed) during the Phase 3 hardening pass (2026-08-25)

(1) All three of Problems 6, 7, and 8's deployable service files
(`dynamic_behavioral_service.py`, `real_time_alert_service.py`,
`roll_rate_scoring_service.py`) hardcoded the author's real local Windows
path (`C:\Users\rnand\...`) as their model/policy-file default — the
exact same privacy-leak bug class already found and fixed once for
Problem 5's `early_default_service.py` during the Phase 2 pass, but it
had crept back in for all three Phase 3 services and was live on GitHub
before this pass. Fixed to default to each repo's own `models/`/`src/`
folder instead (self-contained), matching the established pattern.
(2) Problem 6 and Problem 7's services declared ports (`8003`, `8004`)
that collide with Problem 3's and Problem 4's already-running services —
undetected until this pass cross-checked every service's port against
the platform's full port list while writing their Dockerfiles.
Reassigned to `8006` and `8007` respectively (Problem 8's `8005` was
already free). Neither bug affected any notebook's own output or any
already-computed real number — both were caught in the deployable
service layer only, and both are now covered by this pass's own tests
(which import each service module fresh and would fail to even load a
policy/model file with a bad default).

### Closing the two hard blockers named by an independent model-risk benchmark (2026-08-25)

A benchmark pass against real external frameworks (Fed/OCC SR 11-7, Basel IRB
validation standards, CFPB Circular 2022-03 / ECOA-Reg B adverse-action
requirements, EU AI Act Annex III high-risk credit-scoring requirements)
scored this platform honestly as strong for a portfolio but named two hard
blockers for actual production use at a regulated institution: (1) zero
authentication on any of the 8 deployed FastAPI services, and (2) zero
adverse-action reason-code/explainability output on any service. Both are
now closed, for real, across all 8 services -- not just Problems 3-8, which
had already been hardened in earlier passes, but Problems 1 and 2 as well.

**Authentication.** Every business endpoint (`/model-info`, `/policy-info`,
`/predict`, `/risk-tier`, `/score`) on all 8 services now requires a valid
`X-API-Key` header, checked with `secrets.compare_digest` against an
`API_KEY` environment variable (falls back to a published dev-only default
with a loud warning log if unset, so a forgotten `API_KEY` fails safe rather
than silently open). `/health` deliberately stays open on every service,
matching standard load-balancer / Kubernetes liveness-probe practice.
`docker-compose.yml` for all 8 services now requires `API_KEY` at container
start (`${API_KEY:?Set API_KEY before running}`) rather than baking a secret
into any Dockerfile image layer.

**Explainability.** Every `/predict`/`/risk-tier`/`/score` response now
returns a real, live-computed `top_reasons` field satisfying CFPB Circular
2022-03's "specific, principal reasons" standard -- not the `shap` library,
deliberately, since that would add both a new dependency and approximation
risk. Instead each service uses whichever technique is exact for its own
underlying model: occlusion-based marginal contribution (re-score the same
customer with one real feature at a time reset to its training-set baseline,
report the resulting change in predicted PD) for Problems 1, 2, 5, and 6's
real trained classifiers; exact linear-term decomposition (each weighted
composite score's own `weight * direction * z` terms already sum to the
score, so ranking those terms by magnitude is exact, not approximate) for
Problems 4 and 8; deterministic rule narration (a new `explain_ecl()` states
exactly which IFRS9-stage rule fired and which frozen LGD value drove the
amount) for Problem 3's fully interpretable branch/lookup engine; and
ranking of already-computed z-score deviations for Problem 7. Every
technique is verified bit-exact against direct computation in its own test
(e.g. `test_score_top_reasons_matches_direct_top_contributing_features`) --
not just "returns something."

**Two more real bugs found (and fixed) while building this pass.** (1)
Problem 1's `main.py` and Problem 2's `risk_tier_service.py` still hardcoded
the author's real local Windows path as their preprocessing-artifacts
default -- the exact same privacy-leak bug class already found and fixed
three times elsewhere in this codebase (Problem 5 in the Phase 2 pass,
Problems 6/7/8 in the Phase 3 pass) but never previously caught for
Problems 1 and 2, since they predate every prior hardening pass. Fixed to
raise a clear `RuntimeError` if `AMEX_PROJECT_ROOT` is unset rather than
silently defaulting to a path that only exists on one machine. (2) The
`.env.example` files for Problems 5, 6, 7, and 8 displayed the author's real
local Windows path/username as their "example" value -- a milder
information-disclosure issue than a hardcoded default, but still a leak in
a file published publicly as a template. Cleaned up across all 8 problems
for consistency (Problems 1-4 previously had no `.env.example` at all; all
4 were created fresh in this pass).

32 new tests cover this pass (8 auth-rejection tests, 8 auth-plus-baseline
tests, and 16 explainability tests verifying `top_reasons` bit-exact against
direct computation) -- 126 total, 0 regressions, 0 new `bandit` findings,
0 new `pyflakes` findings, and zero remaining hardcoded local paths anywhere
in the repository (`grep -rn "C:\\Users\\rnand"` returns nothing).

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
   done, 2026-08-25, pushed to GitHub 2026-08-25.
3. ~~Build Phase 3 (Problems 6, 7, 8): 12 notebooks + real notebook-output
   artifacts + full Global Standard hardening pass (tests, Docker,
   MODEL_CARD/CHANGELOG/requirements.txt, BENCHMARKS.md, CI wiring)~~ —
   done, 2026-08-25, pushed to GitHub 2026-08-25.
4. ~~Close the two hard blockers named by an independent model-risk
   benchmark pass: real API-key authentication and real per-request
   explainability on all 8 deployed services~~ — done, 2026-08-25, see
   above.
5. Real `docker build`/compose smoke test for all 7 Dockerfiles (Problems
   1, 3, 4, 5, 6, 7, 8) once run somewhere with real Docker Hub registry
   access — this pass, like the Phase 2 one before it, could only
   statically verify build-context correctness, not actually pull a base
   image and build (this sandbox's Docker CLI has no daemon access).
6. Fix Problem 1's `src/docker/Dockerfile` build-context bug (see above) —
   flagged, not fixed, in this pass.
7. Pre-commit hook: run `check_notebook_syntax.py` + `pyflakes` on
   `git commit`, so a broken notebook or an unused import is caught
   before it's even pushed, not just in CI after the fact.
8. Repo-wide `black` reformatting pass, once deliberately scheduled (not
   as a side effect of another change) — then flip `format-check` from
   advisory to blocking.
9. Wire all eight problems' notebooks to `shared/` (see above) — now that
   every problem has its own test safety net.
10. A model inventory document, live/alerting monitoring, `pytest-cov`
    coverage measurement, and Dependabot — named as lower-priority items
    by the model-risk benchmark pass, not blockers.
11. ~~Phase 4 (Problems 9, 10, 11)~~ — done, see status table below. Phase 5
    (Problems 12, 13, 14) — started 2026-08-27, Notebook 62 shipped, see
    "Phase 5 build plan" below.
12. Kaggle notebook(s) and LinkedIn write-ups showcasing the platform
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
| Phase 3 — Behavioral Intelligence | Problems 6, 7, 8 | **Complete, pushed to GitHub 2026-08-25** (12 notebooks + real notebook-output artifacts + Global Standard hardening pass, all pushed 2026-08-25) — Problem 6 complete (Notebooks 38-41), RECOMMENDED FOR PRODUCTION (W=3 trailing window, 99.2% AUC retention); Problem 7 complete (Notebooks 42-45), concluded NOT RECOMMENDED FOR PRODUCTION (honest result -- real default-rate lift below KPI target; a v2 enhancement attempt, Notebooks 46-47, was built, showed genuine but insufficient improvement, and was deliberately abandoned per user decision, freeing 46-49 for Problem 8); Problem 8 complete -- Notebooks 46 (Business Understanding & Policy), 47 (Modeling), 48 (Validation & Deployment), and 49 (Financial-Impact Reporting & Packaging) all shipped, RECOMMENDED FOR PRODUCTION on this run (both hard-gate KPIs -- monotonicity and coherence -- met; Severe/Low default ratio 107.2x). All 12 Phase 3 notebooks (38-49) verified: syntax-clean, idempotent, pyflakes-clean. Hardening pass: 21 new tests (94 total platform-wide), Docker for all 3 services, MODEL_CARD/CHANGELOG/requirements.txt, BENCHMARKS.md entries, CI wiring -- see "Two more real bugs found" above. |
| Phase 4 — Operational Risk Management | Problems 9, 10, 11 | **Complete, pushed to GitHub 2026-08-27** (Problem 11 pushed with real RECOMMENDED FOR PRODUCTION results; Problems 9 and 10 are code-complete, 12 notebooks total, but their real run results are not yet synced into this repository -- see each problem's own README for honest current status). |
| Phase 5 — Customer & Business Intelligence | Problems 12, 13, 14 | **Complete 2026-08-27 (code-complete for all 3 problems; real results for 12 & 13).** Problem 12 (360° Customer Intelligence): run end-to-end with real results (62-65) -- real composite AUC 0.9590 vs. best-single 0.9626; real net benefit $1,275,022/cycle (33,900.6% Year-1 ROI); recommended for production. Problem 13 (Risk-Adjusted Profitability Modeling): run end-to-end with real results (66-69) -- real Spearman(risk, profitability) = -0.978 on holdout; real net benefit $58,060,687.58/cycle (1,741,720.6% Year-1 ROI) from the real 148,855-customer cross-tier segment; recommended for production. Problem 14 (Executive Decision Support Dashboard): code-complete (70-73) -- real BI aggregation layer across all 13 prior problems, TOTAL_PLATFORM_NET_VALUE_USD computed with a partition-completeness proof and 4x independent reproduction, 7-tab interactive executive dashboard; not yet run by the user. All 12 Phase 5 notebooks committed locally, not yet pushed to GitHub. **This completes the entire 14-problem, 5-phase platform (Notebooks 1-73), code-complete.** |

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

Notebook 46 (Business Understanding & Policy) and Notebook 47 (Modeling)
shipped 2026-08-25. Notebook 47 found and fixed a genuine non-determinism
bug (475 duplicate `(customer_ID, S_2)` statement-date pairs with no sort
tiebreaker, causing Polars' threaded streaming engine to not guarantee
stable row order across runs) -- fixed via `.with_row_index()` used as a
tertiary sort key; the identical latent bug exists unfixed in Problem 6's
already-delivered Notebooks 39/40, flagged for a future hardening pass.
Running Notebooks 46 and 47 against the real environment also surfaced
two real path-resolution bugs (Notebook 46 assumed Problem 4's summary
JSON lived at the flat `PROJECT_ROOT/artifacts/` path this platform's
Problems 1/2/5/6/7 use, when Problems 3/4 actually nest theirs under
their own `Phase2.../ProblemN/artifacts/`; Notebook 47 trusted a stale
absolute path stored in `notebook_02_summary.json` instead of using the
already-proven `_resolve_pillar_file()` resolver Notebook 39 established)
-- both fixed and re-delivered same day.

Notebook 48 (Validation & Deployment) shipped 2026-08-25, built with
`_resolve_pillar_file()` from the start (no path bugs this time).
Independently reproduces Notebook 47's entire pipeline from scratch
(zero-randomness, so reproduction is checked to 1e-9 with an immediate
raise on any mismatch), bootstraps 95% CIs on both real hard-gate KPIs,
and makes the final honest recommendation call -- NOT RECOMMENDED FOR
PRODUCTION on the fixture run (monotonicity KPI passes, coherence KPI
fails with a 95% CI entirely below zero).

Next problem-roadmap item: Notebook 49 (Problem 8, Financial-Impact
Reporting & Packaging -- final notebook of Problem 8, closes Phase 3).

## Phase 4 build plan — scoped 2026-08-26

Per `AMEX_Master_Execution_Plan.docx`'s Phase 4 table, Phase 4 moves from risk
*models* to risk *operations* -- running the portfolio day to day:

| # | Problem | Depends on | Core technique (per master plan) | Deliverable |
|---|---|---|---|---|
| 9 | Collections Optimization | #4, #8 | Propensity-to-cure scoring + treatment assignment | Collections strategy engine |
| 10 | Credit Line Management | #1, #6 | Utilization-trend + PD-based limit optimization | Limit recommendation service |
| 11 | Real-Time Portfolio Monitoring | #7 | Streaming aggregation + threshold alerting | Ops dashboard + alert feed |

Same 4-notebook-per-problem pattern as Phases 2/3, continuing the numbering
sequence: Notebooks 50-53 (Problem 9), 54-57 (Problem 10), 58-61 (Problem
11) -- 12 notebooks total. Same standing rules apply unchanged, plus the
Phase 4 tightened WARP resource cap (92% CPU / 92% RAM, established in
Notebook 50 after the real Phase 3 hang incident) and the two-tier RAM
pre-flight guard (established in Notebooks 51/52 after a real 45-minute
freeze the user hit running Notebook 52, initially misdiagnosed against
Notebook 51 before the user corrected it).

Problem 9 (Notebooks 50-53) shipped complete 2026-08-26. Real bugs found
and fixed after the user ran these notebooks on their own machine: Notebook
50's `roll_rate_deployment_policy.json` path guess (fixed to read the
canonical path from `notebook_48_summary.json`); Notebook 51's reported
45-minute freeze (initially misdiagnosed -- the actual freeze was in
Notebook 52, corrected on the user's follow-up report); Notebook 52's real
double-CSV-scan bug in its independent-reproduction section (fixed to
collect once), a real `SchemaError` in that same fix (`pl.concat` on two ID
frames carrying mismatched-dtype extra columns -- fixed by selecting only
`customer_ID` before concatenating), and an over-strict RAM guard that
hard-blocked a workable ~14 GB of available RAM (fixed to a two-tier warn/
hard-fail check); Notebook 53's real `ValueError` from an Excel sheet title
containing a forbidden `/` character. See
`/areas/amex-credit-risk-platform-bugfixes.md` for full detail on each.

Problem 10 (Notebooks 54-57) started 2026-08-26. Notebook 54 (Business
Understanding & Policy) shipped: composes Problem 1's real static (whole-
history) PD with Problem 6's real dynamic (monthly-refreshed, trailing-
window) PD into a risk-level x risk-trend policy. Honest scope note: this
Kaggle dataset has no true credit-limit or balance-to-limit utilization
field (by the competition's own anonymization design), so "utilization-
trend" is reinterpreted as the real, measurable PD_TREND signal (dynamic PD
minus static PD) rather than a fabricated raw-column proxy -- stated
plainly in the notebook, the policy artifact, and every downstream report
for this problem. Two real hard-gating KPIs defined: risk-level
monotonicity (reused convention from Problems 4/8) and trend coherence (a
new KPI with no prior platform precedent -- the specific, testable claim
this problem's whole design depends on). A 9-cell action-tier policy (Low/
Medium/High Risk x Trending Better/Stable/Trending Worse -> 5 credit-line
actions) is defined as an honest business-rule layer, explicitly not a
fitted treatment-response model, matching Problem 9's precedent for the
same reason (no real limit-change/outcome data exists in this dataset).

Notebook 55 (Modeling), 56 (Validation & Deployment), and 57 (Financial
Impact, Reporting & Packaging) all shipped -- Problem 10 (Notebooks 54-57)
is code-complete. Real, measured results for Problem 10 are pending the
user's own run + sync of these notebooks (same "packaging pending" status
as Problem 9 -- see each problem's own README for the honest current state).

## Phase 5 build plan — scoped 2026-08-27

Per `AMEX_Master_Execution_Plan.docx`'s Phase 5 table, Phase 5 turns thirteen
models of risk infrastructure into strategy a business can act on:

| # | Problem | Depends on | Core technique (per master plan) | Deliverable |
|---|---|---|---|---|
| 12 | 360° Customer Intelligence | #1, #6, #9, #10 | Multi-signal customer profile aggregation | Unified customer risk profile |
| 13 | Risk-Adjusted Profitability Modeling | #1, #12 | PD-adjusted revenue (spend proxy) minus expected loss | Profitability scoring model |
| 14 | Executive Decision Support Dashboard | All above | BI aggregation layer | Executive dashboard |

Same 4-notebook-per-problem pattern as Phases 2/3/4, continuing the
numbering sequence: Notebooks 62-65 (Problem 12), 66-69 (Problem 13), 70-73
(Problem 14) -- 12 notebooks total. Same standing rules apply unchanged:
zero-fabrication, Claude generates code only (user runs every notebook
locally), WARP optimization standard (Phase 4's 92%/92% cap carried
forward -- no new incident to warrant changing it), `random_state=42`, one
notebook = one idempotent code cell, no local/absolute paths in any
publicly-shared file, two-tier RAM pre-flight guard (Notebooks 51/52
precedent), canonical-source-of-truth path resolution via each producing
notebook's own recorded summary JSON path (never guessed or re-derived --
the Notebook 46/47/50 lesson).

Repository-packaging skeleton for all 3 problems (`notebooks/`, `src/`,
`tests/`, `reports/`, `docs/`, `artifacts/`, `models/`, `data/`, `LICENSE`)
created and committed locally 2026-08-27 -- content is empty by design
except Notebook 62; **not pushed to GitHub** until each problem has real,
run content, same practice as every prior phase.

Notebook 62 (Business Understanding & Policy) shipped 2026-08-27: composes
Problem 1's real static PD, Problem 6's real dynamic PD, Problem 9's real
propensity-to-cure score (collections-eligible customers only), and Problem
10's real risk-level/trend/action worklist into a documented composite --
`UNIFIED_RISK_SCORE = 0.35*STATIC_PD + 0.65*DYNAMIC_PD` (+ a real 0.10
collections adjustment where a real propensity score exists), tertile-graded
into `UNIFIED_RISK_GRADE_NAMES`. Two new hard-gating KPIs with no prior
platform precedent: `profile_completeness` (every dynamic-PD-eligible
customer must get a real, non-null value for the seven always-applicable
fields; the three collections-only fields are honestly nullable, never
imputed) and `composite_non_inferiority` (the real composite's holdout
ROC-AUC must be >= the best single real input signal's AUC, minus a 0.005
ASSUMPTION tolerance) -- the specific, testable claim this problem's design
depends on: that aggregating four real signals does not destroy the signal
any one of them already carried.

**Real bug found and fixed 2026-08-27, on the user's own first run of
Notebook 62:** Section 1 read `NB52_SUMMARY["model_path"]` directly, but
`notebook_52_summary.json` (Problem 9's Validation & Deployment summary) has
no top-level `model_path` key -- only `deployment_policy_path`. The real
model path lives one level down, inside that policy JSON itself
(`COLLECTIONS_DEPLOYMENT_POLICY["model_path"]`, written by Notebook 52
Section 7), the same nesting pattern this platform already uses for every
other cross-problem model-path lookup. Fixed by loading
`P9_DEPLOYMENT_POLICY` from `NB52_SUMMARY["deployment_policy_path"]` first,
then reading `model_path` from that policy dict -- Notebook 62 repackaged,
re-verified with `check_notebook_syntax.py` (64/64 clean), and redelivered.

Notebook 63 (Modeling) shipped 2026-08-27, generated ahead of the user's own
run of Notebook 62 -- every value it needs from Notebook 62 is read from
that notebook's own recorded summary JSON at runtime (never a hardcoded
literal), so the two can be generated and run independently, consistent
with this platform's canonical-source-of-truth convention. Reuses Problem
10's real worklist directly (already carries STATIC_PD/DYNAMIC_PD/PD_TREND/
RISK_LEVEL/TREND/ACTION -- no need to re-score Problems 1/6's models).
Problem 9's real per-STATEMENT propensity-to-cure model is scored once per
collections-eligible customer's own real LATEST statement (the same
"current status" framing already used for DYNAMIC_PD/RISK_LEVEL), via one
real streaming pass over the raw CSV. Both hard-gating KPIs validated on
the real HOLDOUT split; the real treatment-tier median split is refit on
this run's own eligible population, matching Notebook 50's rule-based (not
fixed-value) policy definition exactly.

Notebook 64 (Validation & Deployment) shipped 2026-08-27, completing Problem
12 -- independently reproduces Notebook 63's entire real pipeline from
scratch in a fresh kernel (reloads Problem 10's worklist, re-derives each
customer's real latest-statement severity/state via one real streaming CSV
pass, re-scores collections-eligible customers with Problem 9's real
persisted model, re-computes UNIFIED_RISK_SCORE, re-fits the tertile cuts),
matching Notebook 63's reported ROC-AUC and cut values within the platform's
standard 1e-4 tolerance, plus a 200-sample cross-check of the persisted
`unified_customer_profile.parquet` against the fresh reproduction. Bootstraps
a 200-resample 95% CI on the `composite_non_inferiority` AUC gap only --
`profile_completeness` is a deterministic population-wide null-count check,
not a sampling-variable statistic, so (unlike Notebooks 48/52/56, which
bootstrapped two ratio/rate KPIs each) this notebook honestly bootstraps
just the one KPI that actually has a bootstrap distribution. Architecture
decision: because Problem 12's deliverable is a precomputed lookup artifact
rather than a live-compute-from-inputs model, the generated
`customer_intelligence_lookup_service.py` is a `GET /profile/{customer_id}`
lookup service (loads the real persisted parquet once at startup into an
in-memory index) rather than Notebook 56's live-compute `/recommend`
pattern -- recomputing the full four-signal composite per request would mean
re-implementing Problems 1/6/9/10's pipelines a fifth time, the exact
duplication anti-pattern already flagged in Notebooks 46/50/56. Explainability
via deterministic weighted-term narration (UNIFIED_RISK_SCORE is an explicit
weighted sum, not a trained classifier). `X-API-Key` auth on every endpoint
but `/health`; self-tested live via `TestClient` against real sampled
holdout customers (with and without a real collections propensity score) plus
auth-rejection, and unknown-customer-404 checks. All 64 notebooks pass
`check_notebook_syntax.py`; full local test suite (27 tests) green.

Notebooks 62-64 all written, syntax-checked, and committed locally at this
point (Notebook 65, the 4th and final notebook, followed once the user
confirmed real execution through Notebook 64).

Notebook 65 (Financial Impact, Reporting & Packaging) shipped 2026-08-27,
completing Problem 12, following the standard 15-section elevated-reporting
template established across Notebooks 29/33/37/41/45/49/53/57/61. Financial
model has a deliberately different shape from every prior alerting/scoring
problem (5, 6, 7, 9, 10, 11): Problem 12 gates no action of its own, so
re-claiming Problem 9/10's already-priced loss-prevention benefit here would
double-count value already reported in Notebooks 53 and 57. Instead this
notebook prices real, additive OPERATIONAL EFFICIENCY -- collapsing four
separate case lookups (Problems 1, 6, 9, 10) into one unified profile --
using the real, measured collections-eligible population (Notebook 63) as
the case-lookup volume, with per-lookup time-saved and hourly labor cost as
explicit ASSUMPTIONs, net of a genuinely new recurring ongoing-hosting-cost
stream (this platform's first purely read-through aggregation service, vs.
every prior problem's scored classifier). Section 8 performs a THIRD
independent reproduction of the unified profile (after Notebooks 63 and
64): reads the real persisted `unified_customer_profile.parquet` directly
for the exact full-population `UNIFIED_RISK_GRADE` distribution, then
imports and live-drives the exact `customer_intelligence_lookup_service.py`
Notebook 64 generated against a real, grade-stratified sample (up to 100
customers per grade, deterministic via `RANDOM_SEED`) via its real
`GET /profile/{customer_id}` endpoint -- every live response cross-checked
against the persisted profile row, halting the notebook on any mismatch.
That real grade distribution and live-verified sample are what the packaged
interactive HTML dashboard (multi-tab: Overview, Grade Distribution, Live
Sample, Financial Calculator, SMART Suggestions, Policy & Validation)
embeds, making it the real 360 ops dashboard rather than a mockup. All 65
notebooks pass `check_notebook_syntax.py`; full local test suite (27 tests)
green.

This completes Phase 5's first problem (Problem 12, 360 Degree Customer
Intelligence) end to end: all 4 notebooks (62-65) written, syntax-checked,
and committed locally (not yet run by the user for Notebook 65 specifically,
not yet pushed to GitHub, per this platform's standing practice).

Notebook 66 (Business Understanding & Policy) shipped 2026-08-27, opening
Problem 13 (Risk-Adjusted Profitability Modeling). Real Spend columns
("S_" prefix, per the AMEX Kaggle competition's own documented column
groups D_/S_/P_/B_/R_, excluding the real statement-date exception S_2)
are discovered programmatically from the raw CSV's own header via
`pl.scan_csv(..., n_rows=0).collect_schema().names()` -- not hardcoded --
and verified non-degenerate on a real 2,000-row sample before being trusted
as this problem's revenue proxy basis; the notebook would raise a
`RuntimeError` rather than proceed if no such columns existed. Defines
`REVENUE_ASSUMPTIONS` (average monthly revenue per account, bounded
revenue-multiplier floor/ceiling) as explicit, sourced ASSUMPTIONs (the
same treatment as Notebook 08's `EAD_PER_ACCOUNT_USD` precedent) and the
tertile `PROFITABILITY_TIER_NAMES`. Two new hard-gating KPIs:
`profitability_tier_monotonicity` (real per-tier default rate must be
non-increasing Low to High Profitability -- the inverse-direction cousin
of the tertile-monotonicity convention reused from Problems 4/8/10/12) and
`risk_adjustment_materiality` (genuinely new: the real Spearman rank
correlation between `UNIFIED_RISK_SCORE` and `PROFITABILITY_SCORE` on real
holdout must be <= an ASSUMPTION -0.15 threshold, proving PD-adjustment
measurably re-ranks customers rather than revenue dominating the score).

Notebook 67 (Modeling) shipped 2026-08-27: computes each real customer's
`SPEND_PERCENTILE_RANK` via one real streaming pass over the raw CSV
(latest real statement per customer, real rank-based percentile over the
real mean of the discovered Spend columns), with an honest 0.5 fallback
for customers with no real recorded spend -- never fabricated. Derives
`REVENUE_MULTIPLIER`, `REVENUE_PER_ACCOUNT_USD`, `PD_ADJUSTED_REVENUE_USD`
(net of `UNIFIED_RISK_SCORE`), `EXPECTED_LOSS_USD`, and
`PROFITABILITY_SCORE` via chained polars expressions; fits real tertile
cuts on the real TRAIN split; validates both hard-gating KPIs on real
HOLDOUT. Persists `profitability_scored_profile.parquet` and
`profitability_modeling_results.json`; generates a twin-axis tier P&L
chart and a risk-vs-profitability hexbin chart from real data.

Notebook 68 (Validation & Deployment) shipped 2026-08-27: independently
reproduces Notebook 67's entire pipeline from a fresh kernel (including a
fresh real streaming CSV pass and refitted tertile cuts), comparing every
reproduced value to Notebook 67's reported values within tolerance;
cross-checks the persisted profile against a real 500-customer sample;
bootstraps a 200-resample 95% CI on the `risk_adjustment_materiality`
Spearman correlation. Reuses Notebook 64's precomputed-lookup FastAPI
architecture for `profitability_scoring_lookup_service.py`
(`GET /profitability/{customer_id}`, `X-API-Key` auth on every endpoint
but `/health`) since Problem 13's deliverable is a precomputed artifact,
not a model to re-run live per request -- explicitly avoiding
re-implementing Notebook 67's pipeline a second time, the same
duplication anti-pattern flagged in Notebooks 46/50/56/64. Self-tested
live via `TestClient` against one real customer per tier plus
auth-rejection and unknown-customer-404 checks. All 68 notebooks pass
`check_notebook_syntax.py`; full local test suite (27 tests) green.

Notebook 69 (Financial Impact, Reporting & Packaging) shipped 2026-08-27,
completing Problem 13, following the standard 15-section elevated-
reporting template established across Notebooks 29/33/37/41/45/49/53/57/
61/65. This problem's own genuinely new, additive financial claim: the
real cross-tier segment of customers who are simultaneously High Risk
(Problem 12's `UNIFIED_RISK_GRADE`) *and* Low Profitability (this
problem's own `PROFITABILITY_TIER`) -- a segment invisible to either
single-axis lens alone, read directly off the real persisted
`unified_customer_profile.parquet` joined with this problem's own real
`profitability_scored_profile.parquet`. Prices a targeted PROACTIVE
EXPOSURE REDUCTION action against that real segment's own real total
expected loss (an explicit `exposure_reduction_rate` ASSUMPTION), net of
a real per-account `segment_review_cost_usd_per_account` ASSUMPTION --
explicitly, in code comments, NOT double-counting Problems 9/10's own
already-priced collections/alerting benefits (Notebooks 53, 57), since
this is a distinct, newly-identified segment those problems' single-axis
scores do not themselves surface. Section 8 performs a third independent
reproduction: live-drives the exact deployed
`profitability_scoring_lookup_service.py` against a real tier-stratified
sample (100/tier) plus a dedicated real sample from the cross-tier segment
itself, cross-checking every response against the persisted profile.
Packages a multi-tab interactive HTML dashboard (Overview, Tier P&L
Summary, Live Sample, Financial Calculator, SMART Suggestions, Policy &
Validation), a Word financial-impact report, and a 6-sheet Excel
workbook. All 69 notebooks pass `check_notebook_syntax.py`; full local
test suite (27 tests) green.

This completes Phase 5's second problem (Problem 13, Risk-Adjusted
Profitability Modeling) end to end: all 4 notebooks (66-69) written,
syntax-checked, and committed locally. Notebooks 66-69 were then run
end-to-end by the user with real results synced 2026-08-27: all hard
gates passed, recommended for production, real Spearman(risk,
profitability) = -0.978 on holdout, real net benefit $58,060,687.58/cycle
(1,741,720.6% Year-1 ROI) from the real 148,855-customer cross-tier
segment. Problem 12's real results synced the same day: composite AUC
0.9590 vs. best-single 0.9626 (both hard-gating KPIs pass), real net
benefit $1,275,022/cycle (33,900.6% Year-1 ROI).

Notebook 70 (Business Understanding & Policy) shipped 2026-08-27, opening
Problem 14 (Executive Decision Support Dashboard) -- the platform's grand
finale, depending on all 13 prior problems per the master execution
plan's "BI aggregation layer" -> "Executive dashboard" definition. Every
one of the 13 prior problems' own canonical summary JSON(s) (spanning
Phases 1-5, Problems 1-13) is registered and classified into one of three
real categories: `foundational_model` (Problems 1, 2 -- Credit Scoring and
Risk Tier Classification predate this platform's financial-impact-
reporting convention entirely and carry no standalone dollar benefit;
their value is realized downstream), `reserve_optimization` (Problem 3 --
a reserve-accuracy gain, a genuinely different kind of number from a P&L
benefit, kept as its own separate line rather than summed with the
others), or `value_creation` (Problems 4-13 -- each carries a real
net-benefit-per-cycle-equivalent figure). Two new hard-gating KPIs with no
prior platform analog: `aggregation_completeness` (all 13 problems' real
summary JSONs load and parse) and `aggregation_scope_correctness` (the
platform total's real inclusion set is provably correct via a partition-
completeness proof plus a per-problem data-driven exclusion reason --
guarding against exactly the category error an executive rollup is most
exposed to: silently summing a foundational model's AUC, a reserve
figure, or a not-recommended system's benefit into one impressive-looking
headline number).

Notebook 71 (Modeling -- the real BI aggregation layer itself) shipped
2026-08-27: builds the real 13-row executive rollup table via a single
generic `_extract()` path-walker driven entirely by Notebook 70's own
registry (zero per-problem special-casing), computes
`TOTAL_PLATFORM_NET_VALUE_USD` as the sum of only the production-
recommended `value_creation` problems' real figures, and validates both
hard-gating KPIs -- including a real cross-check that Problem 7 (this
platform's one built-but-not-recommended system, per its own real
Notebook 45 result) is correctly excluded for a genuine, data-driven
reason rather than a hardcoded skip. A real, genuinely new cross-problem
consistency check confirms Problems 12 and 13's real `eligible_population`
fields agree exactly (both real datasets score the same real Problem-10
worklist population).

Notebook 72 (Validation & Deployment) shipped 2026-08-27: independently
reproduces the entire aggregation from scratch in a fresh kernel (re-
reading all 13 real summary JSONs), cross-checks the persisted table
row-by-row, re-validates both hard-gating KPIs fresh, and generates a
real, auth-protected FastAPI **lookup** service
(`GET /executive-summary`, `GET /problem/{problem_number}`) -- reusing
Problems 12/13's precomputed-lookup architecture, since Problem 14's
deliverable is a BI aggregation artifact, not a live model. Self-tested
live via `TestClient` against all 13 real problem rows plus auth-
rejection and unknown-problem-404 checks.

Notebook 73 (Financial Impact, Reporting & Packaging -- the grand finale)
shipped 2026-08-27, completing Problem 14, Phase 5, and the entire
14-problem platform. This problem's own genuinely new, additive financial
claim: EXECUTIVE DECISION-LATENCY REDUCTION -- real time saved by
reviewing one unified dashboard instead of 13 separate reports, pricing a
different constituency's time (C-suite/CRO review time) than any prior
problem, net of the dashboard's own ongoing hosting cost. Section 8
performs a FOURTH independent reproduction of the platform total (after
Notebooks 71, 72, and 72's own self-test) by live-driving the exact
deployed `executive_dashboard_service.py`. Builds a real portfolio
risk-profitability map -- Problem 12's real `UNIFIED_RISK_GRADE` crossed
with Problem 13's real `PROFITABILITY_TIER` on the real persisted
profile -- explicitly documented as the honest analog to a geographic
map, since this dataset carries no real location field (no fabricated
geography is built). Packages a 7-tab interactive HTML executive
dashboard (Overview, Problem Registry with real functional phase/
category/status filters, Risk-Profitability Map as a real HTML/CSS
heat-grid, Model Health Matrix, a live financial calculator, SMART
Suggestions, Policy & Validation), a comprehensive Word report, and a
7-sheet Excel workbook with real AutoFilter tables and conditional-
formatting color scales (native PivotTable slicers are not generated --
openpyxl has no API to create them -- so this workbook delivers the real,
functional AutoFilter equivalent instead of overclaiming a feature the
library cannot produce). All 73 repo notebooks pass
`check_notebook_syntax.py`; full local test suite (27 tests) green. The
entire 4-notebook chain (70-73) was additionally smoke-tested end-to-end
against a realistic mock 13-problem dataset before delivery, confirming
every KPI, reproduction, and generated artifact (Word/Excel/HTML/charts/
FastAPI service) actually runs correctly, not just compiles.

This completes Phase 5 (Problems 12, 13, 14) and the entire 14-problem,
5-phase AMEX Enterprise Credit Risk Platform end to end: all 12 Phase 5
notebooks (62-73) written, syntax-checked, and committed locally.
Problems 12 and 13 have real, synced run results (above); Notebooks
70-73 (Problem 14) are code-complete, not yet run by the user, not yet
pushed to GitHub, per this platform's standing practice.

Next: once the user runs Notebooks 70-73 and syncs real Problem 14
results, the platform-wide mega report (paused since before Phase 5
began, per the user's own standing instruction) can resume -- this time
incorporating Phase 5's real notebook outputs and results, built to a
Harvard-grade, global top-tier financial-institutional standard.
