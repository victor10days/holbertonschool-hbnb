from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class Amenity(BaseModel):
    """
    Amenity model for place amenities.

    Attributes:
        name: Amenity name (e.g., WiFi, Pool, Parking)
    """
    __tablename__ = 'amenities'

    name: Mapped[str] = mapped_column(String(50), nullable=False)

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
