from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class ChatMessageRecord:
    role: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)


class SessionRepository:
    """In-memory session store with the same interface used for PostgreSQL-backed storage."""

    def __init__(self) -> None:
        self._sessions: Dict[str, List[ChatMessageRecord]] = {}

    def append_message(self, session_id: str, role: str, content: str) -> None:
        self._sessions.setdefault(session_id, []).append(ChatMessageRecord(role=role, content=content))

    def get_messages(self, session_id: str) -> List[ChatMessageRecord]:
        return self._sessions.get(session_id, [])
