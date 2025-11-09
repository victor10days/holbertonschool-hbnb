import uuid
from datetime import datetime
from typing import Dict, Any


class BaseModel:
    """
    Base model class for all entities.
    Provides common attributes and methods.

    Attributes:
        id (str): UUID stored as a string
        created_at (datetime): Timestamp at creation
        updated_at (datetime): Timestamp at last update
    """

    def __init__(self):
        """Initialize base attributes with UUID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data: Dict[str, Any]):
        """
        Update object attributes from dictionary and save.

        Args:
            data: Dictionary containing attributes to update
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """
        Convert the object to a dictionary.

        Returns:
            Dictionary representation of the object
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def validate(self):
        """
        Validate the object's attributes.
        Should be overridden by subclasses.

        Raises:
            ValueError: If validation fails
        """
        pass
