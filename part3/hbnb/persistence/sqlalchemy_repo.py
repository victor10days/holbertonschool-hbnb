"""
SQLAlchemy Repository implementation.
Provides database persistence using SQLAlchemy ORM.
"""
from __future__ import annotations
from typing import Type, TypeVar, List, Optional, Callable
from sqlalchemy.orm import Session

T = TypeVar("T")


class SQLAlchemyRepository:
    """
    Repository class for database persistence using SQLAlchemy.
    Implements the same interface as MemoryRepository for easy transition.
    """

    def __init__(self, db_session: Session):
        """
        Initialize the repository with a database session.

        Args:
            db_session: SQLAlchemy database session
        """
        self._session = db_session

    def add(self, obj: T) -> T:
        """
        Add a new object to the database.

        Args:
            obj: The object to add

        Returns:
            The added object
        """
        self._session.add(obj)
        self._session.commit()
        return obj

    def get(self, cls: Type[T], obj_id: str) -> Optional[T]:
        """
        Retrieve an object by its ID.

        Args:
            cls: The class type of the object
            obj_id: The ID of the object

        Returns:
            The object if found, None otherwise
        """
        return self._session.query(cls).filter_by(id=obj_id).first()

    def list(self, cls: Type[T], predicate: Optional[Callable[[T], bool]] = None) -> List[T]:
        """
        List all objects of a given type, optionally filtered by a predicate.

        Args:
            cls: The class type of objects to list
            predicate: Optional filter function

        Returns:
            List of objects matching the criteria
        """
        query = self._session.query(cls)
        results = query.all()

        if predicate:
            return [obj for obj in results if predicate(obj)]

        return results

    def update(self, obj: T) -> T:
        """
        Update an existing object in the database.

        Args:
            obj: The object to update

        Returns:
            The updated object
        """
        self._session.merge(obj)
        self._session.commit()
        return obj

    def delete(self, cls: Type[T], obj_id: str) -> None:
        """
        Delete an object from the database.

        Args:
            cls: The class type of the object
            obj_id: The ID of the object to delete
        """
        obj = self.get(cls, obj_id)
        if obj:
            self._session.delete(obj)
            self._session.commit()
