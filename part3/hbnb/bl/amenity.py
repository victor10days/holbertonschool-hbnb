from .base import BaseModel

class Amenity(BaseModel):
    """
    Amenity model.
    NOTE: Marked as abstract temporarily - will be fully mapped in Task 7
    """
    __abstract__ = True  # Temporarily abstract until Task 7

    name: str = ""

    def __init__(self, name: str = "", **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def validate(self) -> None:
        if not self.name:
            raise ValueError("name is required")

    def to_dict(self) -> dict:
        """Simple to_dict for compatibility"""
        return {
            'id': self.id if hasattr(self, 'id') else '',
            'name': self.name,
            'created_at': self.created_at if hasattr(self, 'created_at') else '',
            'updated_at': self.updated_at if hasattr(self, 'updated_at') else ''
        }
