"""The Notes CRUD endpoints.

Each route does three things and nothing more:
  1. receive validated input (FastAPI + Pydantic handle validation),
  2. call ONE storage method,
  3. translate storage errors into HTTP status codes.

No business logic leaks into storage; no storage details leak into HTTP.
"""

import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas import Note, NoteCreate, NoteUpdate
from app.storage import NoteNotFound, store

logger = logging.getLogger(__name__)

# prefix => every path here starts with /notes. tags => grouping in /docs.
router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[Note])
def list_notes():
    return store.list()


@router.post("", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate):
    note = store.create(payload)
    # Structured-ish log: a message + machine-readable fields. When we add Loki
    # later, these `extra` fields become searchable labels.
    logger.info("note created", extra={"note_id": note.id})
    return note


@router.get("/{note_id}", response_model=Note)
def get_note(note_id: str):
    try:
        return store.get(note_id)
    except NoteNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@router.put("/{note_id}", response_model=Note)
def update_note(note_id: str, payload: NoteUpdate):
    try:
        note = store.update(note_id, payload)
    except NoteNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    logger.info("note updated", extra={"note_id": note.id})
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str):
    try:
        store.delete(note_id)
    except NoteNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    logger.info("note deleted", extra={"note_id": note_id})
    # 204 No Content => intentionally return nothing.
