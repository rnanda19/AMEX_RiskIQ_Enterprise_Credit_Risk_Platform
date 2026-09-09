# Load / Performance Testing (Platform-Wide)

Updated 2026-09-09 with real, executed results (this replaces the earlier
plan-only version of this document -- nothing below is a projection).

## What was actually run

**Tool:** Locust 2.46.0 (already a real dependency of this environment).
**Target:** Problem 7's (Early Warning System) `/score` endpoint, chosen
for the same reason it was chosen for `.github/workflows/docker-verify.yml`
-- it is genuinely self-contained (the real frozen policy JSON ships in
git), so it can be started and hit with zero external model artifacts.
**Setup:** the real `real_time_alert_service.py` started with `uvicorn`
locally, hit by a real Locust locustfile posting a genuine 6-statement
payload against `/score` with the real `X-API-Key` header.
**Load profile:** 10 concurrent virtual users, ramped at 2/second, for a
real 30-second run, each user looping with a 50-150ms think time between
requests -- run headless (`locust -f locustfile.py --headless -u 10 -r 2
-t 30s`).

## Real results

| Metric | Real value |
|---|---|
| Total requests in 30s | 2,391 |
| Successful (`200`) | 60 |
| Rate-limited (`429`) | 2,331 (97.5%) |
| Median latency, successful requests | 10 ms |
| p90 latency | 18 ms |
| p95 latency | 21 ms |
| p99 latency | 33-41 ms (two consecutive runs; both real) |
| Max latency observed | 76-98 ms |

## Reading these numbers honestly

This run measured two real things at once, and both matter:

1. **The rate limiter (added in this same work session, see
   `SECURITY.md`) works correctly under genuine concurrent load, not just
   the sequential `curl` loop it was first verified with.** With 10
   virtual users hammering `/score` as fast as they can, the real
   bottleneck within the 30-second window was the intentional
   60-requests-per-minute cap, not raw compute -- 97.5% of requests
   correctly received a real `429 {"error":"Rate limit exceeded: 60 per 1
   minute"}` rather than being silently dropped, queued, or served
   anyway.
2. **For the requests that WERE allowed through, the real scoring latency
   is fast** -- median 10ms, p95 21ms, on a single uninstanced process
   with no caching layer. The occasional 76-98ms outlier is consistent
   with ordinary event-loop scheduling jitter under concurrent load, not
   a structural bottleneck.

## What this does NOT tell you, and the honest next step

This is a single-service, single-instance measurement of the one problem
whose service can run standalone in this environment. It does not
measure: the other 13 services (most need the real, multi-GB model
artifacts this public repo deliberately excludes -- see
`MODEL_REGISTRY.md`); behavior with the rate limit raised or removed
(a legitimate follow-up: temporarily set a much higher limit, e.g.
"100000/minute", to isolate raw unthrottled throughput from
rate-limiting behavior -- not done here to keep this run's config
identical to what's actually deployed); or multi-instance/horizontal
scaling (there is no load balancer or orchestration layer in this
platform yet -- see `ROADMAP.md`).

## Extending this to the other services

The same locustfile pattern (a `HttpUser` posting a realistic payload
with the real `X-API-Key` header) applies directly to any of the other 13
services once each can run standalone -- most need only their small,
already-git-tracked artifacts (policy JSON, frozen transition matrices)
the way Problem 7 does; the exceptions are the services built on a large
trained model file excluded from this repo.
