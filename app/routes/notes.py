from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from sqlalchemy import select

from app.access import Database, TeamMember
from app.models import Note
from app.schemas import NoteInput, NotePatch, NoteView

router = APIRouter(prefix="/teams/{team_id}/notes")


def find_note(db, team_id, note_id):
    note = db.get(Note, note_id)
    if note is None or note.team_id != team_id:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("", response_model=NoteView, status_code=201)
def create_note(team_id: str, data: NoteInput, db: Database, member: TeamMember):
    note = Note(team_id=team_id, author_id=member.id, **data.model_dump())
    db.add(note)
    db.commit()
    return note


@router.get("", response_model=list[NoteView])
def list_notes(
    team_id: str, db: Database, member: TeamMember,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return db.scalars(
        select(Note).where(Note.team_id == team_id)
        .order_by(Note.updated_at.desc(), Note.id).offset(offset).limit(limit)
    ).all()


@router.get("/{note_id}", response_model=NoteView)
def get_note(team_id: str, note_id: str, db: Database, member: TeamMember):
    return find_note(db, team_id, note_id)


@router.patch("/{note_id}", response_model=NoteView)
def update_note(team_id: str, note_id: str, data: NotePatch, db: Database, member: TeamMember):
    note = find_note(db, team_id, note_id)
    changes = data.model_dump(exclude_unset=True)
    if any(value is None for value in changes.values()):
        raise HTTPException(status_code=422, detail="Note fields cannot be null")
    for field, value in changes.items():
        setattr(note, field, value)
    db.commit()
    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(team_id: str, note_id: str, db: Database, member: TeamMember):
    db.delete(find_note(db, team_id, note_id))
    db.commit()
    return Response(status_code=204)
