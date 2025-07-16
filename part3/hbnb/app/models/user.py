import re
from flask_bcrypt import generate_password_hash, check_password_hash
from .base_model import BaseModel

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        if not first_name or not last_name or not email:
            raise ValueError("first_name, last_name, and email are required")
        if not EMAIL_REGEX.match(email):
            raise ValueError("Invalid email format")
        if password and len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._password_hash = None
        
        if password:
            self.set_password(password)

    def set_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self._password_hash = generate_password_hash(password).decode('utf-8')
        self.save()

    def check_password(self, password):
        if not self._password_hash:
            return False
        return check_password_hash(self._password_hash, password)

    def to_dict(self):
        data = super().to_dict()
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }

    def to_dict_safe(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
