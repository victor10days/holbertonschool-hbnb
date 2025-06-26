import re
from .base_model import BaseModel

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class User(BaseModel):
    def __init__(self, first_name, last_name, email, **kwargs):
        if not first_name or not last_name or not email:
            raise ValueError("first_name, last_name, and email are required")
        if not EMAIL_REGEX.match(email):
            raise ValueError("Invalid email format")
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def to_dict(self):
        data = super().to_dict()
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }
