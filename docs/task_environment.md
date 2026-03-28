# Task Environment

## 1. Rational Objective

Answer operational questions using only grounded runbook evidence. When evidence is weak or unrelated, abstain explicitly instead of guessing.

## 2. PEAS

- Performance:
  - retrieval relevance
  - citation inclusion in every grounded answer
  - abstention accuracy on unsupported questions
- Environment:
  - local markdown runbook corpus and benchmark question set
- Actuators:
  - API response payloads, server-rendered views, query history records
- Sensors:
  - user question text, optional service filter, runbook chunk corpus

## 3. Environmental Dimensions

- Evidence quality varies by runbook coverage and specificity.
- Questions can be noisy or out-of-domain.
- Safety requires refusing unsupported requests.
- Model behavior is optional and subordinate to deterministic policy.

## 4. Problem Formalization

Given question `q` and optional filter `f`:

1. chunk corpus `C`
2. retrieve top chunks `R(q, f)` deterministically
3. compute confidence `s`
4. if `s < threshold`, abstain
5. else generate answer from `R` with explicit citations
6. optionally polish wording without changing claims

## 5. Architecture Choice

A retrieval-policy architecture is used:

- deterministic chunk retrieval
- deterministic answer policy and abstention
- optional provider for stylistic polish only

This keeps decisions inspectable and prevents hidden model authority.

## 6. Guardrails / Workflow Maturity

- no invented procedures
- citation-required grounded answers
- explicit insufficiency warning
- no client-side model calls
- backend-only secret handling
- query history for auditability
