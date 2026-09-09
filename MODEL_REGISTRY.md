# Model Registry (Platform-Wide)

This is a real, current index over every problem's model registry status,
verified directly against the repository (`git ls-files`, `git grep`) on
2026-09-09 -- not projected or assumed.

## Problems with a documented model registry (8 of 14)

Each of these has its own `0N_ProblemN.../models/README.md`, populated
from that problem's real Notebook-09-style model registry (registered
model versions, timestamps, and real holdout metrics):

| Problem | Registry file |
|---|---|
| 1 -- Credit Scoring / PD Prediction | `01_Problem1_Credit_Scoring_PD_Prediction/models/README.md` |
| 2 -- Risk Tier Classification | `02_Problem2_Risk_Tier_Classification/models/README.md` |
| 3 -- Expected Credit Loss (IFRS9/CECL) | `03_Problem3_Expected_Credit_Loss_IFRS9_CECL/models/README.md` |
| 4 -- Delinquency Escalation / Loss Severity | `04_Problem4_Delinquency_Escalation_Loss_Severity/models/README.md` |
| 5 -- Early Payment Default Detection | `05_Problem5_Early_Payment_Default_Detection/models/README.md` |
| 9 -- Collections Optimization | `09_Problem9_Collections_Optimization/models/README.md` |
| 10 -- Credit Line Management | `10_Problem10_Credit_Line_Management/models/README.md` |
| 11 -- Real-Time Portfolio Monitoring | `11_Problem11_Real_Time_Portfolio_Monitoring/models/README.md` |

Trained model binaries themselves are intentionally excluded from the
GitHub package (a 20 MB per-file size-safety policy) -- each registry
README documents how to regenerate them locally against the real Kaggle
data.

## Problem with real model artifacts but no registry doc (1 of 14)

- **Problem 6 -- Dynamic/Behavioral Credit Scoring**: `models/` contains
  real trained artifacts (`dynamic_behavioral_xgboost_w3.joblib`,
  `preprocessing_artifacts.joblib`) but no `README.md` documenting them.
  This is a genuine, open gap -- not yet closed as of this writing.

## Problems using rule-based / lookup scoring, no trained-model registry (5 of 14)

These problems' services are feature-lookup, rule-based, or aggregation
logic rather than a trained ML model with its own artifact, so there is
no model registry to document for them:

- Problem 7 -- Early Warning System
- Problem 8 -- Roll Rate Modeling
- Problem 12 -- 360 Customer Intelligence
- Problem 13 -- Risk-Adjusted Profitability Modeling
- Problem 14 -- Executive Decision Support Dashboard

## What a real, unified registry would still need

Every registry today is a per-problem markdown table, hand-populated from
each problem's own notebook run. There is no cross-platform, queryable
registry (e.g. MLflow's model registry, or a single structured JSON/DB
file) -- `git grep -c mlflow` returns 0 hits in this repository. Moving to
one is tracked in `ROADMAP.md` as a real, not-yet-started item.
