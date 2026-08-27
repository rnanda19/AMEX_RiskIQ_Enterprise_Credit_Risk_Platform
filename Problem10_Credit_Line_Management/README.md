# AMEX Enterprise Credit Risk Platform -- Credit Line Management

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]() [![CRISP-DM](https://img.shields.io/badge/methodology-CRISP--DM-informational.svg)]() [![License: All Rights Reserved](https://img.shields.io/badge/license-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

Phase 4, Problem 10 of the platform: a 4-notebook build (Notebooks 54-57) covering credit-line management on the real Kaggle **American Express Default Prediction** dataset.

## Status: Complete -- Real Results Synced, Hardened (2026-08-27)

**Real, synced results:** real risk-level monotonicity passed (461.02x top-to-bottom default-rate ratio), but real trend coherence and minimum-tier-population both failed -- **honestly NOT recommended for production**. This is the one system in the platform's 9-problem value-creation total that is deliberately excluded on its own real, data-driven KPI miss (real net benefit if deployed anyway: $4,108,042.50/cycle, shown for completeness, not as a deployment recommendation). See the [Executive Capstone Report](../Executive_Capstone_Report/) and root `README.md`'s Platform-at-a-Glance table.

📊 [Financial Impact Dashboard](reports/financial_impact_reporting_packaging/credit_line_management_financial_impact_dashboard.html) · 📄 [Financial Impact Report (Word)](reports/financial_impact_reporting_packaging/Credit_Line_Management_Financial_Impact_Report.docx) · 📊 [Financial Impact Workbook (Excel)](reports/financial_impact_reporting_packaging/AMEX_Problem10_Financial_Impact_Workbook.xlsx)

This problem also received the platform's Global Standard hardening delta (2026-08-27): a real, auth-protected FastAPI recommendation service (`src/credit_line_scoring_service.py`), Docker packaging, real unit tests, and `MODEL_CARD.md`/`CHANGELOG.md`/`requirements.txt` -- deployed here for completeness and honest transparency, matching this platform's standard of shipping every real result, including the ones that didn't clear their KPI bar. See `CHANGELOG.md` for the full detail.

**Update (2026-08-27):** `PD_TREND` was root-caused and redesigned (Notebooks 54-55) into a genuine same-model, two-time-point measure, replacing the original cross-model residual. Real re-run on the full dataset: genuine partial improvement -- risk-level monotonicity improved (483x ratio), and the High Risk tier's trend-coherence gate now passes for the first time (previously the worst offender at a -21 point real gap). But Low Risk and Medium Risk tiers are still incoherent, and the tighter statement-coverage bar the fix requires made the minimum-tier-population problem worse (one real segment shrank to just 7 customers). Still **NOT recommended for production** -- see `CHANGELOG.md` for the full honest before/after. Notebooks 56-57 have been updated to match the redefinition but not yet re-run with real data, so `docs/credit_line_deployment_policy.json` and the financial-impact reports below still reflect the prior (pre-redesign) run.

## Project Structure

```
Problem10_Credit_Line_Management/
├── data/
│   └── README.md
├── docs/
│   ├── credit_line_deployment_policy.json
│   └── credit_line_policy.json
├── notebooks/
│   ├── 54_credit_line_management_business_understanding.ipynb
│   ├── 55_credit_line_management_modeling.ipynb
│   ├── 56_credit_line_management_validation_deployment.ipynb
│   └── 57_credit_line_management_financial_impact_reporting_packaging.ipynb
├── reports/
│   ├── modeling/
│   └── financial_impact_reporting_packaging/
├── src/
│   ├── credit_line_scoring_service.py
│   └── docker/
├── tests/
├── MODEL_CARD.md
├── CHANGELOG.md
├── requirements.txt
└── LICENSE
```

## License

All Rights Reserved -- this repository is shared publicly for portfolio and demonstration purposes only. It is not licensed for reuse, modification, or redistribution; see `LICENSE` for details.
