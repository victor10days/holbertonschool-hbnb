from __future__ import annotations
from typing import Dict, Type, TypeVar, List, Optional, Callable
from dataclasses import asdict

T = TypeVar("T")

class MemoryRepository:
    """Simple in-memory repo keyed by model class name then id."""

    def __init__(self):
        self._db: Dict[str, Dict[str, object]] = {}

    def _bucket(self, cls: Type[T]) -> Dict[str, T]:
        return self._db.setdefault(cls.__name__, {})  # type: ignore

    def add(self, obj: T) -> T:
        bucket = self._bucket(type(obj))
        bucket[obj.id] = obj
        return obj

    def get(self, cls: Type[T], obj_id: str) -> Optional[T]:
        return self._bucket(cls).get(obj_id)  # type: ignore

    def list(self, cls: Type[T], predicate: Optional[Callable[[T], bool]] = None) -> List[T]:
        values = list(self._bucket(cls).values())  # type: ignore
        return [v for v in values if predicate(v)] if predicate else values

    def update(self, obj: T) -> T:
        bucket = self._bucket(type(obj))
        if obj.id not in bucket:
            raise KeyError(f"{type(obj).__name__}({obj.id}) not found")
        bucket[obj.id] = obj
        return obj

    def delete(self, cls: Type[T], obj_id: str) -> None:
        bucket = self._bucket(cls)
        if obj_id in bucket:
            del bucket[obj_id]
