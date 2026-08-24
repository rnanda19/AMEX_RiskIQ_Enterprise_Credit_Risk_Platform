# Models

Problem 2 (Risk Tier Classification) does **not** train a new model -- it reuses Problem 1's real, saved champion model (**xgboost**, holdout AUC 0.9620396555226549, holdout AMEX metric 0.7935631597243085) as-is, and adds a policy-based tier classification layer on top of its real predicted PD scores. See `docs/risk_tier_policy.json` for the real, saved bucketing policy (business-rule thresholds and quantile cutpoints) this layer applies -- that policy file, not a retrained model binary, is Problem 2's own core artifact.
