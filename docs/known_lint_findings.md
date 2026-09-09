# Known Lint Findings (Historical)

`pyflakes` ran as an advisory (non-blocking) CI step from 2026-08-24 through
2026-09-09, gating the `lint` job in `.github/workflows/code-quality.yml`
(not `ci.yml`, which only covers notebook-syntax checks and pytest). It was
run once against the existing, already-verified `src/` files at the time
the workflow was added, to establish a baseline rather than let
pre-existing findings silently fail the very first CI run.

## Fixed on 2026-09-09

All three findings below were fixed directly, in both the generated `src/`
file and the notebook cell that generates it (so the two never drift
apart), and `pyflakes` now reports zero findings across the full scope the
`lint` job checks. `continue-on-error` has been removed from the `lint`
job in `.github/workflows/code-quality.yml` -- a real lint regression now
fails the build.

| File | Finding | Fix |
|---|---|---|
| `01_Problem1_Credit_Scoring_PD_Prediction/src/monitoring/monitoring_job.py` | `joblib` imported but unused | Removed the unused `import joblib` line, in the `.py` file and in the corresponding line of `12_monitoring.ipynb`'s generator cell. |
| `09_Problem9_Collections_Optimization/src/collections_scoring_service.py` | `typing.Dict` imported but unused | Changed `from typing import Dict, List, Optional` to `from typing import List, Optional` (both `List` and `Optional` are genuinely used elsewhere in the file), in the `.py` file and in `52_collections_optimization_validation_deployment.ipynb`'s generator cell. |
| `13_Problem13_Risk_Adjusted_Profitability_Modeling/src/profitability_scoring_lookup_service.py` | f-string missing placeholders (line 120) | The `rationale=` value is two implicitly-concatenated string literals, and *neither* half actually uses `{}` interpolation, so pyflakes flagged the whole expression. Removed the `f` prefix from both halves (they're plain strings), in the `.py` file and in `68_profitability_modeling_validation_deployment.ipynb`'s generator cell. |

This file is kept as a record of the fix rather than deleted, since the
git history and the reasoning behind why these were deferred (avoiding
notebook/generated-file drift) are useful context for anyone auditing the
CI hardening timeline.
