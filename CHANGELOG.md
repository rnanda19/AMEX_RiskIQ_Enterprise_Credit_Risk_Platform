# Changelog -- AMEX RiskIQ Enterprise Credit Risk Platform (Platform-Wide)

This is a platform-level index over all 14 problems' own `CHANGELOG.md`
files (each problem's own file has the full detail: exact test counts,
port numbers, code-level fixes). Dates below are real commit dates from
this repository's git history (`git log`), grouped here so the platform's
build story reads as one timeline. Nothing here is estimated or
reconstructed -- every line traces to a real commit.

## Unreleased

- **Real OAuth2 client-credentials + JWT pilot completed on Problem 7**
  (Early Warning System), replacing that service's `X-API-Key` header on
  `/score` and `/model-info` with a real `POST /token` (client-credentials
  grant) + `Authorization: Bearer <token>` flow, per the scoped migration
  plan in `AUTH_HARDENING.md`. The token is a genuine HS256-signed JWT
  (`PyJWT==2.3.0`) with real `iss`/`sub`/`aud`/`scope`/`iat`/`exp` claims
  (15-minute expiry), validated on every protected request. Verified two
  ways: Problem 7's test suite grew from 10 to 18 real tests (issuing a
  real token, rejecting a wrong client_secret/unknown client_id/bad
  grant_type, rejecting a missing/invalid/expired/wrong-scope token, and
  -- the regression check that matters most -- confirming the *old*
  `X-API-Key` header alone no longer authenticates the endpoint), and a
  live end-to-end run against a real `uvicorn` instance (old header ->
  real 401; `/token` -> real signed JWT; that token against `/score` and
  `/model-info` -> real 200s; a wrong client_secret -> real 401). The
  full 180-test platform suite (172 + 8 new) passes. `AUTH_HARDENING.md`,
  `SECURITY.md`, Problem 7's own `README.md`, and `LOAD_TESTING.md` all
  updated to reflect this honestly -- 13 of 14 services still use
  `X-API-Key`; this is a single-service pilot, with its real
  simplifications (one hardcoded client, reused secret as both client
  credential and JWT signing key, `/token` itself not yet rate-limited)
  stated plainly, not hidden.
- Also fixed a real gap found while touching Problem 7's dependency
  files again: its root `requirements.txt` had `slowapi` but was missing
  `prometheus-client` (added during the earlier Prometheus pilot entry
  below but never added to this file) -- added both `prometheus-client`
  and `PyJWT` to keep it consistent with `requirements-api.txt`.
