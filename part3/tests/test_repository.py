#!/usr/bin/env python3
"""
Tests for Repository and InMemoryRepository classes.
"""
import unittest
from app.persistence.repository import Repository, InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class TestInMemoryRepository(unittest.TestCase):
    """Test cases for InMemoryRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo = InMemoryRepository()

    def test_add_and_get(self):
        """Test adding and retrieving objects."""
        user = User(email="test@example.com", first_name="Test", last_name="User")
        self.repo.add(user)
        retrieved = self.repo.get(user.id)
        self.assertEqual(retrieved, user)

    def test_get_all(self):
        """Test retrieving all objects."""
        user1 = User(email="user1@example.com", first_name="User", last_name="One")
        user2 = User(email="user2@example.com", first_name="User", last_name="Two")
        self.repo.add(user1)
        self.repo.add(user2)
        all_users = self.repo.get_all()
        self.assertEqual(len(all_users), 2)
        self.assertIn(user1, all_users)
        self.assertIn(user2, all_users)

    def test_update(self):
        """Test updating an object."""
        user = User(email="test@example.com", first_name="Test", last_name="User")
        self.repo.add(user)
        self.repo.update(user.id, {'first_name': 'Updated'})
        updated_user = self.repo.get(user.id)
        self.assertEqual(updated_user.first_name, 'Updated')

    def test_delete(self):
        """Test deleting an object."""
        user = User(email="test@example.com", first_name="Test", last_name="User")
        self.repo.add(user)
        result = self.repo.delete(user.id)
        self.assertTrue(result)
        self.assertIsNone(self.repo.get(user.id))

    def test_delete_nonexistent(self):
        """Test deleting a nonexistent object."""
        result = self.repo.delete("nonexistent-id")
        self.assertFalse(result)

    def test_get_by_attribute(self):
        """Test retrieving by attribute."""
        user = User(email="test@example.com", first_name="Test", last_name="User")
        self.repo.add(user)
        retrieved = self.repo.get_by_attribute('email', 'test@example.com')
        self.assertEqual(retrieved, user)

    def test_email_uniqueness_enforced(self):
        """Test that email uniqueness is enforced."""
        user1 = User(email="test@example.com", first_name="User", last_name="One")
        self.repo.add(user1)

        # Try to add another user with same email
        user2 = User(email="test@example.com", first_name="User", last_name="Two")
        with self.assertRaises(ValueError) as context:
            self.repo.add(user2)
        self.assertIn("already exists", str(context.exception))

    def test_different_emails_allowed(self):
        """Test that different emails are allowed."""
        user1 = User(email="user1@example.com", first_name="User", last_name="One")
        user2 = User(email="user2@example.com", first_name="User", last_name="Two")
        self.repo.add(user1)
        self.repo.add(user2)  # Should not raise
        self.assertEqual(len(self.repo.get_all()), 2)

    def test_non_user_objects_no_email_check(self):
        """Test that non-user objects don't trigger email check."""
        amenity1 = Amenity(name="WiFi")
        amenity2 = Amenity(name="Pool")
        self.repo.add(amenity1)
        self.repo.add(amenity2)  # Should not raise
        self.assertEqual(len(self.repo.get_all()), 2)


if __name__ == '__main__':
    unittest.main()
