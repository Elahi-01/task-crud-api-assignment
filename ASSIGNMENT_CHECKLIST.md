# Assignment checklist

- [x] Server starts on localhost with one documented command.
- [x] `GET /tasks` lists every task.
- [x] `GET /tasks/{id}` returns one task or JSON `404`.
- [x] `POST /tasks` creates a task with JSON `201`.
- [x] `PUT /tasks/{id}` updates title and/or done.
- [x] `DELETE /tasks/{id}` returns an empty `204` response.
- [x] Invalid POST and PUT bodies return JSON `400`.
- [x] Storage is an in-memory Python list; there is no database or file storage.
- [x] Swagger UI is available at `/docs`.
- [x] Automated tests cover the full CRUD cycle and status codes.
- [x] Git history contains one meaningful commit for every required stage.
- [x] README contains installation, run instructions, endpoint table, curl output, and Swagger screenshot.

The only step that must be completed by the repository owner is creating a public GitHub repository and pushing this existing Git history to it.
