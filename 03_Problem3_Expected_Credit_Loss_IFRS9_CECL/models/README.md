# Models

This problem has no trained ML model of its own -- `src/ecl_calculator.py` is a deterministic calculation engine that combines Problem 1's real trained PD model and Problem 4's real trained severity model through a frozen, rule-based formula (see `reports/validation_deployment/ecl_scoring_bundle.json` for the exact frozen parameters, and each of those problems' own `models/` folder for their trained artifacts).
