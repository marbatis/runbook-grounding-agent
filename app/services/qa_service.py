from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.providers.base import AnswerProvider
from app.providers.mock_provider import MockAnswerProvider
from app.providers.openai_provider import OpenAIAnswerProvider
from app.repositories.qa_repo import QARepository
from app.schemas.models import HistoryItem, QAResponse
from app.services.answer_policy import AnswerPolicy
from app.services.chunker import RunbookChunker
from app.services.retrieval import RunbookRetrieval

logger = logging.getLogger(__name__)


class QAService:
    def __init__(self, db: Session, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        root = Path(__file__).resolve().parents[2]
        runbook_dir = root / "data" / "runbooks"

        self.chunker = RunbookChunker(runbook_dir)
        chunks = self.chunker.load_chunks()
        self.retrieval = RunbookRetrieval(chunks, mode=self.settings.retrieval_mode)
        self.policy = AnswerPolicy(min_confidence=self.settings.min_confidence)
        self.repo = QARepository(db)
        self.provider = self._select_provider()

    def ask(self, question: str, service_filter: Optional[str] = None) -> QAResponse:
        retrieved = self.retrieval.retrieve(
            question=question,
            service_filter=service_filter,
            top_k=self.settings.max_chunks,
        )

        response = self.policy.build_response(
            question=question,
            chunks=retrieved,
            service_filter=service_filter,
        )

        if not response.insufficient_evidence:
            citations = [chunk.citation for chunk in response.cited_chunks]
            polished = self.provider.polish_answer(question, response.answer, citations)
            response = response.model_copy(update={"answer": polished})

        self.repo.save(
            query_id=response.query_id,
            question=question,
            service_filter=service_filter or "",
            result=response.model_dump(mode="json"),
        )

        logger.info(
            "qa_completed",
            extra={
                "query_id": response.query_id,
                "confidence": response.confidence,
                "insufficient_evidence": response.insufficient_evidence,
            },
        )
        return response

    def get(self, query_id: str) -> Optional[QAResponse]:
        raw = self.repo.get(query_id)
        if not raw:
            return None
        return QAResponse.model_validate(raw)

    def history(self, limit: int = 100) -> list[HistoryItem]:
        rows = self.repo.list_recent(limit=limit)
        return [
            HistoryItem(
                query_id=row["query_id"],
                question=row["question"],
                confidence=row["confidence"],
                insufficient_evidence=row["insufficient_evidence"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def list_runbooks(self) -> list[str]:
        return sorted({chunk.runbook for chunk in self.retrieval.chunks})

    def _select_provider(self) -> AnswerProvider:
        mode = self.settings.provider_mode
        if mode == "mock":
            return MockAnswerProvider()
        if mode == "openai":
            return OpenAIAnswerProvider(self.settings)

        if self.settings.openai_api_key:
            try:
                return OpenAIAnswerProvider(self.settings)
            except Exception:
                logger.exception("openai_provider_init_failed")

        return MockAnswerProvider()
