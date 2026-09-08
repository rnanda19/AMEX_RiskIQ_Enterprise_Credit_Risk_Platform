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
