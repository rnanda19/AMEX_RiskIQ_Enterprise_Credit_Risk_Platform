---
name: Model improvement
about: Propose a change to a model's methodology, features, or validation approach
title: "[MODEL] "
labels: model-improvement
---

**Which model / MODEL_CARD.md is this about?**
e.g. `04_Problem4_Delinquency_Escalation_Loss_Severity/MODEL_CARD.md`.

**What's the proposed change?**
Architecture, feature set, validation method, or hyperparameters.

**What real, measured evidence supports it?**
This platform's zero-fabrication rule applies here too — a proposed improvement needs to be
backed by something measurable (a benchmark result, a statistical test, a real ablation), not
just a plausible-sounding intuition. If you've already run something, include the real numbers.

**What would this change, concretely?**
- Does it change model architecture/features? (would require re-running + re-verifying the
  relevant notebook chain end to end)
- Does it change a labeled `ASSUMPTION` only? (lower-risk, single-notebook change)
- Does it affect statistical validation (chi-square, PSI, bootstrap CI, calibration)? How?

**Risk of regression**
Per `CONTRIBUTING.md`: a notebook's actual computed output must never change as a side effect of
an unrelated change. If this proposal would change output, it needs the full
compile-check → fixture-run → idempotency-check → real-data-verification cycle before merging.
