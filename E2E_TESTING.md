# End-to-End / Integration Testing (Platform-Wide)

Real, current counts, verified 2026-09-09 directly against the repository:

- `git grep -c "^def test_" -- '*.py'` (summed across files): **164 real
  test functions**.
- `git ls-files | grep -E "test_.*\.py$|_test\.py$"`: **21 real test
  files**.
- `git grep -l "TestClient" -- '*.py'`: **14 files** -- one per problem,
  each under that problem's own `tests/` directory (e.g.
  `01_Problem1_Credit_Scoring_PD_Prediction/tests/test_fastapi_service.py`).

## What this platform's tests actually verify

Every one of the 14 `TestClient`-based test files spins up its problem's
real FastAPI app **in-process** (via FastAPI's `TestClient`, backed by
`httpx`) and sends real HTTP requests to its real endpoints -- `/health`,
the scoring endpoint, and (where implemented) the reason-code path --
asserting on real status codes and real response payload shapes. This is
genuine service-level integration testing, not a mock of the framework.

Additionally, `shared/tests/` covers the shared library
(`shared/config.py`, `shared/metrics.py`, `shared/monitoring.py`,
`shared/tiers.py`) directly.

## What is honestly still missing

**A true cross-service, end-to-end test does not exist.** Every test
today exercises exactly one service in isolation. There is no test that,
for example, takes one synthetic applicant through Problem 1 (PD
scoring) -> Problem 2 (risk tier) -> Problem 9 (collections
prioritization) as a single simulated customer journey across multiple
live services. Building that would require either:

1. Running several of the 14 FastAPI services together (e.g. via
   `docker compose`) and driving them with a real HTTP client script, or
2. A lighter-weight in-process version that imports each service's
   FastAPI app and chains `TestClient` calls, passing one service's real
   output into the next service's real input.

Neither exists yet. This is tracked as a real, open item -- not
described here as done when it isn't.
