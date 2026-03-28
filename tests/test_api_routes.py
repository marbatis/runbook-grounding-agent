from __future__ import annotations


def test_home_page_renders(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Grounded Runbook Q&A" in response.text


def test_api_ask_returns_citations_and_answer(client) -> None:
    response = client.post(
        "/api/qa/ask",
        json={"question": "How should I rotate certificates safely?"},
    )
    assert response.status_code == 201
    payload = response.json()

    assert payload["query_id"]
    assert isinstance(payload["cited_chunks"], list)
    assert payload["cited_chunks"]
    assert payload["answer"]


def test_api_ask_abstains_for_unsupported_question(client) -> None:
    response = client.post(
        "/api/qa/ask",
        json={"question": "Who will win the world cup in 2038?"},
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["insufficient_evidence"] is True


def test_fetch_query_and_history(client) -> None:
    create = client.post(
        "/api/qa/ask",
        json={"question": "How to handle DNS failure symptoms?"},
    )
    assert create.status_code == 201
    query_id = create.json()["query_id"]

    detail = client.get(f"/api/qa/{query_id}")
    assert detail.status_code == 200

    history = client.get("/api/history")
    assert history.status_code == 200
    assert history.json()["items"]
