#!/usr/bin/env python3
"""
Comprehensive tests for all model classes.
Tests class definitions, inheritance, validation, relationships, and timestamps.
"""
import unittest
import time
from datetime import datetime
from app.models.base import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class."""

    def test_base_model_creation(self):
        """Test BaseModel instance creation."""
        model = BaseModel()
        self.assertIsNotNone(model.id)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_uuid_uniqueness(self):
        """Test that UUIDs are unique across instances."""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_save_updates_timestamp(self):
        """Test that save() updates the updated_at timestamp."""
        model = BaseModel()
        old_updated_at = model.updated_at
        time.sleep(0.01)
        model.save()
        self.assertGreater(model.updated_at, old_updated_at)

    def test_update_method(self):
        """Test the update method updates attributes and timestamp."""
        model = BaseModel()
        old_updated_at = model.updated_at
        time.sleep(0.01)
        model.update({'test_attr': 'test_value'})
        # updated_at should be updated
        self.assertGreater(model.updated_at, old_updated_at)

    def test_to_dict(self):
        """Test to_dict conversion."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)


class TestUser(unittest.TestCase):
    """Test cases for User class."""

    def test_user_inherits_from_base_model(self):
        """Test that User inherits from BaseModel."""
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        self.assertIsInstance(user, BaseModel)
        self.assertIsNotNone(user.id)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_user_creation_valid(self):
        """Test creating a user with valid data."""
        user = User(
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertFalse(user.is_admin)

    def test_user_is_admin_default(self):
        """Test that is_admin defaults to False."""
        user = User(email="test@example.com", first_name="Test", last_name="User")
        self.assertFalse(user.is_admin)

    def test_user_is_admin_true(self):
        """Test setting is_admin to True."""
        user = User(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            is_admin=True
        )
        self.assertTrue(user.is_admin)

    def test_user_validation_empty_first_name(self):
        """Test validation fails with empty first_name."""
        with self.assertRaises(ValueError) as context:
            User(email="test@example.com", first_name="", last_name="Doe")
        self.assertIn("first_name", str(context.exception))

    def test_user_validation_empty_last_name(self):
        """Test validation fails with empty last_name."""
        with self.assertRaises(ValueError) as context:
            User(email="test@example.com", first_name="John", last_name="")
        self.assertIn("last_name", str(context.exception))

    def test_user_validation_empty_email(self):
        """Test validation fails with empty email."""
        with self.assertRaises(ValueError) as context:
            User(email="", first_name="John", last_name="Doe")
        self.assertIn("email", str(context.exception))

    def test_user_validation_invalid_email_format(self):
        """Test validation fails with invalid email format."""
        with self.assertRaises(ValueError) as context:
            User(email="invalid-email", first_name="John", last_name="Doe")
        self.assertIn("Invalid email format", str(context.exception))

    def test_user_validation_first_name_max_length(self):
        """Test validation fails when first_name exceeds 50 characters."""
        with self.assertRaises(ValueError) as context:
            User(
                email="test@example.com",
                first_name="a" * 51,
                last_name="Doe"
            )
        self.assertIn("50 characters", str(context.exception))

    def test_user_validation_last_name_max_length(self):
        """Test validation fails when last_name exceeds 50 characters."""
        with self.assertRaises(ValueError) as context:
            User(
                email="test@example.com",
                first_name="John",
                last_name="a" * 51
            )
        self.assertIn("50 characters", str(context.exception))

    def test_user_to_dict(self):
        """Test User to_dict includes all attributes."""
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        user_dict = user.to_dict()
        self.assertIn('email', user_dict)
        self.assertIn('first_name', user_dict)
        self.assertIn('last_name', user_dict)
        self.assertIn('is_admin', user_dict)
        self.assertEqual(user_dict['email'], "test@example.com")


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity class."""

    def test_amenity_inherits_from_base_model(self):
        """Test that Amenity inherits from BaseModel."""
        amenity = Amenity(name="WiFi")
        self.assertIsInstance(amenity, BaseModel)

    def test_amenity_creation_valid(self):
        """Test creating an amenity with valid data."""
        amenity = Amenity(name="Swimming Pool")
        self.assertEqual(amenity.name, "Swimming Pool")
        self.assertIsNotNone(amenity.id)

    def test_amenity_validation_empty_name(self):
        """Test validation fails with empty name."""
        with self.assertRaises(ValueError) as context:
            Amenity(name="")
        self.assertIn("name", str(context.exception))

    def test_amenity_validation_name_max_length(self):
        """Test validation fails when name exceeds 50 characters."""
        with self.assertRaises(ValueError) as context:
            Amenity(name="a" * 51)
        self.assertIn("50 characters", str(context.exception))

    def test_amenity_to_dict(self):
        """Test Amenity to_dict includes name."""
        amenity = Amenity(name="WiFi")
        amenity_dict = amenity.to_dict()
        self.assertIn('name', amenity_dict)
        self.assertEqual(amenity_dict['name'], "WiFi")


class TestPlace(unittest.TestCase):
    """Test cases for Place class."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User(email="owner@example.com", first_name="Owner", last_name="User")

    def test_place_inherits_from_base_model(self):
        """Test that Place inherits from BaseModel."""
        place = Place(
            title="Cozy Apartment",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.user
        )
        self.assertIsInstance(place, BaseModel)

    def test_place_creation_valid(self):
        """Test creating a place with valid data."""
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.user
        )
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.description, "A nice place to stay")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        self.assertEqual(place.owner, self.user)
        self.assertEqual(place.owner_id, self.user.id)

    def test_place_validation_empty_title(self):
        """Test validation fails with empty title."""
        with self.assertRaises(ValueError) as context:
            Place(
                title="",
                price=100.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner=self.user
            )
        self.assertIn("title", str(context.exception))

    def test_place_validation_title_max_length(self):
        """Test validation fails when title exceeds 100 characters."""
        with self.assertRaises(ValueError) as context:
            Place(
                title="a" * 101,
                price=100.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner=self.user
            )
        self.assertIn("100 characters", str(context.exception))

    def test_place_validation_negative_price(self):
        """Test validation fails with negative price."""
        with self.assertRaises(ValueError) as context:
            Place(
                title="Test Place",
                price=-10.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner=self.user
            )
        self.assertIn("positive", str(context.exception))

    def test_place_validation_latitude_range(self):
        """Test validation fails with latitude out of range."""
        with self.assertRaises(ValueError) as context:
            Place(
                title="Test Place",
                price=100.0,
                latitude=100.0,
                longitude=-74.0060,
                owner=self.user
            )
        self.assertIn("latitude", str(context.exception))

    def test_place_validation_longitude_range(self):
        """Test validation fails with longitude out of range."""
        with self.assertRaises(ValueError) as context:
            Place(
                title="Test Place",
                price=100.0,
                latitude=40.7128,
                longitude=200.0,
                owner=self.user
            )
        self.assertIn("longitude", str(context.exception))

    def test_place_validation_no_owner(self):
        """Test validation fails without owner."""
        with self.assertRaises(ValueError) as context:
            Place(
                title="Test Place",
                price=100.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner=None
            )
        self.assertIn("owner", str(context.exception))

    def test_place_add_amenity(self):
        """Test adding an amenity to a place."""
        place = Place(
            title="Test Place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.user
        )
        amenity = Amenity(name="WiFi")
        place.add_amenity(amenity)
        self.assertIn(amenity, place.amenities)

    def test_place_add_review(self):
        """Test adding a review to a place."""
        place = Place(
            title="Test Place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.user
        )
        reviewer = User(email="reviewer@example.com", first_name="Rev", last_name="Iewer")
        review = Review(text="Great place!", rating=5, place=place, user=reviewer)
        place.add_review(review)
        self.assertIn(review, place.reviews)


