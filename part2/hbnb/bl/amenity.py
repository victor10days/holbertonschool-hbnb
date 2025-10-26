from dataclasses import dataclass
from .base import BaseModel

@dataclass
class Amenity(BaseModel):
    name: str = ""

    def validate(self) -> None:
        if not self.name:
            raise ValueError("name is required")
