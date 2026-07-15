"""End-to-end API tests using FastAPI's TestClient.

TestClient spins the app up in-process and lets us make real HTTP-style calls
without a running server — fast and perfect for CI. When we add GitHub Actions,
`pytest` is the gate that must pass before an image is built.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_is_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_readiness_is_ok():
    r = client.get("/health/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_create_note_returns_201_with_server_fields():
    r = client.post("/notes", json={"title": "First note", "content": "hello"})
    assert r.status_code == 201
    note = r.json()
    assert note["title"] == "First note"
    assert note["content"] == "hello"
    # server-owned fields must be present and populated by the server
    assert note["id"]
    assert note["created_at"]
    assert note["updated_at"]


def test_create_note_rejects_empty_title():
    # title has min_length=1, so an empty title must fail validation (422).
    r = client.post("/notes", json={"title": "", "content": "x"})
    assert r.status_code == 422


def test_get_note_roundtrip():
    created = client.post("/notes", json={"title": "Find me"}).json()
    r = client.get(f"/notes/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_list_returns_a_list():
    r = client.get("/notes")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_partial_update_only_changes_sent_fields():
    created = client.post("/notes", json={"title": "Old title", "content": "keep me"}).json()
    r = client.put(f"/notes/{created['id']}", json={"title": "New title"})
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"] == "New title"
    assert updated["content"] == "keep me"  # untouched because we didn't send it


def test_delete_then_get_is_404():
    created = client.post("/notes", json={"title": "temporary"}).json()
    assert client.delete(f"/notes/{created['id']}").status_code == 204
    assert client.get(f"/notes/{created['id']}").status_code == 404


def test_get_missing_note_is_404():
    r = client.get("/notes/this-id-does-not-exist")
    assert r.status_code == 404
