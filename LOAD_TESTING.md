# Load / Performance Testing (Platform-Wide)

Real, current state, verified 2026-09-09: `git grep -c "locust\|k6 "`
returns **0 hits** anywhere in this repository. No load or performance
test of any kind has been run against any of the 14 FastAPI services.
This document exists to state that gap honestly rather than leave it
undiscovered, and to lay out the concrete, low-cost path to closing it.

## What load testing would need to answer here

For a portfolio project, the real question worth answering is not
"can this survive real production traffic" (it was never built or
deployed for that) but a narrower, honestly useful one: **given this
platform's actual, current architecture (synchronous FastAPI + `joblib`-
loaded scikit-learn/XGBoost models, no async model inference, no
connection pooling beyond framework defaults), what is its real
single-instance throughput and p50/p95/p99 latency under load, and where
does it fall over first?**

## The concrete plan (not yet executed)

1. **Tool: Locust** (pure Python, matches this platform's stack, no JVM
   dependency the way k6 would add). Install with
   `pip install locust`.
2. **Target: Problem 1's FastAPI service** first (it is the most mature
   and already has real reason-code + SHAP-based scoring, so it is the
   most realistic load-bearing endpoint to test) -- run it locally
   (`uvicorn ... `), then point a Locust locustfile at its real scoring
   endpoint with a realistic payload shape drawn from the actual test
   fixtures already in `01_Problem1_Credit_Scoring_PD_Prediction/tests/`.
3. **Report real numbers, not projections**: requests/sec at increasing
   concurrent-user counts, and the actual point (if any, within a
   reasonable ceiling such as 200 concurrent users on a single container)
   where p95 latency degrades past a stated threshold or the process
   starts erroring.
4. **Extend to the remaining 13 services** only after the Problem 1
   pilot's methodology and locustfile pattern are validated, to avoid
   writing 14 slightly-different, unverified load scripts up front.

None of the above has been run as of this writing. When it is, this
document will be replaced with the real numbers and the exact Locust
command used to produce them -- never with an estimate.
