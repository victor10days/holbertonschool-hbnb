from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, user_id, place_id, valid_user_ids, valid_place_ids, **kwargs):
        if not text:
            raise ValueError("text is required")
        if user_id not in valid_user_ids:
            raise ValueError("Invalid user_id")
        if place_id not in valid_place_ids:
            raise ValueError("Invalid place_id")
        
        rating = kwargs.get('rating', 5)
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        
        super().__init__()
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating

    def to_dict(self):
        data = super().to_dict()
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }
