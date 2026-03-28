# Batch Window Miss

## Symptoms
- Batch job completion after SLA window indicates scheduling drift or resource contention.
- Repeated misses across days require escalation to platform operations.

## Verification
- Verify upstream dependency completion times and queue lag.
- Confirm cron schedule, timezone alignment, and lock acquisition delays.

## Safe Response
- Run targeted backfill only after validating downstream reconciliation impact.
- Notify stakeholders before changing batch cadence.
