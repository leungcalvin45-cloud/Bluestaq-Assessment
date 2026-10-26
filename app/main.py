from fastapi import FastAPI

from app.db import Base, engine
from app import models  # Register tables before creating them.
from app.routes import notes, teams


def create_app():
    app = FastAPI(title="Team Notes")
    app.include_router(teams.router)
    app.include_router(notes.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
