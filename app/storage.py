"""Storage layer, hidden behind a tiny interface.

Right now notes live in a plain in-memory dict, which means they vanish when the
process restarts. That's fine for building everything else first.

The important design choice: the routes talk to this store through five methods
(list / create / get / update / delete) and NOTHING else. They never touch the
dict directly. So when we reach the "database" layer, we can write a
PostgresNoteStore with the same five methods and swap it in — without changing a
single line of the API routes. That clean seam is the whole point.
"""

from datetime import datetime, timezone
from uuid import uuid4

from app.schemas import Note, NoteCreate, NoteUpdate


class NoteNotFound(Exception):
    """Raised by the store when a note id doesn't exist.

    Note this is a *storage* concept, not an HTTP one — the store knows nothing
    about 404s. The router translates this exception into an HTTP 404. Keeping
    HTTP concerns out of storage is what lets us reuse the store elsewhere
    (e.g. a background worker) later.
    """


class InMemoryNoteStore:
    def __init__(self) -> None:
        self._notes: dict[str, Note] = {}

    def list(self) -> list[Note]:
        return list(self._notes.values())

    def create(self, data: NoteCreate) -> Note:
        now = datetime.now(timezone.utc)
        note = Note(
            id=uuid4().hex,
            title=data.title,
            content=data.content,
            created_at=now,
            updated_at=now,
        )
        self._notes[note.id] = note
        return note

    def get(self, note_id: str) -> Note:
        try:
            return self._notes[note_id]
        except KeyError as exc:
            raise NoteNotFound(note_id) from exc

    def update(self, note_id: str, data: NoteUpdate) -> Note:
        note = self.get(note_id)  # raises NoteNotFound if missing
        # exclude_unset=True => only overwrite fields the client actually sent.
        changes = data.model_dump(exclude_unset=True)
        updated = note.model_copy(update={**changes, "updated_at": datetime.now(timezone.utc)})
        self._notes[note_id] = updated
        return updated

    def delete(self, note_id: str) -> None:
        if note_id not in self._notes:
            raise NoteNotFound(note_id)
        del self._notes[note_id]


# Single shared instance the app uses. Swapping storage backends later means
# changing just this line (and providing a class with the same methods).
store = InMemoryNoteStore()
