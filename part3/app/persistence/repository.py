from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Repository(ABC):
    """
    Abstract base class for repository pattern.
    Defines the interface for data persistence operations.
    """

    @abstractmethod
    def add(self, obj: Any) -> None:
        """
        Add an object to the repository.

        Args:
            obj: Object to add
        """
        pass

    @abstractmethod
    def get(self, obj_id: str) -> Optional[Any]:
        """
        Retrieve an object by its ID.

        Args:
            obj_id: Object identifier

        Returns:
            The object if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        """
        Retrieve all objects from the repository.

        Returns:
            List of all objects
        """
        pass

    @abstractmethod
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        """
        Update an object with new data.

        Args:
            obj_id: Object identifier
            data: Dictionary containing updated attributes

        Returns:
            The updated object if found, None otherwise
        """
        pass

    @abstractmethod
    def delete(self, obj_id: str) -> bool:
        """
        Delete an object from the repository.

        Args:
            obj_id: Object identifier

        Returns:
            True if object was deleted, False otherwise
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        """
        Retrieve an object by a specific attribute value.

        Args:
            attr_name: Name of the attribute to search by
            attr_value: Value to match

        Returns:
            The first object matching the criteria, None if not found
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository interface.
    Stores objects in a dictionary indexed by their ID.
    """

    def __init__(self):
        """Initialize the in-memory storage."""
        self._storage: Dict[str, Any] = {}

    def add(self, obj: Any) -> None:
        """
        Add an object to the repository.

        Args:
            obj: Object to add (must have an 'id' attribute)

        Raises:
            ValueError: If email already exists (for User objects)
        """
        # Check for email uniqueness if object has email attribute
        if hasattr(obj, 'email'):
            existing = self.get_by_attribute('email', obj.email)
            if existing and existing.id != obj.id:
                raise ValueError(f"Email {obj.email} already exists")

        self._storage[obj.id] = obj

    def get(self, obj_id: str) -> Optional[Any]:
        """
        Retrieve an object by its ID.

        Args:
            obj_id: Object identifier

        Returns:
            The object if found, None otherwise
        """
        return self._storage.get(obj_id)

    def get_all(self) -> List[Any]:
        """
        Retrieve all objects from the repository.

        Returns:
            List of all objects
        """
        return list(self._storage.values())

    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        """
        Update an object with new data.

        Args:
            obj_id: Object identifier
            data: Dictionary containing updated attributes

        Returns:
            The updated object if found, None otherwise
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
        return obj

    def delete(self, obj_id: str) -> bool:
        """
        Delete an object from the repository.

        Args:
            obj_id: Object identifier

        Returns:
            True if object was deleted, False otherwise
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        """
        Retrieve an object by a specific attribute value.

        Args:
            attr_name: Name of the attribute to search by
            attr_value: Value to match

        Returns:
            The first object matching the criteria, None if not found
        """
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
