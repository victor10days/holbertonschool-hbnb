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

    def to_dict(self):
        data = super().to_dict()
        return {
            'id': self.id,
            'text': self.text,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }
