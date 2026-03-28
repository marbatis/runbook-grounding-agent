from __future__ import annotations

from app.services.chunker import RunbookChunker


def test_chunker_loads_chunks_with_citations(runbook_dir) -> None:
    chunks = RunbookChunker(runbook_dir).load_chunks()
    assert len(chunks) >= 30
    assert all(chunk.citation.startswith("RBK:") for chunk in chunks)
    assert any("#L" in chunk.citation for chunk in chunks)
