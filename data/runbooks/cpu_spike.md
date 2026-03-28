# CPU Spike

## Symptoms
- p95 latency rise with CPU saturation suggests compute bottleneck.
- CPU spikes after deploy can indicate runaway loops or hot query plans.

## Verification
- Verify top processes and thread pools before scaling blindly.
- Compare current release hash with last stable release.

## Safe Response
- Throttle non-critical traffic and apply controlled scaling.
- Roll back recent change if saturation remains after mitigation.
