#!/usr/bin/env python3
"""
Script to create test places in the database
"""
from app import create_app, db
from hbnb.bl.place import Place
from hbnb.bl.user import User

def create_test_places():
    """Create test places for testing the frontend"""
    app = create_app()

    with app.app_context():
        # Get the test user
        user = db.session.query(User).filter_by(email='test@example.com').first()

        if not user:
            print("Test user not found! Please create a test user first.")
            return

        # Check existing places
        existing_count = db.session.query(Place).count()
        print(f"Current places in database: {existing_count}")

        # Test places data
        test_places = [
            {
                'name': 'Beach House',
                'description': 'Beautiful beach house with ocean view',
                'price': 250.0,
                'latitude': 34.0522,
                'longitude': -118.2437,
                'owner_id': user.id
            },
            {
                'name': 'Mountain Cabin',
                'description': 'Cozy cabin in the mountains',
                'price': 80.0,
                'latitude': 39.7392,
                'longitude': -104.9903,
                'owner_id': user.id
            },
            {
                'name': 'City Loft',
                'description': 'Modern loft in downtown',
                'price': 150.0,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': user.id
            },
            {
                'name': 'Country Cottage',
                'description': 'Peaceful cottage in the countryside',
                'price': 45.0,
                'latitude': 51.5074,
                'longitude': -0.1278,
                'owner_id': user.id
            },
            {
                'name': 'Luxury Villa',
                'description': 'Stunning villa with pool and garden',
                'price': 500.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': user.id
            }
        ]

        created = 0
        for place_data in test_places:
            # Check if place with same name exists
            existing = db.session.query(Place).filter_by(name=place_data['name']).first()
            if not existing:
                place = Place(**place_data)
                db.session.add(place)
                created += 1
                print(f"Created: {place_data['name']} - ${place_data['price']}")
            else:
                print(f"Skipped (exists): {place_data['name']}")

        db.session.commit()

        total = db.session.query(Place).count()
        print(f"\n✓ Created {created} new places")
        print(f"✓ Total places in database: {total}")

if __name__ == '__main__':
    create_test_places()
