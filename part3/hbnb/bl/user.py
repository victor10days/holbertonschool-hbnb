from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(BaseModel):
    """
    User model for authentication and user management.

    Attributes:
        email: User's email address (unique)
        password: Hashed password
        first_name: User's first name
        last_name: User's last name
        is_admin: Whether user has admin privileges
    """
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __init__(self, email: str = "", password: str = "", first_name: str = "",
                 last_name: str = "", is_admin: bool = False, **kwargs):
        """
        Initialize User instance.

        Args:
            email: User's email address
            password: User's password (will be hashed)
            first_name: User's first name
            last_name: User's last name
            is_admin: Whether user has admin privileges
        """
        super().__init__(**kwargs)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def validate(self) -> None:
        """Validate user data"""
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
