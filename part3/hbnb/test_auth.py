#!/usr/bin/env python3
"""
Test script for JWT authentication functionality
"""

import json
from app import create_app

def test_auth_system():
    """Test the authentication system"""
    app = create_app('development')
    
    with app.test_client() as client:
        print("Testing JWT Authentication System...")
        
        # Test 1: Register a new user
        print("\n1. Testing user registration:")
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'securepassword123'
        }
        
        response = client.post('/api/v1/auth/register', 
                             json=user_data,
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 2: Register an admin user
        print("\n2. Testing admin user registration:")
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@example.com',
            'password': 'adminpassword123',
            'is_admin': True
        }
        
        response = client.post('/api/v1/auth/register', 
                             json=admin_data,
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 3: Login with correct credentials
        print("\n3. Testing login with correct credentials:")
        login_data = {
            'email': 'john@example.com',
            'password': 'securepassword123'
        }
        
        response = client.post('/api/v1/auth/login', 
                             json=login_data,
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        result = response.get_json()
        print(f"   Response: {result}")
        
        # Store token for further tests
        token = result.get('access_token') if result else None
        
        # Test 4: Login with incorrect credentials
        print("\n4. Testing login with incorrect credentials:")
        wrong_login_data = {
            'email': 'john@example.com',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/v1/auth/login', 
                             json=wrong_login_data,
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 5: Access protected endpoint without token
        print("\n5. Testing protected endpoint without token:")
        response = client.get('/api/v1/auth/protected')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        # Test 6: Access protected endpoint with token
        if token:
            print("\n6. Testing protected endpoint with token:")
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get('/api/v1/auth/protected', headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.get_json()}")
            
            # Test 7: Get current user information
            print("\n7. Testing current user endpoint:")
            response = client.get('/api/v1/auth/me', headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.get_json()}")
            
            # Test 8: Logout user
            print("\n8. Testing logout:")
            response = client.post('/api/v1/auth/logout', headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.get_json()}")
            
            # Test 9: Access protected endpoint after logout
            print("\n9. Testing protected endpoint after logout:")
            response = client.get('/api/v1/auth/protected', headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.get_json()}")
        
        # Test 10: Registration validation
        print("\n10. Testing registration validation:")
        invalid_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',
            'password': 'short'
        }
        
        response = client.post('/api/v1/auth/register', 
                             json=invalid_data,
                             content_type='application/json')
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        print("\nAuthentication tests completed!")

if __name__ == '__main__':
    test_auth_system()