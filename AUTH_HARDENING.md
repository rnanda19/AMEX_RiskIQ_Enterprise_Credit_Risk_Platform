# Authentication Hardening -- Platform-Wide

Real, current state, verified 2026-09-09 (`grep -rln require_api_key
--include="*.py"`).

## What exists today

All 14 deployed FastAPI services use the same pattern: a single, shared
static secret compared against an `X-API-Key` request header.

```python
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(presented: str = Security(_api_key_header)) -> str:
    if not presented or not secrets.compare_digest(presented, API_KEY):
        raise HTTPException(status_code=401, detail="Missing or invalid X-API-Key header.")
    return presented
```

A few honest details worth stating plainly, not glossed over:

- The comparison uses `secrets.compare_digest`, so it is at least
  constant-time (no timing-attack side channel) -- that part is done
  correctly.
- The key itself is one static string per service (`API_KEY`, read from
  an environment variable -- see each service's `.env.example`), shared
  by every caller. There is no per-caller identity: a valid request only
  proves "holds the shared secret," not "is customer/system X."
- There is no expiry, no rotation mechanism, and no scoping (every caller
  that has the key can call every protected endpoint on that service --
  there are no read-only vs. write-capable keys).
- Revoking access today means changing the environment variable and
  restarting the service, which invalidates the key for every caller at
  once, not just the one being revoked.

This is a real, working control -- it stops an anonymous, keyless caller
cold, and is the correct minimum bar for a solo portfolio project's
demo services. It is not, and is not being represented as, an
enterprise-grade identity system.

## Why OAuth2/JWT is not implemented yet, stated honestly

Replacing shared-API-key auth with real OAuth2 (e.g. the
`OAuth2PasswordBearer`/`OAuth2ClientCredentials` flows FastAPI ships
support for) plus signed JWTs is a materially larger change than the
rate-limiting rollout in this same changelog entry, for three concrete
reasons:

1. **It needs an issuer.** Shared-key auth needs nothing but the key
   itself; JWT auth needs something to actually issue and sign tokens --
   at minimum a `/token` endpoint per service (or one shared auth
   service all 14 trust), a signing key, and a chosen algorithm (HS256
   with a shared secret is the simplest real option that needs no new
   infrastructure; RS256 with a real key pair is the stronger, more
   "real OAuth2" option but needs key management this platform doesn't
   have yet).
2. **It touches all 14 services' request path**, not just their
   dependency list -- every `dependencies=[Depends(require_api_key)]`
   call site (`grep` count: 14 files, 1-2 protected endpoints each)
   would need to change to a token-decoding dependency, and every
   existing test that currently sends `X-API-Key` (all 172 real tests
   that exercise a protected endpoint) would need to instead mint or
   stub a real signed token. That is a real regression-risk surface
   across the entire platform, not a contained, low-risk change.
3. **No user sign-off yet for a live pilot this session.** Consistent
   with this platform's standing practice of piloting risky, cross-
   cutting changes on one service first (see the rate-limiting and
   Prometheus entries in `CHANGELOG.md`), a real OAuth2/JWT pilot would
   itself be a reasonable next step -- but doing it silently, without
   the person driving this hardening work agreeing on which flow
   (password, client-credentials) and which algorithm (HS256 vs. RS256)
   to commit to, risks building the wrong thing twice.

## A concrete, scoped migration plan (not yet started)

If and when this is picked up, the lowest-risk real path is:

1. **Pilot on Problem 7** (same service already piloting rate limiting
   and Prometheus, so its `.env.example`, tests, and docs are already
   the most current in the platform): add a `python-jose[cryptography]`
   or `PyJWT` dependency, a `/token` endpoint implementing the OAuth2
   **client-credentials** flow (this is a service-to-service scoring
   API, not a human login form, so client-credentials is the correct
   grant type -- not password or authorization-code), issuing a
   short-lived (e.g. 15-minute) HS256-signed JWT against the same
   `API_KEY`-style shared secret used today (so no new infrastructure is
   needed for the pilot).
2. Change `require_api_key`'s dependency to decode and validate that JWT
   (signature, expiry, and an `aud`/`scope` claim identifying it as
   valid for this service) instead of comparing a static string.
3. Update Problem 7's tests to mint a real token via the new `/token`
   endpoint in a fixture, then use it exactly like today's
   `X-API-Key` header is used, and re-run its 10-test suite plus the
   full 172-test platform suite to confirm no regression, the same
   verification bar every other change in this changelog has met.
4. Document the pilot's real, verified scope in this file (which
   service, which grant type, which algorithm, which tests changed) --
   the same honest-scope pattern `MONITORING.md` and `LOAD_TESTING.md`
   already follow -- before considering rolling it out to the other 13
   services.

This document will be updated the day any part of that plan is actually
implemented and verified -- not before.
