from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description, **kwargs):
        if not name:
            raise ValueError("name is required")
        super().__init__()
        self.name = name
        self.description = description

    def to_dict(self):
        data = super().to_dict()
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }
