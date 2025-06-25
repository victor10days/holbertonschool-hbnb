# This file is the user model, which inherits from BaseModel and represents a user in the application.

import re
from .base_model import BaseModel

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class User(BaseModel):
    def __init__(self, name, email, password):
        if not name or not email:
            raise ValueError("Name and email are required")
        if not EMAIL_REGEX.match(email):
            raise ValueError("Invalid email format")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        super().__init__()
        self.name = name
        self.email = email
        self.password = password  # Should be hashed in a real app

    def to_dict(self):
        data = super().to_dict()
        data.pop('password', None)  # Hide password for security
        return data
