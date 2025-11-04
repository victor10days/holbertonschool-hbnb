from __future__ import annotations
import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

def now_iso() -> str:
    return datetime.utcnow().strftime(ISO)

@dataclass
class BaseModel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return asdict(self)

    def touch(self) -> None:
        self.updated_at = now_iso()
