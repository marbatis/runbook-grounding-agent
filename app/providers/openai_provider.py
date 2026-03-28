from __future__ import annotations

import json
import logging
from typing import Optional

from app.config import Settings
from app.providers.base import AnswerProvider

logger = logging.getLogger(__name__)


class OpenAIAnswerProvider(AnswerProvider):
    def __init__(self, settings: Settings):
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider")

        try:
            from openai import OpenAI
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("openai package is required") from exc

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def polish_answer(self, question: str, draft_answer: str, citations: list[str]) -> str:
        prompt = {
            "question": question,
            "draft_answer": draft_answer,
            "citations": citations,
            "instruction": (
                "Rewrite for clarity in one concise paragraph. "
                "Do not add claims beyond draft_answer. "
                "Keep every citation ID exactly as provided."
            ),
        }

        try:
            response = self.client.responses.create(
                model=self.model,
                input=json.dumps(prompt),
            )
            text: Optional[str] = getattr(response, "output_text", None)
            if text and text.strip():
                polished = text.strip()
                if all(citation in polished for citation in citations):
                    return polished
        except Exception as exc:  # pragma: no cover
            logger.exception("openai_polish_failed", extra={"error": str(exc)})

        return draft_answer
