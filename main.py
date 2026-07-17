"""Stage 0: the smallest possible FastAPI server."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_server() -> dict[str, str]:
    """Return a simple message to prove the server is running."""
    return {"message": "Hello, server"}
