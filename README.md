# Team Notes API

A REST API for sharing notes within small teams.

Built with FastAPI and SQLAlchemy. Uses SQLite locally and PostgreSQL with Docker.

## Run

Python 3.11+ required.

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\activate
```

Then run:

```bash
pip install -e ".[test]"
python -m app.init_db
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

Or run with Docker:

```bash
docker compose up --build
```

## Tests

```bash
pytest -q
```

## API

- `POST /users` — create a user
- `POST /teams` — create a team
- `POST /teams/{team_id}/members/{user_id}` — add a member
- `POST /teams/{team_id}/notes` — create a note
- `GET /teams/{team_id}/notes` — list notes
- `GET /teams/{team_id}/notes/{note_id}` — get a note
- `PATCH /teams/{team_id}/notes/{note_id}` — update a note
- `DELETE /teams/{team_id}/notes/{note_id}` — delete a note

Send `X-User-Id` with team requests. Users can only access notes in teams they belong to.

## Decisions

- Notes belong to teams rather than individual users. This keeps sharing and access checks simple.
- PostgreSQL supports concurrent writes; SQLite makes local setup quick.
- Routes, database models, and access checks are kept separate so the code is easier to extend.

## With more time

I'd replace `X-User-Id` with real authentication. Right now it's only a demo identity header and is **not safe for a public deployment**. I'd also add database migrations, more integration tests, and edit-conflict handling.

I left out attachments, real-time editing, and a separate service layer for now. They add complexity without helping the basic notes workflow.
