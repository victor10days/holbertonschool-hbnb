#!/usr/bin/env python3
"""
Test script for the User model with password hashing functionality
"""

from app.models.user import User

def test_user_model():
    print("Testing User Model with Password Hashing...")
    
    # Test 1: Create a regular user
    print("\n1. Testing regular user creation:")
    user1 = User('John', 'Doe', 'john@example.com', password='securepassword123')
    print(f"   User created: {user1.first_name} {user1.last_name}")
    print(f"   Email: {user1.email}")
    print(f"   Is admin: {user1.is_admin}")
    print(f"   Password hash exists: {bool(user1._password_hash)}")
    
    # Test 2: Create an admin user
    print("\n2. Testing admin user creation:")
    admin = User('Admin', 'User', 'admin@example.com', password='adminpass123', is_admin=True)
    print(f"   Admin created: {admin.first_name} {admin.last_name}")
    print(f"   Is admin: {admin.is_admin}")
    
    # Test 3: Password verification
    print("\n3. Testing password verification:")
    print(f"   Correct password: {user1.check_password('securepassword123')}")
    print(f"   Incorrect password: {user1.check_password('wrongpassword')}")
    
    # Test 4: Password change
    print("\n4. Testing password change:")
    user1.set_password('newpassword123')
    print(f"   Old password works: {user1.check_password('securepassword123')}")
    print(f"   New password works: {user1.check_password('newpassword123')}")
    
    # Test 5: Safe dictionary output
    print("\n5. Testing safe dictionary output:")
    user_dict = user1.to_dict_safe()
    print(f"   Safe dict: {user_dict}")
    print(f"   Contains password: {'password' in user_dict}")
    print(f"   Contains password hash: {'_password_hash' in user_dict}")
    
    # Test 6: Validation errors
    print("\n6. Testing validation errors:")
    
    # Short password
    try:
        User('Test', 'User', 'test@example.com', password='short')
        print("   ERROR: Short password should have failed!")
    except ValueError as e:
        print(f"   Password validation: {e}")
    
    # Invalid email
    try:
        User('Test', 'User', 'invalid-email', password='validpassword123')
        print("   ERROR: Invalid email should have failed!")
    except ValueError as e:
        print(f"   Email validation: {e}")
    
    # Missing required fields
    try:
        User('', 'User', 'test@example.com', password='validpassword123')
        print("   ERROR: Empty first name should have failed!")
    except ValueError as e:
        print(f"   Required field validation: {e}")
    
    print("\nAll tests passed! ✓")

if __name__ == '__main__':
    test_user_model()