# Amenity class for the HBNB application
# This file is the amenity model, which inherits from BaseModel and represents an amenity in the application.

from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description, place_id=None):
        super().__init__()
        self.name = name
        self.description = description
        self.place_id = place_id

    def to_dict(self):
        data = super().to_dict()
        return data
