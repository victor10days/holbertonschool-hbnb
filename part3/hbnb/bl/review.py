from dataclasses import dataclass
from .base import BaseModel

@dataclass
class Review(BaseModel):
    text: str = ""
    user_id: str = ""   # User.id
    place_id: str = ""  # Place.id
    rating: int = 0      # optional, 0-5

    def validate(self) -> None:
        if not self.text:
            raise ValueError("text is required")
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.place_id:
            raise ValueError("place_id is required")
        if not (0 <= self.rating <= 5):
            raise ValueError("rating must be 0..5")
