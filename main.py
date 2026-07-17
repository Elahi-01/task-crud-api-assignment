"""A small in-memory CRUD API for managing to-do tasks."""

from copy import deepcopy
from typing import Any

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from starlette.requests import Request

app = FastAPI(
    title="Task API",
    version="1.0",
    description="Create, read, update, and delete in-memory to-do tasks.",
)

SEED_TASKS: list[dict[str, Any]] = [
    {"id": 1, "title": "Learn HTTP", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Test Swagger UI", "done": True},
]

tasks: list[dict[str, Any]] = deepcopy(SEED_TASKS)
next_task_id = 4


class TaskCreate(BaseModel):
    """Request body used to create a task."""

    model_config = ConfigDict(extra="forbid", strict=True)

    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title must not be empty")
        return cleaned


class TaskUpdate(BaseModel):
    """Request body used to update a task's title and/or completion state."""

    model_config = ConfigDict(extra="forbid", strict=True)

    title: str | None = None
    done: bool | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title must not be empty")
        return cleaned

    @model_validator(mode="after")
    def at_least_one_field_is_required(self) -> "TaskUpdate":
        if self.title is None and self.done is None:
            raise ValueError("Provide title and/or done")
        return self


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Keep every HTTP error in the required {\"error\": ...} format."""
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Convert FastAPI's default 422 validation response into HTTP 400."""
    details = [
        {
            "field": ".".join(str(part) for part in error["loc"] if part != "body")
            or "body",
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid request body", "details": details},
    )


def reset_tasks() -> None:
    """Restore the initial task list; used by the automated tests."""
    global tasks, next_task_id
    tasks = deepcopy(SEED_TASKS)
    next_task_id = 4


def find_task(task_id: int) -> dict[str, Any]:
    """Return a task by ID or raise a JSON-formatted 404 error."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.get("/", summary="Show API information")
def api_information() -> dict[str, object]:
    """Return the API name, version, and main resource endpoint."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health", summary="Check server health")
def health_check() -> dict[str, str]:
    """Return a small response that confirms the server is alive."""
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def list_tasks() -> list[dict[str, Any]]:
    """Return the complete in-memory task list."""
    return tasks


@app.get("/tasks/{task_id}", summary="Get one task")
def get_task(task_id: int) -> dict[str, Any]:
    """Return one task, or HTTP 404 when its ID does not exist."""
    return find_task(task_id)


@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
def create_task(payload: TaskCreate) -> dict[str, Any]:
    """Create a task with the next ID and an initial done value of false."""
    global next_task_id

    new_task = {
        "id": next_task_id,
        "title": payload.title,
        "done": False,
    }
    tasks.append(new_task)
    next_task_id += 1
    return new_task


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, payload: TaskUpdate) -> dict[str, Any]:
    """Update a task's title, completion state, or both."""
    task = find_task(task_id)

    if payload.title is not None:
        task["title"] = payload.title
    if payload.done is not None:
        task["done"] = payload.done

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(task_id: int) -> Response:
    """Remove a task and return an empty HTTP 204 response."""
    task = find_task(task_id)
    tasks.remove(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
