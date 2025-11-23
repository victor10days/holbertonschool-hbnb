from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel, place_amenity
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .place import Place


class Amenity(BaseModel):
    """
    Amenity model for place amenities.

    Attributes:
        name: Amenity name (e.g., WiFi, Pool, Parking)
        places: List of places that have this amenity (many-to-many)
    """
    __tablename__ = 'amenities'

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    places: Mapped[List["Place"]] = relationship("Place", secondary=place_amenity, back_populates="amenities")

    def __init__(self, name: str = "", **kwargs):
        """
        Initialize Amenity instance.

        Args:
            name: Amenity name
        """
        super().__init__(**kwargs)
        self.name = name

    def validate(self) -> None:
        """Validate amenity data"""
        if not self.name:
            raise ValueError("name is required")
