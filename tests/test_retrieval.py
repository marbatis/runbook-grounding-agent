from __future__ import annotations

from app.services.chunker import RunbookChunker
from app.services.retrieval import RunbookRetrieval


def test_retrieval_prefers_relevant_runbook(runbook_dir) -> None:
    chunks = RunbookChunker(runbook_dir).load_chunks()
    retrieval = RunbookRetrieval(chunks, mode="keyword")

    top = retrieval.retrieve("How to rotate certificate safely in production?", top_k=3)
    assert top
    assert top[0].runbook == "certificate_rotation"


def test_embedding_mode_returns_ranked_chunks(runbook_dir) -> None:
    chunks = RunbookChunker(runbook_dir).load_chunks()
    retrieval = RunbookRetrieval(chunks, mode="embedding")

    top = retrieval.retrieve("dns resolution timeout and nxdomain", top_k=3)
    assert top
    assert len(top) <= 3
