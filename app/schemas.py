"""Pydantic models = the *shape* of data crossing the API boundary.

FastAPI uses these to:
  - validate incoming JSON (reject bad requests with a 422 automatically),
  - serialize outgoing responses,
  - generate the interactive /docs.

We deliberately use THREE models instead of one, because "what a client may
send when creating", "what they may send when updating", and "what we return"
are genuinely different shapes. Conflating them is a classic source of bugs
(e.g. letting a client set the server-owned `id` or `created_at`).
"""

from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Fields a client provides to CREATE a note."""

    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="", max_length=10_000)


class NoteUpdate(BaseModel):
    """Fields a client may provide to UPDATE a note. All optional (partial update).

    `None` here means "not provided" — we only touch fields the client actually sent.
    """

    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, max_length=10_000)


class Note(NoteCreate):
    """A stored note as RETURNED to clients (server-owned fields included)."""

    id: str
    created_at: datetime
    updated_at: datetime
