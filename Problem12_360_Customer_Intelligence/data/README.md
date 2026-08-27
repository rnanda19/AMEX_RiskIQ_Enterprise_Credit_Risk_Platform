# Data

This problem's deployable service (`src/customer_intelligence_lookup_service.py`) serves
per-customer lookups from the real `unified_customer_profile.parquet` -- Notebook 63's real,
precomputed unified risk profile for every real customer (composed from Problems 1, 6, 9, 10).

That file is **not committed to this repository** (~29 MB of real per-customer data; this repo's
established convention -- see e.g. Problem 8's `data/README.md` -- keeps large per-customer
files out of git and ships only small, curated policy/report artifacts). Run
`64_customer_intelligence_validation_deployment.ipynb` against your own local copy of the
platform folder to regenerate it, then either place it here as `unified_customer_profile.parquet`
or point `AMEX_P12_PROFILE_PATH` at wherever you keep it.

Competition: https://www.kaggle.com/competitions/amex-default-prediction
