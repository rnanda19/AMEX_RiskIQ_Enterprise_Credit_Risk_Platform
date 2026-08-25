## What does this change?

Describe the change and which `ProblemN_.../` (or `shared/`, or root infra) it touches.

## Type of change

- [ ] Bug fix (non-breaking)
- [ ] New notebook / problem
- [ ] Infra / CI / tooling (no change to computed output)
- [ ] Documentation only
- [ ] Model / methodology change (see below)

## Verification checklist

Per `CONTRIBUTING.md` — check every box that applies before requesting review:

- [ ] `python -m pytest shared/tests ProblemN_.../tests -v` passes
- [ ] `python scripts/check_notebook_syntax.py .` passes (if any notebook changed)
- [ ] `pyflakes` clean on any changed `src/`/`tests/` (or new findings logged in
      `docs/known_lint_findings.md`)
- [ ] If this changes a notebook's computed output: re-ran it end to end and confirmed every
      downstream number/report/artifact is still consistent (no stale cached figures)
- [ ] No absolute/local file paths introduced into any notebook or public-facing file
- [ ] No fabricated numbers — every new figure is either computed live or an explicit, labeled
      `ASSUMPTION`

## If this is a model/methodology change

- [ ] The relevant `MODEL_CARD.md` is updated with the real, re-measured numbers
- [ ] Statistical validation was re-run (chi-square/PSI/bootstrap CI/calibration, as applicable)
      and the real result is included in this PR's description
