# Auth Token Failures

## Symptoms
- Repeated `invalid token signature` errors indicate signer drift or key mismatch.
- Sudden token verification failures after deploy should trigger rollback readiness review.

## Verification
- Verify clock skew between auth nodes before rotating keys.
- Confirm current key ID (kid) matches issuer metadata.

## Safe Response
- If login failure crosses threshold, escalate through incident escalation runbook.
- Rotate signer keys only with rollback checklist prepared.
