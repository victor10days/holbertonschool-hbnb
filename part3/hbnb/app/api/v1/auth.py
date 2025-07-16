"""
Authentication endpoints for user registration, login, and logout
"""

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import AuthService

# Create namespace for authentication
ns = Namespace('auth', description='Authentication operations')

# Define data models for Swagger documentation
user_registration_model = ns.model('UserRegistration', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password (minimum 6 characters)'),
    'is_admin': fields.Boolean(required=False, description='Admin flag (default: False)')
})

user_login_model = ns.model('UserLogin', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

user_response_model = ns.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address'),
    'is_admin': fields.Boolean(description='Admin flag')
})

auth_response_model = ns.model('AuthResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Nested(user_response_model, description='User information')
})

# Initialize authentication service
auth_service = AuthService()

# Create a simple in-memory blacklist for demonstration
# In production, you'd use Redis or a database
jwt_blacklist = set()

@ns.route('/register')
class UserRegistration(Resource):
    @ns.expect(user_registration_model)
    @ns.doc('register_user')
    def post(self):
        """Register a new user"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'{field} is required'}, 400
            
            # Register user
            result = auth_service.register_user(data)
            return result, result.get('status_code', 500)
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@ns.route('/login')
class UserLogin(Resource):
    @ns.expect(user_login_model)
    @ns.doc('login_user')
    def post(self):
        """Authenticate user and get access token"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not data.get('email') or not data.get('password'):
                return {'error': 'Email and password are required'}, 400
            
            # Login user
            result = auth_service.login_user(data['email'], data['password'])
            return result, result.get('status_code', 500)
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@ns.route('/logout')
class UserLogout(Resource):
    @ns.doc('logout_user')
    @jwt_required()
    def post(self):
        """Logout user and invalidate token"""
        try:
            # Get the JWT token identifier
            jti = get_jwt()['jti']
            
            # Add token to blacklist
            jwt_blacklist.add(jti)
            
            return {'message': 'User logged out successfully'}, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@ns.route('/me')
class CurrentUser(Resource):
    @ns.doc('get_current_user')
    @jwt_required()
    def get(self):
        """Get current authenticated user information"""
        try:
            # Check if token is blacklisted
            jti = get_jwt()['jti']
            if jti in jwt_blacklist:
                return {'error': 'Token has been revoked'}, 401
            
            # Get current user
            current_user = auth_service.get_current_user()
            if not current_user:
                return {'error': 'User not found'}, 404
            
            return current_user.to_dict_safe(), 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

@ns.route('/protected')
class ProtectedResource(Resource):
    @ns.doc('protected_endpoint')
    @jwt_required()
    def get(self):
        """Example protected endpoint"""
        try:
            # Check if token is blacklisted
            jti = get_jwt()['jti']
            if jti in jwt_blacklist:
                return {'error': 'Token has been revoked'}, 401
            
            current_user_id = get_jwt_identity()
            current_user = auth_service.get_current_user()
            
            return {
                'message': 'Access granted to protected resource',
                'user_id': current_user_id,
                'user': current_user.to_dict_safe() if current_user else None
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500