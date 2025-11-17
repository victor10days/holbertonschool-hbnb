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
        description: Amenity description
        places: List of places that have this amenity (many-to-many)
    """
    __tablename__ = 'amenities'

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True, default="")

    # Relationships
    places: Mapped[List["Place"]] = relationship("Place", secondary=place_amenity, back_populates="amenities")

    def __init__(self, name: str = "", description: str = "", **kwargs):
        """
        Initialize Amenity instance.

        Args:
            name: Amenity name
            description: Amenity description
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description

    def validate(self) -> None:
        """Validate amenity data"""
        if not self.name:
            raise ValueError("name is required")
