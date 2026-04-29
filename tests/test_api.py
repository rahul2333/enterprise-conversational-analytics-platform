from fastapi.testclient import TestClient

from src.api import main

client = TestClient(main.app)


def test_health():
    res = client.get("/")
    assert res.status_code == 200


def test_query_blocks_non_select_sql(monkeypatch):
    monkeypatch.setattr(main.llm, "generate_sql", lambda question, context: "DELETE FROM demo")

    response = client.post("/query", json={"question": "delete all rows", "execute": True})
    assert response.status_code == 200

    payload = response.json()
    assert payload["is_sql_valid"] is False
    assert payload["execution_mode"] == "blocked"
    assert payload["warnings"]
