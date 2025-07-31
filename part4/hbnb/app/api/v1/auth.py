from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import get_facade
import jwt
import datetime

ns = Namespace('auth', description='Authentication operations')

login_model = ns.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

register_model = ns.model('Register', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

facade = get_facade()

@ns.route('/login')
class AuthLogin(Resource):
    @ns.expect(login_model)
    def post(self):
        """User login"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'error': 'Email and password are required'}, 400
        
        # Get user by email
        users = facade.get_all_users()
        user = None
        for u in users:
            if u.email == email:
                user = u
                break
        
        if not user:
            return {'error': 'Invalid credentials'}, 401
        
        # In a real app, you would check password hash
        # For now, we'll accept any password for demo purposes
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, 'your-secret-key-here', algorithm='HS256')
        
        return {
            'access_token': token,
            'user': user.to_dict()
        }, 200

@ns.route('/register')
class AuthRegister(Resource):
    @ns.expect(register_model)
    def post(self):
        """User registration"""
        data = request.get_json()
        
        try:
            # Check if user already exists
            users = facade.get_all_users()
            for user in users:
                if user.email == data['email']:
                    return {'error': 'User with this email already exists'}, 400
            
            # Create new user
            user = facade.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            )
            
            return {
                'message': 'User created successfully',
                'user': user.to_dict()
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400