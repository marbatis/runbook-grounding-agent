# Database Connection Pool Exhaustion

## Symptoms
- Connection acquisition timeout and request queuing indicate pool exhaustion.
- Retry storms can quickly consume pool capacity.

## Verification
- Verify active connection counts and long-running query footprint.
- Confirm pool sizing and transaction timeout settings.

## Safe Response
- Throttle callers and reduce concurrency before raising pool limits.
- Escalate if write-path latency threatens customer transactions.
