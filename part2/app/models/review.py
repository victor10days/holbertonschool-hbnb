from app.models.base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.place import Place


class Review(BaseModel):
    """
    Review model representing a user review of a place.

    Attributes:
        text (str): Review text content (required)
        rating (int): Rating value (between 1 and 5)
        place (Place): Reference to the Place instance being reviewed
        user (User): Reference to the User instance who wrote the review
    """

    def __init__(self, text: str, rating: int, place: 'Place', user: 'User'):
        """
        Initialize a Review instance.

        Args:
            text: Review text content
            rating: Rating value (1-5)
            place: Place instance being reviewed
            user: User instance writing the review

        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.place_id = place.id if place else None
        self.user_id = user.id if user else None
        self.validate()

    def validate(self):
        """
        Validate review attributes.

        Raises:
            ValueError: If validation fails
        """
        # Check required text field
        if not self.text or not isinstance(self.text, str):
            raise ValueError("text is required and must be a string")

        # Validate rating
        if not isinstance(self.rating, int):
            raise ValueError("rating must be an integer")
        if not 1 <= self.rating <= 5:
            raise ValueError("rating must be between 1 and 5")

        # Validate place exists and is valid
        if self.place is None:
            raise ValueError("place is required and must be a valid Place instance")

        # Validate user exists and is valid
        if self.user is None:
            raise ValueError("user is required and must be a valid User instance")

    def to_dict(self):
        """Convert review to dictionary."""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        })
        return data
