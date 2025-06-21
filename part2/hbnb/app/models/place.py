# This file is the place model, which inherits from BaseModel and represents a place in the application.

from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, name, location, owner_id, amenities=None, reviews=None):
        super().__init__()
        self.name = name
        self.location = location  # string, or dict with lat/lon
        self.owner_id = owner_id
        self.amenities = amenities if amenities is not None else []
        self.reviews = reviews if reviews is not None else []

    def to_dict(self):
        data = super().to_dict()
        return data
