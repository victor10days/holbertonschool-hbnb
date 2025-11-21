#!/usr/bin/env python3
"""
Script to create a test user in the database
"""
from app import create_app, db
from hbnb.bl.user import User

def create_test_user():
    """Create a test user for login testing"""
    app = create_app()

    with app.app_context():
        # Check if user already exists
        existing_user = db.session.query(User).filter_by(email='test@example.com').first()

        if existing_user:
            print("Test user already exists!")
            print(f"Email: {existing_user.email}")
            print(f"Name: {existing_user.first_name} {existing_user.last_name}")
            return

        # Create new user
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            is_admin=False
        )

        # Hash the password
        user.hash_password('password123')

        # Add to database
        db.session.add(user)
        db.session.commit()

        print("Test user created successfully!")
        print(f"Email: {user.email}")
        print(f"Password: password123")
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"User ID: {user.id}")

if __name__ == '__main__':
    create_test_user()
