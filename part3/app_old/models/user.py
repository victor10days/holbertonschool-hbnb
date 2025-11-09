import re
from app.models.base import BaseModel


class User(BaseModel):
    """
    User model representing a user in the system.

    Attributes:
        first_name (str): User's first name (required, max 50 characters)
        last_name (str): User's last name (required, max 50 characters)
        email (str): User's email address (required, unique, valid format)
        is_admin (bool): Admin status (defaults to False)
    """

    def __init__(self, email: str, first_name: str, last_name: str, is_admin: bool = False):
        """
        Initialize a User instance.

        Args:
            email: User's email address
            first_name: User's first name
            last_name: User's last name
            is_admin: Admin status (defaults to False)

        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.validate()

    def validate(self):
        """
        Validate user attributes.

        Raises:
            ValueError: If validation fails
        """
        # Check required fields
        if not self.first_name or not isinstance(self.first_name, str):
            raise ValueError("first_name is required and must be a string")
        if not self.last_name or not isinstance(self.last_name, str):
            raise ValueError("last_name is required and must be a string")
        if not self.email or not isinstance(self.email, str):
            raise ValueError("email is required and must be a string")

        # Check max length
        if len(self.first_name) > 50:
            raise ValueError("first_name must not exceed 50 characters")
        if len(self.last_name) > 50:
            raise ValueError("last_name must not exceed 50 characters")

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")

        # Validate is_admin is boolean
        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")

    def to_dict(self):
        """Convert user to dictionary."""
        data = super().to_dict()
        data.update({
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin
        })
        return data
