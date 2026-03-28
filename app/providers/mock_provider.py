from __future__ import annotations

from app.providers.base import AnswerProvider


class MockAnswerProvider(AnswerProvider):
    def polish_answer(self, question: str, draft_answer: str, citations: list[str]) -> str:
        # In mock mode, return deterministic answer exactly.
        return draft_answer
