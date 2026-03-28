# Dependency Outage

## Symptoms
- Upstream timeouts plus downstream 5xx usually indicate dependency outage.
- Connection refused errors from a shared dependency increase blast radius.

## Verification
- Verify dependency status page and cross-check internal error telemetry.
- Identify impacted services before failover or degraded mode changes.

## Safe Response
- Enable degraded mode if dependency remains unavailable.
- Coordinate communication with dependency owner and incident commander.
