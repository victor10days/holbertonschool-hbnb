# This file is the review model, which inherits from BaseModel and represents a review in the application.

from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, content, user_id, place_id, rating=None):
        super().__init__()
        self.content = content
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating

    def to_dict(self):
        data = super().to_dict()
        return data
