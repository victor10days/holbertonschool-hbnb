from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

def now_iso() -> str:
    return datetime.utcnow().strftime(ISO)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base"""
    pass


# Association table for many-to-many relationship between Place and Amenity
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
)


class BaseModel(Base):
    """
    Base model for all entities.
    Provides common attributes: id, created_at, updated_at
    """
    __abstract__ = True  # Don't create a table for BaseModel itself

    # Primary key
    id: Mapped[str] = mapped_column(
        String(60),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def to_dict(self) -> dict:
        """Convert model instance to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # Convert datetime objects to ISO format strings
            if isinstance(value, datetime):
                result[column.name] = value.strftime(ISO)
            else:
                result[column.name] = value
        return result

    def touch(self) -> None:
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
