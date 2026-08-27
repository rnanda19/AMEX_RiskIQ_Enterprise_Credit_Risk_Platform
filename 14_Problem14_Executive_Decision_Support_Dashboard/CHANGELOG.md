# Changelog -- Problem 14: Executive Decision Support Dashboard

## 2026-08-27 -- Global Standard hardening pass (delta, Problems 9-14)

- **Real bug found and fixed:** `executive_dashboard_service.py`'s `POLICY_PATH`/`DATA_PATH`
  defaults hardcoded the author's real local Windows paths -- same bug class already found and
  fixed for Problems 5-13's services; fixed to default to the real policy JSON and real dashboard
  data now shipped alongside it in `src/`. `.env.example`'s example values had the same leak --
  replaced with generic placeholders.
- Added `tests/` (pytest): the real FastAPI dashboard service driven end-to-end via `TestClient`
  against the real, measured dashboard data and deployment policy.
- Added `src/docker/` (Dockerfile, docker-compose.yml, .dockerignore).
- Synced this problem's real `reports/validation_deployment/`-equivalent artifacts (deployment
  policy, dashboard data, aggregation table) from the author's machine into the repository for the
  first time.
- Wired into the platform's root `ci.yml`, `code-quality.yml`, and `Makefile`.

