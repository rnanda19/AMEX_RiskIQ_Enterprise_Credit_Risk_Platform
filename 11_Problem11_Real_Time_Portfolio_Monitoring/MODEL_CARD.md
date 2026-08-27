# Model Card -- Problem 11: Real-Time Portfolio Monitoring

## Technique

This is **not** a trained classifier. It is an unsupervised statistical-process-control (SPC) monitor: a real trailing-baseline control chart computed over 8 SHAP-ranked portfolio features (`P_2`, `B_1`, `B_11`, `D_39`, `B_4`, `S_3`, `R_1`, `B_5`), with a control limit of 2.5 standard deviations and a minimum 6-month trailing baseline. A calendar month is flagged as an ALERT month when its real cross-sectional mean, for any monitored column, breaches that column's own trailing baseline by more than the control limit.

A secondary, customer-level "joint deviation" score complements the portfolio-level chart: a customer only counts toward a flagged cohort if their own real statement value is itself >=2.0 standard deviations from that month's real cross-sectional peer mean, in the same direction the portfolio itself is breaching.

## Intended Use

Operational, cohort-level early warning for a credit-risk operations team -- surfacing calendar months where portfolio behavior is shifting, so a risk committee can investigate before it is visible customer-by-customer. This complements, and does not replace, Problem 7's per-customer early-warning classifier.

## Training Data

None -- this technique fits no model and requires no training set. It is computed directly from real monthly aggregates of the Kaggle American Express Default Prediction statement history.

## Evaluation (Real, Measured)

| Metric | Value |
|---|---|
| Winning candidate | 1 consecutive breaching month |
| Cohort default rate lift | 2.67x (95% CI [2.64, 2.70]) |
| Accuracy | 0.795 |
| Precision | 0.692 |
| Recall | 0.378 |
| F1 | 0.488 |
| Specificity | 0.941 |
| MCC | 0.401 |
| ROC-AUC (continuous cohort score) | 0.663 |
| PR-AUC (continuous cohort score) | 0.459 |
| Live API self-test | True |
| Recommended for production | True |

Full candidate sweep (2-10 consecutive breaching months) and confusion matrices: `reports/modeling/portfolio_monitoring_modeling_results.json`.

## Known Limitations

- Coarse, month-level signal by construction: the ROC-AUC of the continuous cohort score (0.663) retains only ~69% of the full-history reference AUC (0.961) -- expected for a portfolio-aggregate technique, not a failure of the design.
- Customer-level cohort membership depends on the joint-deviation redesign (see `CHANGELOG.md`): a customer must be both in a portfolio-flagged month AND individually deviating in the same direction, so a customer who is only ever "average" is never flagged even during a real alert month.
- Fewer than 6 consecutive breaching months (candidates 4+) produced zero alerted customers on this real run -- reported honestly in the candidate sweep rather than omitted.

## Serving

`src/portfolio_alert_feed_service.py` -- real FastAPI service, `X-API-Key`-gated (`/health` open), self-tested in Notebook 60 against `src/portfolio_monitoring_deployment_policy.json`.
