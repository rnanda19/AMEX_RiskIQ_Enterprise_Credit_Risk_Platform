# Adverse Action / Reason Code Disclosure (Platform-Wide)

Under the US Equal Credit Opportunity Act (ECOA) and the Fair Credit
Reporting Act (FCRA), a real credit issuer that denies an application or
takes a negative action based on a credit-risk model must give the
applicant specific, accurate reasons ("adverse action reasons") -- not
just a score. This document is a real, current inventory of where this
platform actually generates reason codes, verified 2026-09-09
(`git grep -il "reason_code" -- '*/src/*.py'`).

## Where reason-code generation is real and implemented (6 of 14 problems)

| Problem | File | Mechanism |
|---|---|---|
| 1 -- Credit Scoring / PD Prediction | `src/fastapi_service/main.py` | Per-request reason codes returned alongside the PD score |
| 2 -- Risk Tier Classification | `src/risk_tier_service.py` | Reason codes tied to the tier assignment |
| 5 -- Early Payment Default Detection | `src/early_default_service.py` | Reason codes tied to the early-default risk flag |
| 6 -- Dynamic/Behavioral Credit Scoring | `src/dynamic_behavioral_service.py` | Reason codes tied to the behavioral score |
| 7 -- Early Warning System | `src/real_time_alert_service.py` | Reason codes tied to the early-warning alert |
| 9 -- Collections Optimization | `src/collections_scoring_service.py` | Reason codes tied to the collections-priority score |

Problem 1's explainability work (`notebooks/06_explainable_ai.ipynb`) is
also the only place in the platform with real SHAP-based feature
attribution -- the reason codes there trace back to actual SHAP values,
not a hand-picked rule list.

## Where it does not yet exist (8 of 14 problems)

Problems 3, 4, 8, 10, 11, 12, 13, and 14 do not currently generate
reason codes in their scoring services. For the problems among these
that represent a real underwriting or servicing decision that could
plausibly trigger a real adverse-action obligation (in particular
Problem 3 -- Expected Credit Loss, and Problem 4 -- Delinquency
Escalation), this is a real, open gap.

## Honest scope note

This entire platform is a portfolio project trained on the public Kaggle
"AMEX Default Prediction" dataset, not a real credit decisioning system
in production -- no applicant has ever actually received one of these
notices. This document exists so that (a) the reason-code capability that
does exist is documented rather than left to be discovered by reading
source, and (b) the remaining gap is stated honestly rather than implied
to be solved everywhere it structurally should be.
