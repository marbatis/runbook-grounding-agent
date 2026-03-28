from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    service_filter: Optional[str] = Field(default=None, max_length=120)


class RunbookChunk(BaseModel):
    chunk_id: str
    runbook: str
    section: str
    text: str
    score: float
    citation: str


class QAResponse(BaseModel):
    query_id: str
    question: str
    answer: str
    cited_chunks: list[RunbookChunk]
    confidence: float = Field(ge=0.0, le=1.0)
    insufficient_evidence: bool
    safe_next_steps: list[str]
    related_runbooks: list[str]
    created_at: datetime


class HistoryItem(BaseModel):
    query_id: str
    question: str
    confidence: float
    insufficient_evidence: bool
    created_at: datetime
