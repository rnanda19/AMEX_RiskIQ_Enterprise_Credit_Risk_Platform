# Data

This problem's deployable service (`src/profitability_scoring_lookup_service.py`) serves
per-customer lookups from the real `profitability_scored_profile.parquet` -- Notebook 67's real,
precomputed PD-adjusted profitability score for every real customer (built on Problem 12's real
unified risk score plus an explicitly ASSUMPTION-labeled revenue estimate).

That file is **not committed to this repository** (~38 MB of real per-customer data; same
convention as Problem 12 -- see that problem's `data/README.md`). Run
`68_profitability_modeling_validation_deployment.ipynb` against your own local copy of the
platform folder to regenerate it, then either place it here as
`profitability_scored_profile.parquet` or point `AMEX_P13_PROFILE_PATH` at wherever you keep it.

Competition: https://www.kaggle.com/competitions/amex-default-prediction
