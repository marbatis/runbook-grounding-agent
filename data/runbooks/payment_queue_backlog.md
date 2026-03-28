# Payment Queue Backlog

## Symptoms
- Queue depth growth with stable ingress usually indicates consumer slowdown.
- Payment retries and timeout spikes often amplify backlog growth.

## Verification
- Verify consumer lag and dead-letter volume before changing retry policy.
- Confirm downstream ledger latency and transaction lock contention.

## Safe Response
- Gradually increase consumer capacity and cap retry concurrency.
- Escalate to payments owner if backlog threatens settlement window.
