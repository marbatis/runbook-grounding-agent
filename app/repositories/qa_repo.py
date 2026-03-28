from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import QARecord


class QARepository:
    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        query_id: str,
        question: str,
        service_filter: str,
        result: dict[str, Any],
    ) -> None:
        record = QARecord(
            query_id=query_id,
            question=question,
            service_filter=service_filter or "",
            confidence=float(result["confidence"]),
            insufficient_evidence=bool(result["insufficient_evidence"]),
            answer_json=json.dumps(result, default=str),
        )
        self.db.add(record)
        self.db.commit()

    def get(self, query_id: str) -> Optional[dict[str, Any]]:
        stmt = select(QARecord).where(QARecord.query_id == query_id)
        row = self.db.scalar(stmt)
        if not row:
            return None
        return json.loads(row.answer_json)

    def list_recent(self, limit: int = 100) -> list[dict[str, Any]]:
        stmt = select(QARecord).order_by(desc(QARecord.created_at)).limit(limit)
        rows = self.db.scalars(stmt).all()
        return [json.loads(row.answer_json) for row in rows]
