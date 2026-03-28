from __future__ import annotations

from collections import Counter
from typing import Optional

from app.schemas.models import RunbookChunk
from app.services.chunker import tokenize


class RunbookRetrieval:
    def __init__(self, chunks: list[RunbookChunk], mode: str = "keyword"):
        self.chunks = chunks
        self.mode = mode
        self.chunk_token_counts = [
            Counter(tokenize(chunk.text + " " + chunk.section))
            for chunk in chunks
        ]

    def retrieve(
        self,
        question: str,
        service_filter: Optional[str] = None,
        top_k: int = 4,
    ) -> list[RunbookChunk]:
        if self.mode == "embedding":
            scored = self._embedding_rank(question, service_filter)
        else:
            scored = self._keyword_rank(question, service_filter)

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def _keyword_rank(self, question: str, service_filter: Optional[str]) -> list[RunbookChunk]:
        query_tokens = tokenize(question)
        if not query_tokens:
            return []

        query_counter = Counter(query_tokens)
        scored: list[RunbookChunk] = []
        for chunk, token_counts in zip(self.chunks, self.chunk_token_counts):
            overlap = sum(min(query_counter[token], token_counts[token]) for token in query_counter)
            if overlap == 0:
                continue

            precision = overlap / max(1, len(query_tokens))
            section_boost = 0.1 if any(t in chunk.section.lower() for t in query_tokens) else 0.0
            filter_boost = (
                0.15
                if service_filter and service_filter.lower() in chunk.runbook.lower()
                else 0.0
            )
            score = min(1.0, precision + section_boost + filter_boost)
            scored.append(chunk.model_copy(update={"score": score}))

        return scored

    def _embedding_rank(self, question: str, service_filter: Optional[str]) -> list[RunbookChunk]:
        # Deterministic pseudo-embedding ranking to keep MVP dependency-free.
        query_vec = self._hash_vector(question)
        scored: list[RunbookChunk] = []
        for chunk in self.chunks:
            chunk_vec = self._hash_vector(chunk.text)
            score = self._cosine(query_vec, chunk_vec)
            if service_filter and service_filter.lower() in chunk.runbook.lower():
                score += 0.1
            if score <= 0:
                continue
            scored.append(chunk.model_copy(update={"score": min(score, 1.0)}))
        return scored

    @staticmethod
    def _hash_vector(text: str, dims: int = 32) -> list[float]:
        vec = [0.0] * dims
        for token in tokenize(text):
            index = sum(ord(ch) for ch in token) % dims
            vec[index] += 1.0
        return vec

    @staticmethod
    def _cosine(vec_a: list[float], vec_b: list[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)
