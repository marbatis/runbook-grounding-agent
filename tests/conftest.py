from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    db_url = f"sqlite:///{tmp_path / 'qa_test.db'}"

    monkeypatch.setenv("DATABASE_URL", db_url)
    monkeypatch.setenv("PROVIDER_MODE", "mock")
    monkeypatch.setenv("RETRIEVAL_MODE", "keyword")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    from app.config import get_settings
    from app.db import configure_database, init_db
    from app.main import create_app

    get_settings.cache_clear()
    configure_database(db_url)
    init_db()

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def runbook_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "runbooks"
