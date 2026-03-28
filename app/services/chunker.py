from __future__ import annotations

import re
from pathlib import Path

from app.schemas.models import RunbookChunk


class RunbookChunker:
    def __init__(self, runbook_dir: Path):
        self.runbook_dir = runbook_dir

    def load_chunks(self) -> list[RunbookChunk]:
        chunks: list[RunbookChunk] = []
        for path in sorted(self.runbook_dir.glob("*.md")):
            chunks.extend(self._chunk_file(path))
        return chunks

    def _chunk_file(self, path: Path) -> list[RunbookChunk]:
        lines = path.read_text(encoding="utf-8").splitlines()
        section = "Overview"
        chunk_index = 0
        chunks: list[RunbookChunk] = []

        for line_no, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                section = line.lstrip("#").strip()
                continue
            if len(line) < 20:
                continue

            chunk_index += 1
            citation = f"RBK:{path.name}#L{line_no}"
            chunks.append(
                RunbookChunk(
                    chunk_id=f"{path.stem}-{chunk_index}",
                    runbook=path.stem,
                    section=section,
                    text=line,
                    score=0.0,
                    citation=citation,
                )
            )

        return chunks


TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]
