# Certificate Rotation

## Preconditions
- Verify certificate expiry window and trust chain integrity.
- Confirm all dependent services support new certificate bundle.

## Safe Rotation
- Rotate certificate in staged order and validate handshake success after each step.
- Keep prior certificate available for immediate rollback.

## Escalation
- If handshake failure impacts production auth or ingress, escalate immediately.
