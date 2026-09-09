# Authentication Hardening -- Platform-Wide

Real, current state, verified 2026-09-09 (`grep -rln require_api_key
--include="*.py"` for the 13 unchanged services; the OAuth2/JWT pilot
below verified via a real running server, not just unit tests).

## What exists today: two different patterns, by design

**13 of the 14 deployed FastAPI services** (all except Problem 7) still
use the platform's original pattern: a single, shared static secret
compared against an `X-API-Key` request header.

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

This remains a real, working control for those 13 services -- it stops
an anonymous, keyless caller cold, and is the correct minimum bar for a
solo portfolio project's demo services. It is not, and is not being
represented as, an enterprise-grade identity system.

**Problem 7 (Early Warning System) is the one exception**, piloting a
real OAuth2 client-credentials + JWT flow instead -- see below.

## The Problem 7 OAuth2/JWT pilot, implemented and verified 2026-09-09

`07_Problem7_Early_Warning_System/src/real_time_alert_service.py` now
implements a real OAuth2 **client-credentials** grant (this is a
service-to-service scoring API, not a human login form, so
client-credentials is the correct grant type, not password or
authorization-code):

1. `POST /token` with form fields `grant_type=client_credentials`,
   `client_id=ews-service-client`, `client_secret=<the API_KEY value>`
   returns a real, signed JSON Web Token: `{"access_token": "...",
   "token_type": "bearer", "expires_in": 900}`.
2. The token is a genuine HS256-signed JWT (via `PyJWT==2.3.0`) with real
   claims -- `iss`, `sub`, `aud`, `scope`, `iat`, `exp` (15-minute
   expiry) -- not a static string dressed up to look like one.
3. `/score` and `/model-info` now require `Authorization: Bearer
   <token>` instead of `X-API-Key`, validated by `require_bearer_token`:
   signature verified against the shared secret, `aud`/`iss` checked,
   expiry checked, and the `scope` claim must equal `"score"`.
4. `/health`, `/metrics`, and `/token` itself stay unauthenticated (the
   last one is how a caller gets a token in the first place).

**Verified two ways, not just asserted:**

- Problem 7's test suite grew from 10 to 18 tests, all real and all
  passing: issuing a real token via the actual `/token` endpoint (not a
  hand-fabricated one) and decoding it to check its claims; rejecting a
  wrong `client_secret`, an unknown `client_id`, and an unsupported
  `grant_type`; rejecting a missing token, an invalid token, a genuinely
  expired token (a real JWT signed with an `exp` in the past), and a
  token with the wrong `scope`; and -- the real regression check that
  matters most -- confirming the **old `X-API-Key` header alone no
  longer authenticates `/model-info`**, proving this replaced the old
  control rather than merely adding a second option beside it. The full
  180-test platform suite (172 pre-existing + 8 new) passes.
- Live end-to-end against a real running `uvicorn` instance: `X-API-Key`
  alone against `/model-info` -> real `401`; `POST /token` with the
  correct client credentials -> a real signed JWT; that token against
  `/model-info` -> real `200`; that token against `/score` with a real
  payload -> a real `200` with real computed scoring output; `POST
  /token` with a wrong `client_secret` -> real `401`.

**Real, stated simplifications of this pilot, not hidden:**

- There is a single hardcoded registered client (`ews-service-client`) --
  no client registry or database. A real multi-client rollout would need
  one.
- The same shared secret (`API_KEY`) is reused as both that client's
  credential *and* the JWT's HS256 signing key. A real production setup
  would keep those separate (and likely move to RS256 with a real key
  pair, so the service verifying tokens doesn't need to hold the same
  secret used to issue them). This pilot deliberately reused the one
  secret specifically to avoid standing up new infrastructure just to
  prove the pattern.
- `/token` itself is not rate-limited or otherwise brute-force-protected
  in this pilot -- a real deployment would want that (this platform
  already has a real rate-limiting implementation on `/score`; extending
  it to `/token` is a small, real follow-on, not attempted here to avoid
  the same kind of test-interaction risk already seen and deliberately
  avoided on Problem 11's `/reset`/`/alert-feed` endpoints -- see
  `CHANGELOG.md`).
- No token revocation exists (nor did key revocation before this pilot) -
  a compromised token remains valid until its 15-minute expiry.

## Path to platform-wide rollout (not yet started)

Now that the pattern is real and verified on one service, extending it
to the other 13 is a mechanical repeat of the same steps applied here:
add the `PyJWT` dependency, add the same `/token` endpoint and
`require_bearer_token` dependency, swap the `Depends(require_api_key)`
call sites, and rewrite each service's tests the same way Problem 7's
were rewritten (mint a real token via `/token` in place of the static
`X-API-Key` header). That is a real, contained, well-understood change
now -- it was a genuinely open design question before this pilot existed
to prove the pattern out. It has not been done for the other 13 services
in this pass; each would need its own dedicated test run and live
verification before being called done, the same bar this document holds
itself to.
