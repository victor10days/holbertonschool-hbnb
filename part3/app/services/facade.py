from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Facade pattern implementation for HBnB application.
    Uses singleton pattern to ensure all endpoints share the same repositories.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HBnBFacade, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if HBnBFacade._initialized:
            return
        HBnBFacade._initialized = True

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


    # User operations
    def create_user(self, user_data: dict):
        """
        Create a new user.

        Args:
            user_data: Dictionary with user data (email, first_name, last_name, is_admin)

        Returns:
            Created User instance

        Raises:
            ValueError: If validation fails or email already exists
        """
        user = User(
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            is_admin=user_data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: dict):
        """
        Update a user.

        Args:
            user_id: User ID
            user_data: Dictionary with fields to update

        Returns:
            Updated User instance or None if not found

        Raises:
            ValueError: If validation fails
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Update allowed fields only
        for key in ['first_name', 'last_name', 'email']:
            if key in user_data:
                setattr(user, key, user_data[key])

        # Validate updated user
        user.validate()
        user.save()

        return user

    def delete_user(self, user_id: str):
        """Delete a user."""
        return self.user_repo.delete(user_id)

    # Place operations
    def create_place(self, place_data: dict):
        """
        Create a new place.

        Args:
            place_data: Dictionary with place data

        Returns:
            Created Place instance

        Raises:
            ValueError: If validation fails or related entities don't exist
        """
        # Validate owner exists
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} not found")

        # Validate amenities exist
        amenity_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            amenities.append(amenity)

        # Create place
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner=owner
        )

        # Add amenities
        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id: str, place_data: dict):
        """
        Update a place.

        Args:
            place_id: Place ID
            place_data: Dictionary with fields to update

        Returns:
            Updated Place instance or None if not found

        Raises:
            ValueError: If validation fails
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Update allowed fields
        for key in ['title', 'description', 'price', 'latitude', 'longitude']:
            if key in place_data:
                setattr(place, key, place_data[key])

        # Validate updated place
        place.validate()
        place.save()

        return place

    def delete_place(self, place_id: str):
        """Delete a place."""
        if not self.place_repo.get(place_id):
            raise NotFoundError()
        self.repo.delete(Place, place_id)
        return self.place_repo.delete(place_id)

    # Review operations
    def create_review(self, review_data: dict):
        """
        Create a new review.

        Args:
            review_data: Dictionary with review data

        Returns:
            Created Review instance

        Raises:
            ValueError: If validation fails or related entities don't exist
        """
        # Validate user exists
        user_id = review_data.get('user_id')
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Validate place exists
        place_id = review_data.get('place_id')
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")

        # Create review
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,
            user=user
        )

        # Add review to place
        place.add_review(review)

        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str):
        """Retrieve all reviews for a specific place."""
        return [review for review in self.review_repo.get_all()
                if hasattr(review, 'place_id') and review.place_id == place_id]

    def update_review(self, review_id: str, review_data: dict):
        """
        Update a review.

        Args:
            review_id: Review ID
            review_data: Dictionary with fields to update

        Returns:
            Updated Review instance or None if not found

        Raises:
            ValueError: If validation fails
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Update allowed fields
        for key in ['text', 'rating']:
            if key in review_data:
                setattr(review, key, review_data[key])

        # Validate updated review
        review.validate()
        review.save()

        return review

    def delete_review(self, review_id: str):
        """Delete a review."""
        return self.review_repo.delete(review_id)

    # Amenity operations
    def create_amenity(self, amenity_data: dict):
        """
        Create a new amenity.

        Args:
            amenity_data: Dictionary with amenity data (name)

        Returns:
            Created Amenity instance

        Raises:
            ValueError: If validation fails
        """
        amenity = Amenity(name=amenity_data.get('name'))
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: dict):
        """
        Update an amenity.

        Args:
            amenity_id: Amenity ID
            amenity_data: Dictionary with fields to update

        Returns:
            Updated Amenity instance or None if not found

        Raises:
            ValueError: If validation fails
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        # Update name if provided
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']

        # Validate updated amenity
        amenity.validate()
        amenity.save()

        return amenity

    def delete_amenity(self, amenity_id: str):
        """Delete an amenity."""
        return self.amenity_repo.delete(amenity_id)

