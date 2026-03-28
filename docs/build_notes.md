# Build Notes

- Implemented deterministic runbook chunking and retrieval before provider integration.
- Added explicit abstention policy with configurable confidence threshold.
- Added optional embedding-like deterministic retrieval mode via config switch.
- Added provider interface with mock default and OpenAI polish option.
- Added SQLite history persistence for traceability.
- Added benchmark question set (25 entries) for scenario evaluation.
