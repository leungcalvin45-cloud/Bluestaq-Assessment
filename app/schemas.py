from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class Named(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class Record(Named):
    model_config = ConfigDict(from_attributes=True)
    id: str


class NoteInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="", max_length=100000)


class NotePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, max_length=100000)


class NoteView(NoteInput):
    model_config = ConfigDict(from_attributes=True)
    id: str
    team_id: str
    author_id: str
    created_at: datetime
    updated_at: datetime
