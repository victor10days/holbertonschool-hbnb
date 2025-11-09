from app.models.base import BaseModel


class Amenity(BaseModel):
    """
    Amenity model representing a feature available at a place.

    Attributes:
        name (str): Amenity name (required, max 50 characters)
    """

    def __init__(self, name: str):
        """
        Initialize an Amenity instance.

        Args:
            name: Amenity name

        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        """
        Validate amenity attributes.

        Raises:
            ValueError: If validation fails
        """
        # Check required name field
        if not self.name or not isinstance(self.name, str):
            raise ValueError("name is required and must be a string")

        # Check max length
        if len(self.name) > 50:
            raise ValueError("name must not exceed 50 characters")

    def to_dict(self):
        """Convert amenity to dictionary."""
        data = super().to_dict()
        data.update({
            'name': self.name
        })
        return data
