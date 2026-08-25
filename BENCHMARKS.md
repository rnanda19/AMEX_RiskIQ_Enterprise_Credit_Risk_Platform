# Benchmarks & Comparisons

Every number below was computed by that problem's own notebooks against the real Kaggle
American Express Default Prediction dataset -- not projected or estimated. This file
consolidates comparisons that already exist scattered across each problem's own
`reports/`/`MODEL_CARD.md`, in one place, for anyone auditing the platform's actual measured
lift over a naive baseline. See each problem's own `MODEL_CARD.md` for full methodology.

## Problem 1 -- Probability of Default: model tournament vs. champion

Champion selected from a real 6-model benchmark tournament (Logistic Regression, Random Forest,
Extra Trees, HistGradientBoosting, XGBoost, LightGBM) on identical `StratifiedKFold(5, seed=42)`
folds. XGBoost won on the real holdout AMEX metric.

| Metric | Value |
|---|---|
| Champion (XGBoost) holdout AUC | 0.9620396555226549 |
| Champion holdout AMEX metric | 0.7936 |
| Training / test customers aggregated | 458,913 / 924,621 |
| Live observed default rate | 25.89% |

## Problem 2 -- Risk Tier Classification: tier separation vs. no tiering

| Metric | Value |
|---|---|
| Risk tiers defined | 4 |
| Chi-square (tier vs. actual default) | p ≈ 0.0 |
| Cramér's V | 0.7636626665627394 |

## Problem 3 -- Expected Credit Loss: IFRS9 / CECL vs. flat-LGD baseline

Real holdout: 91,783 customers.

| Approach | Total ECL (USD) |
|---|---|
| Flat-LGD baseline (Problem 1's Notebook 08, no staging, no tiered LGD) | $67,830,905.87 |
| IFRS9-staged (real, outcome-free staging rubric) | $72,448,498.95 |
| CECL (lifetime, real) | $73,051,922.57 |

The flat baseline under-provisions by **~$4.6M (IFRS9)** / **~$5.2M (CECL)** relative to a
tiered, staged approach on this real holdout -- the gap this problem exists to close.
Chi-square (stage vs. actual default): p = 0.0, Cramér's V 0.7289977841059684.

## Problem 4 -- Loss Severity: tiered LGD vs. flat-LGD baseline

Real holdout: 91,783 customers, 243 real engineered features.

| Approach | Total modeled loss (USD) |
|---|---|
| Flat 45% LGD baseline | $53,473,500.00 |
| 3-tier severity-differentiated LGD (real, 0.3015 / 0.45 / 0.648) | $72,908,932.50 |

Delta: **+$19,435,432.50** -- the flat baseline understates loss by this amount on the real
holdout. Severe-tier customers default at **48.66x** the rate of Low-tier customers (chi-square
p = 0.0, Cramér's V 0.6416) -- not a modeling artifact, a real, large separation.

## Problem 5 -- Early Payment Default: early-window AUC retention vs. full history

| Early window (K statements) | Holdout AUC | % of full-history AUC retained |
|---|---|---|
| Full history (Problem 1's champion) | 0.9620396555226549 | 100% (reference) |
| K=3 (winning candidate, real) | 0.9265274920113401 | 96.31% |

95% bootstrap CI (2,000 resamples): [0.9247892198513004, 0.9281912251702001] -- entirely above
chance. Mean calibration gap 0.00258, split-half score PSI 0.000446 (both well under target).
**Recommended for production.**

## Problem 6 -- Dynamic/Behavioral Credit Scoring: trailing-window AUC retention vs. full history

| Window | Holdout AUC (reproduced) | % of full-history AUC retained |
|---|---|---|
| Full history (Problem 1's champion) | 0.9620396555226549 | 100% (reference) |
| W=3 trailing (winning candidate, real) | 0.9541 | 99.2% |

95% bootstrap CI lower bound: 0.9528. Mean calibration gap 0.0037, split-half score PSI 0.0003
(both well under target). A recency signal, refreshed monthly, complementary to Problem 1's
full-history champion. **Recommended for production.**

## Problem 7 -- Early Warning System: z-score deviation lift vs. base default rate

| Candidate (min. deviation count) | Default rate among alerted | Lift vs. base holdout rate |
|---|---|---|
| Base holdout default rate | 25.62% | 1.00x (reference) |
| Winning candidate = 8 (real, reproduced) | 36.06% | 1.41x |

AUC retention vs. Problem 1's full-history champion: 68.68%. **No candidate met the KPI target
on this run -- honestly NOT recommended for production**, reported as such rather than rounded
up. Real Net Benefit/Cycle if deployed anyway: $4,224,135 (shown for completeness, not as a
deployment recommendation).

## Problem 8 -- Roll-Rate Modeling: severity-tier default-rate separation

| State | Real default rate | Real population share |
|---|---|---|
| Low Severity | 0.57% | 31.7% |
| Moderate Severity | 9.16% | 31.0% |
| Severe | 61.24% | 37.4% |

Severe/Low default-rate ratio: **107.21x** (95% CI lower bound 92.78x). Transition coherence gap
P(Severe→Severe) − P(Low→Severe): 0.9557 (95% CI lower bound 0.9550). Both hard-gate KPIs
(monotonicity, coherence) met on this run; cross-validated against Problem 6's independently
trained dynamic PD (z=8.80, p<0.001). **Recommended for production.**

## Reading this table honestly

These are the platform's own real, measured numbers -- not benchmarked against any external
published model on this dataset (this is a portfolio project, not a leaderboard submission).
"Benchmark" here means each problem's own baseline-vs-improvement comparison, computed on the
same real holdout population, not a claim of state-of-the-art against outside work.
