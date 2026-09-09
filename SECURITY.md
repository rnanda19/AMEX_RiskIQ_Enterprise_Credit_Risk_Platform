# Security Policy

This is a solo-built portfolio project (AMEX RiskIQ Enterprise Credit Risk
Platform). It is not a production banking system and does not process real
customer data -- all data comes from the public Kaggle "AMEX Default
Prediction" competition dataset. That said, responsible disclosure is
welcome and taken seriously.

## Supported Versions

Only the code on the `main` branch is maintained. There are no older
version branches receiving security fixes.

| Version | Supported |
| ------- | --------- |
| `main`  | Yes       |

## Reporting a Vulnerability

If you find a security issue in this repository -- a dependency with a
known CVE, an exposed secret, an authentication or authorization flaw in
one of the FastAPI services, or anything else -- please report it
privately rather than opening a public issue:

- Email: rnanda19@gmail.com
- Or use GitHub's private vulnerability reporting: open the repository's
  **Security** tab -> **Report a vulnerability**.

Please include:
- A description of the issue and its potential impact.
- Steps to reproduce, or a proof of concept if applicable.
- Which problem/service is affected (e.g. `01_Problem1_Credit_Scoring_PD_Prediction`).

You can expect an acknowledgement within a few days. Since this is a
solo-maintained project, fix timelines are best-effort rather than
contractual, but genuine security reports are prioritized over feature
work.

## Scope

In scope: application code, CI/CD workflows, Dockerfiles, and dependency
manifests in this repository.

Out of scope: the underlying Kaggle dataset itself, and any third-party
service (GitHub, PyPI, Docker Hub) this repository merely depends on --
please report those directly to their respective maintainers.

## API Hardening

Every one of the 14 deployed FastAPI services enforces a
60-requests-per-minute rate limit per client IP (`slowapi`) on its
primary scoring/mutating endpoint, returning a real `429` once exceeded.
`/health` and metadata (`*-info`/lookup) endpoints stay unlimited by
design -- they carry no scoring load and are meant to be polled freely
(e.g. by Docker `HEALTHCHECK`). TLS termination is not yet implemented at
the application layer -- see `TLS.md` for the real, current state and
the honest path to closing that gap.

Authentication is not uniform across the platform, by design, and stated
honestly: 13 of the 14 services use a shared `X-API-Key` header (a single
static secret per service, not per-caller identity -- see
`AUTH_HARDENING.md`); Problem 7 (Early Warning System) instead pilots a
real OAuth2 client-credentials + JWT flow (`POST /token`, then
`Authorization: Bearer <token>`), also documented in full in
`AUTH_HARDENING.md` along with its real verification results and stated
limitations.
