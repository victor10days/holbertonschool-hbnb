from typing import List, TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, place_amenity
import json

if TYPE_CHECKING:
    from .user import User
    from .review import Review
    from .amenity import Amenity


class Place(BaseModel):
    """
    Place model for rental properties.

    Attributes:
        name: Place name
        description: Place description
        price: Price per night
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        owner_id: User ID of the owner (foreign key)
        owner: User who owns this place (many-to-one)
        reviews: List of reviews for this place (one-to-many)
        amenities: List of amenities for this place (many-to-many)
    """
    __tablename__ = 'places'

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    owner_id: Mapped[str] = mapped_column(String(60), ForeignKey('users.id'), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="places")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities: Mapped[List["Amenity"]] = relationship("Amenity", secondary=place_amenity, back_populates="places")

    # Store amenity_ids as JSON text for backward compatibility
    _amenity_ids_json: Mapped[str] = mapped_column('amenity_ids', Text, default='[]', nullable=False)

    def __init__(self, name: str = "", description: str = "", price: float = 0.0,
                 latitude: float = 0.0, longitude: float = 0.0, owner_id: str = "",
                 amenity_ids: List[str] = None, **kwargs):
        """
        Initialize Place instance.

        Args:
            name: Place name
            description: Place description
            price: Price per night
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            owner_id: User ID of the owner
            amenity_ids: List of amenity IDs
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = amenity_ids or []

    @property
    def amenity_ids(self) -> List[str]:
        """Get amenity_ids from JSON storage"""
        try:
            return json.loads(self._amenity_ids_json) if self._amenity_ids_json else []
        except (json.JSONDecodeError, AttributeError):
            return []

    @amenity_ids.setter
    def amenity_ids(self, value: List[str]):
        """Set amenity_ids to JSON storage"""
        self._amenity_ids_json = json.dumps(value if value else [])

    def validate(self) -> None:
        """Validate place data"""
        if not self.name:
            raise ValueError("name is required")
        if self.price < 0:
            raise ValueError("price must be >= 0")
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("latitude must be in [-90,90]")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("longitude must be in [-180,180]")
        if not self.owner_id:
            raise ValueError("owner_id is required")
