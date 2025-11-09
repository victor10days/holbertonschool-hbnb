"""
User Repository - Specialized repository for User operations.
Extends SQLAlchemyRepository with user-specific query methods.
"""
from typing import Optional
from hbnb.persistence.sqlalchemy_repo import SQLAlchemyRepository
from hbnb.bl.user import User


class UserRepository(SQLAlchemyRepository):
    """
    User-specific repository with additional query methods.

    Provides specialized methods for user operations such as
    finding users by email (needed for authentication).
    """

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Find a user by their email address.

        Args:
            email: The email address to search for

        Returns:
            User object if found, None otherwise
        """
        return self._session.query(User).filter_by(email=email).first()
