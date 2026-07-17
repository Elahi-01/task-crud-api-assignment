# Task CRUD API

A small **in-memory to-do list CRUD API** built with Python and FastAPI. It supports creating, reading, updating, and deleting tasks, uses the required HTTP status codes, provides JSON error messages, and includes interactive Swagger UI documentation.

> The data is intentionally stored only in memory. Restarting the server restores the three seed tasks because this assignment does not use a database or file storage.

## Features

- Full CRUD operations for tasks
- Three preloaded example tasks
- Input validation for POST and PUT requests
- JSON errors with HTTP 400 and 404
- Correct success codes: 200, 201, and 204
- Swagger UI at `/docs`
- Automated pytest coverage for the required behavior
- Stage-by-stage Git commit history

## Requirements

- Python 3.10 or newer
- Git

## Installation

### Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the API

Run this one documented command from the project folder:

```bash
uvicorn main:app --reload
```

Open:

- API information: `http://localhost:8000/`
- Health check: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Task format

```json
{
  "id": 1,
  "title": "Learn HTTP",
  "done": false
}
```

## Endpoints

| Method | Endpoint | Purpose | Success | Possible errors |
|---|---|---|---:|---:|
| GET | `/` | Show API information | 200 | — |
| GET | `/health` | Check whether the server is alive | 200 | — |
| GET | `/tasks` | List every task | 200 | — |
| GET | `/tasks/{id}` | Get one task | 200 | 404 |
| POST | `/tasks` | Create a new task | 201 | 400 |
| PUT | `/tasks/{id}` | Update title and/or done | 200 | 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204 | 404 |

## Request examples

### Create

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

### Update

```bash
curl -i -X PUT http://localhost:8000/tasks/4 \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk and bread","done":true}'
```

### Delete

```bash
curl -i -X DELETE http://localhost:8000/tasks/4
```

## Actual `curl -i` output

The following output was captured from the running project:

```text
HTTP/1.1 200 OK
date: Fri, 17 Jul 2026 14:51:04 GMT
server: uvicorn
content-length: 42
content-type: application/json

{"id":1,"title":"Learn HTTP","done":false}
```

## Swagger UI

Open `/docs`, choose an endpoint, click **Try it out**, enter the request data, and click **Execute**.

![Swagger UI showing the Task API endpoints](screenshots/swagger-ui.png)

## Run automated tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Git history

This repository was built in separate stages. Check the history with:

```bash
git log --oneline
```

Expected stage commits:

1. `Stage 0: hello server`
2. `Stage 1: root and health endpoints`
3. `Stage 2: read endpoints with 404`
4. `Stage 3: create with validation`
5. `Stage 4: full CRUD`
6. `Stage 5: Swagger UI`
7. `Stage 6: publish and docs`

## Important observation about in-memory storage

After creating or updating tasks, stopping and restarting the server removes those changes and restores the seed list. This happens because the task data lives in Python variables in RAM rather than in persistent database storage.

## Publishing

Read [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md) before publishing. The included `.git` directory preserves the required commit history.
