# Model Card -- Executive Decision Support Dashboard

## Model details

- **Technique:** a real, provable partition-completeness aggregation layer over all 13 prior
  problems -- not a model. Every problem is accounted for exactly once as included (real
  value-creation), foundational (no standalone dollar figure by design), reserve-optimization
  (tracked separately), or excluded (a real KPI miss), enforced by code on every run.
- **Random seed:** 42 (fixed platform-wide).
- **Built by:** `71_executive_dashboard_modeling.ipynb`, validated by
  `72_executive_dashboard_validation_deployment.ipynb`, packaged by
  `73_executive_dashboard_financial_impact_reporting_packaging.ipynb`.
- **Frozen policy:** the real included/excluded problem lists and total platform net value are
  frozen in `docs/executive_dashboard_deployment_policy.json`; the full real per-problem rollup is
  in `reports/modeling/executive_dashboard_data.json` (both shipped self-contained in `src/`).

## Intended use

Serve the real, precomputed executive rollup of the whole platform for a CRO-level dashboard or
API consumer -- total platform net value, per-problem status, and the honest inclusion/exclusion
reasoning behind that total.

## Evaluation (real, measured)

- Aggregation completeness (reproduced): all 13 prior problems accounted for exactly once --
  **PASSED**.
- Aggregation scope correctness (reproduced): foundational (Problems 1, 2) and reserve
  optimization (Problem 3) never summed into the value-creation total; Problem 10 excluded for its
  real KPI miss -- **PASSED**.
- Population consistency (reproduced): **PASSED**.
- Total platform net value (real): $429,926,252.73/cycle, from 9 production-recommended systems.
- **Deployment status: RECOMMENDED FOR PRODUCTION** -- both real hard-gate KPIs passed.

## Limitations

- This layer is only as honest as its 13 upstream inputs -- it re-verifies completeness and scope,
  not each upstream problem's own modeling quality (that is each problem's own MODEL_CARD.md).
- The total is a per-cycle figure across value-creation problems with heterogeneous real cycle
  definitions (some daily, some monthly); see each included problem's own report for its cycle
  definition.

## How this is tested going forward

`tests/` drives the real deployed FastAPI dashboard service end-to-end via `TestClient` against
the real, measured `executive_dashboard_data.json` and `executive_dashboard_deployment_policy.json`
shipped in `src/` -- covering `/health`, `/executive-summary` (asserting the real total platform
net value and included/excluded lists), the auth gate, a known-problem lookup, and the 404 path
for an out-of-range problem number.

## Deployment

`src/executive_dashboard_service.py` defaults `AMEX_P14_POLICY_PATH` / `AMEX_P14_DATA_PATH` to the
real frozen policy JSON and real dashboard data shipped alongside it in `src/` (self-contained --
no local machine path needed; a hardcoded personal Windows path was found and fixed here during
this hardening pass, the same class of bug already fixed for Problems 5-13 -- see
`CHANGELOG.md`). Run locally with `uvicorn executive_dashboard_service:app --port 8014` from
`src/`, or build the container:

```bash
cd src/docker
docker compose up --build
```
