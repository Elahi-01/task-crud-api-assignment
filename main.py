"""Task API — Stage 2: read endpoints with in-memory data."""

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request

app = FastAPI(title="Task API", version="1.0")

# This list is the temporary in-memory data store.
tasks: list[dict[str, Any]] = [
    {"id": 1, "title": "Learn HTTP", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Test Swagger UI", "done": True},
]


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
        status_code=400,
        content={"error": "Invalid request body", "details": details},
    )


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
