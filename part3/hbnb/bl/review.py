from .base import BaseModel

class Review(BaseModel):
    """
    Review model.
    NOTE: Marked as abstract temporarily - will be fully mapped in Task 7
    """
    __abstract__ = True  # Temporarily abstract until Task 7

    text: str = ""
    user_id: str = ""   # User.id
    place_id: str = ""  # Place.id
    rating: int = 0      # optional, 0-5

    def __init__(self, text: str = "", user_id: str = "", place_id: str = "",
                 rating: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating

    def validate(self) -> None:
        if not self.text:
            raise ValueError("text is required")
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.place_id:
            raise ValueError("place_id is required")
        if not (0 <= self.rating <= 5):
            raise ValueError("rating must be 0..5")

    def to_dict(self) -> dict:
        """Simple to_dict for compatibility"""
        return {
            'id': self.id if hasattr(self, 'id') else '',
            'text': self.text,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'rating': self.rating,
            'created_at': self.created_at if hasattr(self, 'created_at') else '',
            'updated_at': self.updated_at if hasattr(self, 'updated_at') else ''
        }
