# Cache Saturation

## Symptoms
- Hit rate collapse with eviction surge indicates cache saturation.
- Backend latency growth may follow cache churn and miss storms.

## Verification
- Verify cache memory pressure and key cardinality growth.
- Check whether recent release changed cache key patterns.

## Safe Response
- Reduce churn-heavy features and tune eviction policy safely.
- Coordinate with service owner before cache flush operations.
