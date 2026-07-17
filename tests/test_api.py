"""Automated checks for every required CRUD behavior and status code."""

import pytest
from fastapi.testclient import TestClient

from main import app, reset_tasks

client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_seed_tasks() -> None:
    """Give every test a fresh copy of the three example tasks."""
    reset_tasks()


def test_root_and_health_endpoints() -> None:
    root = client.get("/")
    assert root.status_code == 200
    assert root.json() == {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}


def test_read_all_and_single_task() -> None:
    all_tasks = client.get("/tasks")
    assert all_tasks.status_code == 200
    assert len(all_tasks.json()) == 3

    one_task = client.get("/tasks/1")
    assert one_task.status_code == 200
    assert one_task.json()["title"] == "Learn HTTP"


def test_unknown_task_returns_json_404() -> None:
    response = client.get("/tasks/99")
    assert response.status_code == 404
    assert response.json() == {"error": "Task 99 not found"}


def test_create_task_returns_201_and_persists_in_memory() -> None:
    created = client.post("/tasks", json={"title": "Buy milk"})
    assert created.status_code == 201
    assert created.json() == {"id": 4, "title": "Buy milk", "done": False}

    all_tasks = client.get("/tasks")
    assert len(all_tasks.json()) == 4


def test_create_rejects_missing_or_empty_title_with_400() -> None:
    missing = client.post("/tasks", json={})
    assert missing.status_code == 400
    assert "error" in missing.json()

    empty = client.post("/tasks", json={"title": "   "})
    assert empty.status_code == 400
    assert "error" in empty.json()


def test_update_title_and_done() -> None:
    response = client.put(
        "/tasks/1",
        json={"title": "Learn FastAPI", "done": True},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "done": True,
    }


def test_update_accepts_done_only_but_rejects_empty_body() -> None:
    done_only = client.put("/tasks/1", json={"done": True})
    assert done_only.status_code == 200
    assert done_only.json()["done"] is True

    empty = client.put("/tasks/1", json={})
    assert empty.status_code == 400
    assert "error" in empty.json()


def test_update_unknown_task_returns_404() -> None:
    response = client.put("/tasks/99", json={"done": True})
    assert response.status_code == 404
    assert response.json() == {"error": "Task 99 not found"}


def test_delete_returns_empty_204_and_removes_task() -> None:
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    assert response.content == b""

    missing_after_delete = client.get("/tasks/1")
    assert missing_after_delete.status_code == 404


def test_delete_unknown_task_returns_404() -> None:
    response = client.delete("/tasks/99")
    assert response.status_code == 404
    assert response.json() == {"error": "Task 99 not found"}
