from __future__ import annotations

from abc import ABC, abstractmethod


class AnswerProvider(ABC):
    @abstractmethod
    def polish_answer(self, question: str, draft_answer: str, citations: list[str]) -> str:
        """Optional answer polishing. Must preserve grounded meaning and citations."""
