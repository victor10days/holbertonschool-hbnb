from dataclasses import dataclass, field
from .base import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@dataclass
class User(BaseModel):
    email: str = ""
    password: str = ""  # not returned in responses
    first_name: str = ""
    last_name: str = ""
    is_admin: bool = False

    def validate(self) -> None:
        if not self.email or "@" not in self.email:
            raise ValueError("email must be a valid address")
        if not self.password:
            raise ValueError("password is required")
    
    def hash_password(self, password: str):
        """Hash a plaintext password."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        return self.password
    
    def verify_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)
