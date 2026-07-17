"""Task API — Stage 1: root and health endpoints."""

from fastapi import FastAPI

app = FastAPI(title="Task API", version="1.0")


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
