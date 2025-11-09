from app.models.base import BaseModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.review import Review
    from app.models.amenity import Amenity


class Place(BaseModel):
    """
    Place model representing a rental property.

    Attributes:
        title (str): Place title (required, max 100 characters)
        description (str): Place description (optional)
        price (float): Price per night (positive value)
        latitude (float): Geographic latitude (between -90.0 and 90.0)
        longitude (float): Geographic longitude (between -180.0 and 180.0)
        owner (User): Reference to the owner User instance
        reviews (List[Review]): List of related reviews
        amenities (List[Amenity]): List of related amenities
    """

    def __init__(self, title: str, price: float, latitude: float, longitude: float,
                 owner, description: str = "", owner_id: Optional[str] = None):
        """
        Initialize a Place instance.

        Args:
            title: Place title
            price: Price per night
            latitude: Geographic latitude
            longitude: Geographic longitude
            owner: Owner User instance
            description: Place description (optional)
            owner_id: Owner ID (for backward compatibility)

        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.owner_id = owner.id if owner else owner_id
        self.reviews: List['Review'] = []
        self.amenities: List['Amenity'] = []
        self.validate()

    def validate(self):
        """
        Validate place attributes.

        Raises:
            ValueError: If validation fails
        """
        # Check required fields
        if not self.title or not isinstance(self.title, str):
            raise ValueError("title is required and must be a string")

        # Check max length
        if len(self.title) > 100:
            raise ValueError("title must not exceed 100 characters")

        # Validate description
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string")

        # Validate price
        if not isinstance(self.price, (int, float)):
            raise ValueError("price must be a number")
        if self.price <= 0:
            raise ValueError("price must be a positive value")

        # Validate latitude
        if not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number")
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")

        # Validate longitude
        if not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number")
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")

        # Validate owner exists
        if self.owner is None:
            raise ValueError("owner is required and must be a valid User instance")

    def add_review(self, review: 'Review'):
        """
        Add a review to this place.

        Args:
            review: Review instance to add

        Raises:
            ValueError: If review is invalid
        """
        if review is None:
            raise ValueError("review cannot be None")
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity: 'Amenity'):
        """
        Add an amenity to this place.

        Args:
            amenity: Amenity instance to add

        Raises:
            ValueError: If amenity is invalid
        """
        if amenity is None:
            raise ValueError("amenity cannot be None")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def to_dict(self):
        """Convert place to dictionary."""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'reviews': [review.id for review in self.reviews],
            'amenities': [amenity.id for amenity in self.amenities]
        })
        return data