class TestReview(unittest.TestCase):
    """Test cases for Review class."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User(email="owner@example.com", first_name="Owner", last_name="User")
        self.place = Place(
            title="Test Place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.user
        )
        self.reviewer = User(email="reviewer@example.com", first_name="Rev", last_name="Iewer")

    def test_review_inherits_from_base_model(self):
        """Test that Review inherits from BaseModel."""
        review = Review(text="Great!", rating=5, place=self.place, user=self.reviewer)
        self.assertIsInstance(review, BaseModel)

    def test_review_creation_valid(self):
        """Test creating a review with valid data."""
        review = Review(
            text="Excellent place to stay!",
            rating=5,
            place=self.place,
            user=self.reviewer
        )
        self.assertEqual(review.text, "Excellent place to stay!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.reviewer)
        self.assertEqual(review.place_id, self.place.id)
        self.assertEqual(review.user_id, self.reviewer.id)

    def test_review_validation_empty_text(self):
        """Test validation fails with empty text."""
        with self.assertRaises(ValueError) as context:
            Review(text="", rating=5, place=self.place, user=self.reviewer)
        self.assertIn("text", str(context.exception))

    def test_review_validation_rating_too_low(self):
        """Test validation fails with rating below 1."""
        with self.assertRaises(ValueError) as context:
            Review(text="Bad", rating=0, place=self.place, user=self.reviewer)
        self.assertIn("rating", str(context.exception))

    def test_review_validation_rating_too_high(self):
        """Test validation fails with rating above 5."""
        with self.assertRaises(ValueError) as context:
            Review(text="Great", rating=6, place=self.place, user=self.reviewer)
        self.assertIn("rating", str(context.exception))

    def test_review_validation_no_place(self):
        """Test validation fails without place."""
        with self.assertRaises(ValueError) as context:
            Review(text="Good", rating=5, place=None, user=self.reviewer)
        self.assertIn("place", str(context.exception))

    def test_review_validation_no_user(self):
        """Test validation fails without user."""
        with self.assertRaises(ValueError) as context:
            Review(text="Good", rating=5, place=self.place, user=None)
        self.assertIn("user", str(context.exception))


class TestRelationships(unittest.TestCase):
    """Test relationships between entities."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = User(email="owner@example.com", first_name="Owner", last_name="User")
        self.place = Place(
            title="Test Place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.owner
        )

    def test_place_has_owner_reference(self):
        """Test that place has owner reference."""
        self.assertEqual(self.place.owner, self.owner)
        self.assertEqual(self.place.owner_id, self.owner.id)

    def test_place_manages_reviews_collection(self):
        """Test that place manages reviews collection."""
        reviewer = User(email="reviewer@example.com", first_name="Rev", last_name="Iewer")
        review = Review(text="Great!", rating=5, place=self.place, user=reviewer)
        self.place.add_review(review)
        self.assertEqual(len(self.place.reviews), 1)
        self.assertIn(review, self.place.reviews)

    def test_place_manages_amenities_collection(self):
        """Test that place manages amenities collection."""
        wifi = Amenity(name="WiFi")
        pool = Amenity(name="Pool")
        self.place.add_amenity(wifi)
        self.place.add_amenity(pool)
        self.assertEqual(len(self.place.amenities), 2)
        self.assertIn(wifi, self.place.amenities)
        self.assertIn(pool, self.place.amenities)

    def test_review_references_user_and_place(self):
        """Test that review references both user and place."""
        reviewer = User(email="reviewer@example.com", first_name="Rev", last_name="Iewer")
        review = Review(text="Nice!", rating=4, place=self.place, user=reviewer)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, reviewer)
        self.assertEqual(review.place_id, self.place.id)
        self.assertEqual(review.user_id, reviewer.id)


if __name__ == '__main__':
    unittest.main()
