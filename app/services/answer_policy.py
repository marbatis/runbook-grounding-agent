from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.schemas.models import QAResponse, RunbookChunk


class AnswerPolicy:
    def __init__(self, min_confidence: float = 0.35):
        self.min_confidence = min_confidence

    def build_response(
        self,
        question: str,
        chunks: list[RunbookChunk],
        service_filter: Optional[str] = None,
    ) -> QAResponse:
        confidence = chunks[0].score if chunks else 0.0
        insufficient = confidence < self.min_confidence or not chunks

        if insufficient:
            answer = (
                "I do not have enough grounded runbook evidence to answer safely. "
                "Please provide a clearer service/context signal or check related runbooks first."
            )
            safe_next_steps = [
                "Confirm impacted service and environment",
                "Collect recent alerts/log excerpts",
                "Re-run query with service_filter",
            ]
            related = sorted({chunk.runbook for chunk in chunks})
            cited = chunks[:2]
        else:
            cited = chunks[:4]
            citation_text = ", ".join(chunk.citation for chunk in cited)
            snippets = " ".join(chunk.text for chunk in cited[:2])
            answer = (
                f"Based on runbook guidance: {snippets} "
                f"Citations: {citation_text}."
            )
            safe_next_steps = self._next_steps(cited)
            related = sorted({chunk.runbook for chunk in cited})

        return QAResponse(
            query_id=str(uuid4()),
            question=question,
            answer=answer,
            cited_chunks=cited,
            confidence=round(confidence, 3),
            insufficient_evidence=insufficient,
            safe_next_steps=safe_next_steps,
            related_runbooks=related,
            created_at=datetime.now(timezone.utc),
        )

    def _next_steps(self, chunks: list[RunbookChunk]) -> list[str]:
        steps = ["Validate preconditions listed in cited runbook sections"]
        if any("rollback" in chunk.text.lower() for chunk in chunks):
            steps.append("Prepare rollback checklist before action")
        if any("escalat" in chunk.text.lower() for chunk in chunks):
            steps.append("Escalate according to cited escalation section")
        if any("verify" in chunk.text.lower() for chunk in chunks):
            steps.append("Verify observed symptoms against cited checks")
        steps.append("Record timeline and evidence references in incident notes")
        return steps[:4]
