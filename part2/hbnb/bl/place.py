from dataclasses import dataclass, field
from typing import List
from .base import BaseModel

@dataclass
class Place(BaseModel):
    name: str = ""
    description: str = ""
    price: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    owner_id: str = ""  # User.id
    amenity_ids: List[str] = field(default_factory=list)  # Amenity.id

    def validate(self) -> None:
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
