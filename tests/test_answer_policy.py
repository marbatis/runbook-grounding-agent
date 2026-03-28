from __future__ import annotations

from app.services.answer_policy import AnswerPolicy
from app.services.chunker import RunbookChunker
from app.services.retrieval import RunbookRetrieval


def test_answer_policy_abstains_for_unsupported_question(runbook_dir) -> None:
    chunks = RunbookChunker(runbook_dir).load_chunks()
    retrieval = RunbookRetrieval(chunks)
    selected = retrieval.retrieve("What is the best smartphone this year?", top_k=3)

    response = AnswerPolicy(min_confidence=0.5).build_response(
        question="What is the best smartphone this year?",
        chunks=selected,
    )

    assert response.insufficient_evidence is True
    assert "enough grounded runbook evidence" in response.answer


def test_grounded_answer_contains_citations(runbook_dir) -> None:
    chunks = RunbookChunker(runbook_dir).load_chunks()
    retrieval = RunbookRetrieval(chunks)
    selected = retrieval.retrieve("How should I handle payment queue backlog?", top_k=3)

    response = AnswerPolicy(min_confidence=0.2).build_response(
        question="How should I handle payment queue backlog?",
        chunks=selected,
    )

    assert response.insufficient_evidence is False
    assert response.cited_chunks
    for chunk in response.cited_chunks:
        assert chunk.citation in response.answer