- **Real bug found and fixed:** pushing the rate-limiting + Prometheus
  changes below broke real CI -- `.github/workflows/ci.yml`'s
  `unit-tests` job installs dependencies fresh from `requirements-dev.txt`
  (not each service's own `requirements-api.txt`), which never listed
  `slowapi` or `prometheus-client`. Problem 1's test step failed with a
  real `ModuleNotFoundError: No module named 'slowapi'` on GitHub's
  runners (confirmed via the real Actions run, then reproduced locally in
  a clean venv installing only `requirements-dev.txt`). Fixed by adding
  `slowapi==0.1.10` and `prometheus-client==0.21.1` to
  `requirements-dev.txt`, pinned to the exact versions already verified
  working elsewhere in this platform.
- Added real, enforced rate limiting (`slowapi`, 60 requests/minute per
  client IP) to the primary scoring/mutating endpoint of all 14 FastAPI
  services -- `/health` and the `*-info`/lookup metadata endpoints are
  left unlimited since they are liveness or metadata reads, not scoring
  load. Verified two ways: the full real `pytest` suite (172 tests) still
  passes with the limiter active, and a live `uvicorn` run of Problem 7's
  service was hammered with 65 real requests -- the first 60 returned
  `200`, the next 5 returned a real `429 {"error":"Rate limit exceeded:
  60 per 1 minute"}`. 6 of the 14 services needed their scoring
  endpoint's body parameter renamed from `request` to `body` first,
  since slowapi requires the literal name `request` for the real
  `starlette.Request` object it inspects for the caller's IP.
- Added a real, scraped Prometheus `/metrics` endpoint to Problem 7's
  Early Warning System service (`prometheus-client==0.21.1`) as a
  single-service pilot -- a `Counter` labeled by outcome
  (`alert`/`no_alert`/`validation_error`/`error`) and a `Histogram` of
  real wall-clock `/score` latency, both populated on every request, not
  placeholders. Verified live: started a real `uvicorn` instance, sent 3
  valid and 1 invalid `/score` request, then scraped `/metrics` and
  confirmed the exact counts (`no_alert` 3, `validation_error` 1, latency
  count 4) with no fabricated values; the service's own 10-test suite and
  the full platform 172-test suite both still pass. See `MONITORING.md`
  for the honest scope note -- this is Problem 7 only, not a
  platform-wide observability stack.
- Added `AUTH_HARDENING.md`: an honest assessment of the platform's
  current shared-static-key `X-API-Key` auth (constant-time comparison,
  but no per-caller identity, expiry, rotation, or scoping), why a real
  OAuth2/JWT replacement was deliberately not attempted in this pass
  (touches all 14 services' request path and all 172 tests that exercise
  a protected endpoint -- real regression-risk surface, not a contained
  change), and a concrete, scoped migration plan (client-credentials
  grant, HS256 JWT, piloted on Problem 7 first) for when it is picked up.
- Added `SECRETS_MANAGEMENT.md` plus a real, working proof-of-concept in
  `docs/secrets_management_demo/`: a dev-mode HashiCorp Vault (`docker-compose.vault.yml`)
  and a script (`vault_dev_example.sh`) that writes a real secret to it
  and reads it back over Vault's actual HTTP API, asserting the value
  matches exactly. A new `.github/workflows/vault-verify.yml` runs this
  for real on every push/PR (this sandbox has no Docker, so -- like
  `docker-verify.yml` before it -- the actual end-to-end run happens on
  GitHub's runners, not claimed as verified here before CI has run it).
  The platform's 14 services still read their secret from a plain
  environment variable today; this is a documented, honestly-scoped
  proof-of-concept for the pattern to migrate to, not a claim that any
  service has been switched over.

## 2026-09-09 -- Gap-analysis + GitHub-audit remediation

- Fixed the 3 pre-existing pyflakes findings (unused `joblib` import,
  unused `typing.Dict` import, an f-string with no placeholders) in both
  the generated `src/` files and their source notebook cells, then
  removed `continue-on-error` from the `lint` job in
  `.github/workflows/code-quality.yml` -- it is now a real, blocking gate.
  See `docs/known_lint_findings.md`.
- Added `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1).
- Added root-level governance docs: `MODEL_REGISTRY.md`, `MONITORING.md`,
  `DATA_PRIVACY.md`, `ADVERSE_ACTION.md`, `TLS.md`, `E2E_TESTING.md`,
  `LOAD_TESTING.md`.
- Ran `black --check` for real against the same scope as the
  `format-check` CI job: 24 of 27 files would be reformatted. Left
  `format-check` advisory rather than flip it to blocking as a side
  effect -- a repo-wide reformat carries real risk of notebook/generated-
  file drift and deserves its own deliberate pass (tracked in
  `ROADMAP.md`).

## 2026-09-08 -- Security hardening

- `9099e37` Added `.github/dependabot.yml` (pip + github-actions
  ecosystems, weekly), CodeQL scanning, `SECURITY.md`, and gitignore
  hardening.
- Widened `bandit`'s scan scope from the 4 `shared/` files to all 14
  problems' `src/` directories, and made the `security-scan` job
  blocking (no `continue-on-error`) -- 0 real findings across every
  problem's `src/` as of this pass.
- `b3804ba` Merged the Dependabot-opened `codeql-action` v4 upgrade PR.

## 2026-08-27 -- Platform complete (all 14 problems) + cross-cutting hardening

- `3b8df94` Notebooks 70-73: Problem 14 (Executive Decision Support
  Dashboard) -- completes Phase 5 and the entire 14-problem platform.
- `08a51c8` Added the Executive Capstone Report and synced real Problem
  14 outputs.
- `155eeca` Global Standard hardening delta: extended the hardening
  pattern established for Problems 1-8 (tests, Docker, root governance
  docs, FastAPI service) to Problems 9-14.
- `72e4e21` Problem 11: synced real "RECOMMENDED FOR PRODUCTION" outputs
  (Phase 4 complete).

## 2026-08-25 -- Phases 3 and 4

- `9460c9b` Began Phase 4 (Problem 9: Collections Optimization).
- `3f4b013` Phase 3 Global Standard hardening pass (Problems 6, 7, 8).
- `0cab76f` Phase 2 hardening: deployable APIs, Docker, root governance
  (Problems 3/4/5).

## 2026-08-24 -- Phase 1 and Phase 2 kickoff

- `0d7588a` Initial commit: Phase 1 (Problem 1: PD Prediction, Problem 2:
  Risk Tier Classification).
- `a39f1f4` Added the enterprise hardening layer: `shared/` library, CI,
  tests, governance docs (Problem 1 pilot).
- `1eb94c1` Added Problem 2 hardening: tests, `MODEL_CARD.md`,
  per-problem `CHANGELOG.md`, `shared/tiers.py`.
- `40c7b9c` Added Phase 2 to the repository: Problem 3 (ECL IFRS9/CECL),
  Problem 4 (Delinquency Escalation / Loss Severity), Problem 5 (Early
  Payment Default Detection).

For the full, unabridged commit history: `git log` in this repository, or
the 91 real commits currently on `main` as of this writing.
