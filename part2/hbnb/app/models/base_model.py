# This file defines the BaseModel class, which serves as a base for all models in the application.

import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Updates the updated_at timestamp (call before saving to storage)."""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Return a dictionary version for serialization (e.g., JSON)."""
        data = self.__dict__.copy()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
