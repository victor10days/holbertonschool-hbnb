from typing import List
from .base import BaseModel

class Place(BaseModel):
    """
    Place model.
    NOTE: Marked as abstract temporarily - will be fully mapped in Task 7
    """
    __abstract__ = True  # Temporarily abstract until Task 7

    name: str = ""
    description: str = ""
    price: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    owner_id: str = ""  # User.id
    amenity_ids: List[str] = []  # Amenity.id

    def __init__(self, name: str = "", description: str = "", price: float = 0.0,
                 latitude: float = 0.0, longitude: float = 0.0, owner_id: str = "",
                 amenity_ids: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenity_ids = amenity_ids or []

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

    def to_dict(self) -> dict:
        """Simple to_dict for compatibility"""
        return {
            'id': self.id if hasattr(self, 'id') else '',
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenity_ids': self.amenity_ids,
            'created_at': self.created_at if hasattr(self, 'created_at') else '',
            'updated_at': self.updated_at if hasattr(self, 'updated_at') else ''
        }
