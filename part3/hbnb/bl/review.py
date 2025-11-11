from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .place import Place


class Review(BaseModel):
    """
    Review model for place reviews.

    Attributes:
        text: Review text content
        user_id: User ID of the reviewer (foreign key)
        place_id: Place ID being reviewed (foreign key)
        rating: Rating from 0 to 5
        user: User who wrote this review (many-to-one)
        place: Place being reviewed (many-to-one)
    """
    __tablename__ = 'reviews'

    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)
    place_id: Mapped[str] = mapped_column(String(60), ForeignKey('places.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    place: Mapped["Place"] = relationship("Place", back_populates="reviews")

    def __init__(self, text: str = "", user_id: str = "", place_id: str = "",
                 rating: int = 0, **kwargs):
        """
        Initialize Review instance.

        Args:
            text: Review text content
            user_id: User ID of the reviewer
            place_id: Place ID being reviewed
            rating: Rating from 0 to 5
        """
        super().__init__(**kwargs)
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating

    def validate(self) -> None:
        """Validate review data"""
        if not self.text:
            raise ValueError("text is required")
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.place_id:
            raise ValueError("place_id is required")
        if not (0 <= self.rating <= 5):
            raise ValueError("rating must be 0..5")
