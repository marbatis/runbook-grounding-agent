from __future__ import annotations


def test_health_mock_mode(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["active_provider"] == "mock"
