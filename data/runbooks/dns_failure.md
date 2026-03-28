# DNS Failure

## Symptoms
- Name resolution timeout and NXDOMAIN spikes indicate DNS path failure.
- Partial regional failure can masquerade as intermittent dependency errors.

## Verification
- Verify resolver health, TTL behavior, and authoritative zone status.
- Confirm application retries are not hiding resolution instability.

## Safe Response
- Shift traffic to healthy resolver path if failover is available.
- Escalate to network operations when resolution failures persist.
