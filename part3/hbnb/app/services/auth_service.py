"""
Authentication service for handling user authentication and JWT token management
"""

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.services.facade import HBnBFacade


class AuthService:
    def __init__(self):
        self.facade = HBnBFacade()
    
    def register_user(self, user_data):
        """
        Register a new user with the provided data
        
        Args:
            user_data (dict): User registration data containing:
                - first_name (str): User's first name
                - last_name (str): User's last name  
                - email (str): User's email address
                - password (str): User's password
                - is_admin (bool, optional): Whether user is admin
        
        Returns:
            dict: Success message and user data, or error message
        """
        try:
            # Check if user already exists
            existing_users = self.facade.get_all_users()
            for user in existing_users:
                if user.email == user_data['email']:
                    return {
                        'error': 'User with this email already exists',
                        'status_code': 400
                    }
            
            # Create new user
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password'],
                is_admin=user_data.get('is_admin', False)
            )
            
            # Save user using facade
            self.facade.create_user(user)
            
            return {
                'message': 'User registered successfully',
                'user': user.to_dict_safe(),
                'status_code': 201
            }
            
        except ValueError as e:
            return {
                'error': str(e),
                'status_code': 400
            }
        except Exception as e:
            return {
                'error': 'Internal server error',
                'status_code': 500
            }
    
    def login_user(self, email, password):
        """
        Authenticate user and generate access token
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            dict: Access token and user data, or error message
        """
        try:
            # Find user by email
            users = self.facade.get_all_users()
            user = None
            for u in users:
                if u.email == email:
                    user = u
                    break
            
            if not user:
                return {
                    'error': 'Invalid email or password',
                    'status_code': 401
                }
            
            # Verify password
            if not user.check_password(password):
                return {
                    'error': 'Invalid email or password',
                    'status_code': 401
                }
            
            # Generate access token
            access_token = create_access_token(
                identity=user.id,
                additional_claims={
                    'is_admin': user.is_admin,
                    'email': user.email
                }
            )
            
            return {
                'access_token': access_token,
                'user': user.to_dict_safe(),
                'status_code': 200
            }
            
        except Exception as e:
            return {
                'error': 'Internal server error',
                'status_code': 500
            }
    
    def get_current_user(self):
        """
        Get current authenticated user from JWT token
        
        Returns:
            User: Current user object or None if not found
        """
        try:
            current_user_id = get_jwt_identity()
            if not current_user_id:
                return None
            
            # Find user by ID
            users = self.facade.get_all_users()
            for user in users:
                if user.id == current_user_id:
                    return user
            
            return None
            
        except Exception:
            return None
    
    def is_admin(self, user_id):
        """
        Check if a user is an admin
        
        Args:
            user_id (str): User ID to check
            
        Returns:
            bool: True if user is admin, False otherwise
        """
        try:
            user = self.facade.get_user(user_id)
            return user.is_admin if user else False
        except Exception:
            return False
    
    def get_user_by_email(self, email):
        """
        Get user by email address
        
        Args:
            email (str): Email address to search for
            
        Returns:
            User: User object or None if not found
        """
        try:
            users = self.facade.get_all_users()
            for user in users:
                if user.email == email:
                    return user
            return None
        except Exception:
            return None