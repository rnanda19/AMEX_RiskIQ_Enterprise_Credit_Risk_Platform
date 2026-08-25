---
name: Bug report
about: Something in a notebook, service, or test doesn't behave as documented
title: "[BUG] "
labels: bug
---

**Which problem / notebook / service is affected?**
e.g. `Problem5_Early_Payment_Default_Detection/src/early_default_service.py`, or `Notebook 36`.

**What happened**
A clear description of the actual behavior, including the full error/traceback if there is one.

**What you expected**
What the documented/README behavior said should happen instead.

**Steps to reproduce**
1. ...
2. ...

**Environment**
- OS:
- Python version:
- Was this run against the real Kaggle dataset, or a fixture/test?

**Real vs. fabricated data note**
This project's standing rule is zero-fabrication — every number in a notebook's output is
computed live by that run, never hardcoded. If this bug involves a suspicious number (one that
looks copied, rounded, or inconsistent with a labeled `ASSUMPTION`), please say so explicitly —
that's treated as a higher-severity class of bug here.
