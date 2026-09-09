# Changelog -- AMEX RiskIQ Enterprise Credit Risk Platform (Platform-Wide)

This is a platform-level index over all 14 problems' own `CHANGELOG.md`
files (each problem's own file has the full detail: exact test counts,
port numbers, code-level fixes). Dates below are real commit dates from
this repository's git history (`git log`), grouped here so the platform's
build story reads as one timeline. Nothing here is estimated or
reconstructed -- every line traces to a real commit.

## Unreleased

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
