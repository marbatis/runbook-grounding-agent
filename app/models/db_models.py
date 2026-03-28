from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class QARecord(Base):
    __tablename__ = "qa_history"

    query_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    service_filter: Mapped[str] = mapped_column(String(128), default="")
    confidence: Mapped[float] = mapped_column(Float)
    insufficient_evidence: Mapped[bool] = mapped_column(Boolean)
    answer_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
