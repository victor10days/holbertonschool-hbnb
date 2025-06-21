# This file is the user model, which inherits from BaseModel and represents a user in the application.

from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, name, email, password):
        super().__init__()
        self.name = name
        self.email = email
        self.password = password  # Should be hashed in a real app

    def to_dict(self):
        data = super().to_dict()
        data.pop('password', None)  # Hide password for security
        return data
