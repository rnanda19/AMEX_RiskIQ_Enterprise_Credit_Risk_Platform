# Model Card — Credit Scoring / Probability-of-Default (PD) Prediction

## Model details

- **Champion model (measured):** XGBoost, selected by holdout AMEX metric
  from a 6-model benchmark set (Logistic Regression, Random Forest, Extra
  Trees, HistGradientBoosting, XGBoost, LightGBM — CatBoost included when
  installed).
- **Champion holdout AUC (measured):** 0.9620396555226549
- **Champion holdout AMEX metric (measured):** 0.7935631597243085
- **Random seed:** 42 (fixed platform-wide, every notebook)
- **Trained by:** `05_model_development.ipynb`, Notebook 5 of 18
- **Metric definition:** `shared/metrics.py::amex_metric_numpy` — the
  official competition metric, 0.5 × Normalized Weighted Gini + 0.5 ×
  Top-4% Capture Rate, non-defaulters weighted 20× relative to defaulters
  in both halves.

## Intended use

Score the probability that a credit card customer defaults, using real
transaction and statement history, so a credit-risk team can price,
provision, and manage portfolio risk proactively. Served in real time via
the FastAPI service in `src/fastapi_service/main.py` (see `/model-info` for
the live values above, `/predict` for scoring).

## Training data

- **Source:** Kaggle — American Express Default Prediction competition.
  Raw CSVs are not redistributed in this repository (see `data/README.md`).
- **Training customers aggregated (measured):** 458,913
- **Test customers aggregated (measured):** 924,621
- **Live default rate, join-validated (measured):** 25.89%

## Evaluation

Stratified 5-fold cross-validation within the train split (Section 7 of
Notebook 05), then a full-train fit evaluated on a held-out, never-trained-on
split (Section 8) — the AUC and AMEX metric above are the holdout numbers,
not the CV numbers, since the holdout is the unbiased estimate.

## Limitations

- The model is trained and evaluated on Kaggle's anonymized/aggregated
  feature set — feature names are not economically interpretable 1:1 (see
  `06_explainable_ai.ipynb` for SHAP-based interpretation of what the
  anonymized features are doing).
- No demographic/protected-attribute data exists in this dataset, so
  fairness auditing (`07_model_risk_management.ipynb`) is necessarily
  proxy-based, not attribute-based — documented explicitly in that
  notebook's own report rather than overstated here.
- Basel III / IFRS9 figures derived from this model's scores
  (`08_basel_ifrs9_mapping.ipynb`) use explicit, labeled `ASSUMPTION`
  values for anything the dataset has no ground truth for (e.g. LGD
  outside what Problem 4 computed, macro scenario weights) — see that
  notebook's own assumption log, not restated here to avoid the two
  drifting apart.

## How this model is tested going forward

`Problem1_Credit_Scoring_PD_Prediction/tests/` covers the *serving* path
(the FastAPI app: health, model-info, prediction shape/range, missing-value
imputation, unseen-category handling) against a small, genuinely-fit
synthetic model — it does not re-run the real training pipeline. Re-running
`05_model_development.ipynb` itself against the real dataset remains the
only source of truth for the numbers on this card; CI does not (and
cannot, without the multi-GB real data) reproduce them.
