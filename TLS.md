# Transport Security (TLS) -- Platform-Wide

Real, current state, verified 2026-09-09.

## What exists today

Every one of the 14 FastAPI services in this platform runs in its local
development configuration exactly as `uvicorn` starts it by default --
**plain HTTP, no TLS termination inside the application itself.** This is
true of every problem's service; there is no per-problem exception.

## Why that's the correct default here, and what would change it

For a solo portfolio project run locally or in a single container, having
each of 14 independent FastAPI processes manage its own TLS certificate
is unnecessary complexity that adds no real security value in this
context (no traffic ever leaves the host or crosses an untrusted network
as currently deployed). This is a deliberate, honest simplification, not
an oversight left undocumented.

A real production deployment of any of these services would need TLS
termination at one of these layers instead of inside each Python process:

1. **A reverse proxy / ingress** (nginx, Traefik, or a cloud load
   balancer) terminating TLS in front of all 14 services, with
   certificates issued by a real CA (or Let's Encrypt via ACME) and
   auto-renewed.
2. **A service mesh** (e.g. Istio, Linkerd) providing mutual TLS (mTLS)
   between services if they were to call each other internally.
3. **`uvicorn --ssl-keyfile / --ssl-certfile`** directly, as the simplest
   possible fix if a reverse proxy is genuinely not an option -- this is
   the fastest real path to close this specific gap for a demo
   deployment, and does not require re-architecting anything.

## Related, already-real hardening

Rate limiting and authentication (see `SECURITY.md` and the platform's
shared API-key middleware) are separate concerns from TLS and are tracked
independently -- TLS protects data in transit; it does not by itself
authenticate or rate-limit a caller.

This document will be updated the day any of the three options above is
actually implemented and verified (e.g. a real `curl -v https://...`
against a running instance, not just a config file added).
