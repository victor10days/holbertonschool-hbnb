from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, user_id, place_id, valid_user_ids, valid_place_ids, **kwargs):
        if not text:
            raise ValueError("text is required")
        if user_id not in valid_user_ids:
            raise ValueError("Invalid user_id")
        if place_id not in valid_place_ids:
            raise ValueError("Invalid place_id")
        super().__init__()
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        # Handle additional fields if required
