from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity
from app.services.facade import get_facade
from app.decorators.auth import require_ownership, admin_required

ns = Namespace('users', description='User operations')

# Model for user data (excludes sensitive information)
user_model = ns.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'is_admin': fields.Boolean(readonly=True)
})

# Model for user updates (excludes admin flag)
user_update_model = ns.model('UserUpdate', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'email': fields.String(required=False)
})

facade = get_facade()

@ns.route('/')
class UserList(Resource):
    @ns.doc('create_user', security='Bearer')
    @admin_required
    @ns.expect(user_model)
    def post(self):
        """Create a new user (Admin only)"""
        data = ns.payload
        try:
            user = facade.create_user(data)
            return user.to_dict_safe(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """Get all users (Public endpoint)"""
        users = facade.get_all_users()
        return [u.to_dict_safe() for u in users]

@ns.route('/<string:id>')
@ns.response(404, 'User not found')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        """Get user by ID (Public endpoint)"""
        user = facade.get_user(id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict_safe()

    @ns.doc('update_user', security='Bearer')
    @require_ownership('user')
    @ns.expect(user_update_model)
    def put(self, id):
        """Update user profile (Authenticated users can only update their own profile)"""
        data = ns.payload
        
        # Remove sensitive fields that shouldn't be updated via this endpoint
        sensitive_fields = ['id', 'created_at', 'updated_at', 'is_admin', 'password']
        for field in sensitive_fields:
            data.pop(field, None)
        
        try:
            user = facade.update_user(id, **data)
            if not user:
                return {'error': 'User not found'}, 404
            return user.to_dict_safe(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:id>/profile')
@ns.response(404, 'User not found')
class UserProfile(Resource):
    @ns.doc('get_user_profile', security='Bearer')
    @require_ownership('user')
    def get(self, id):
        """Get detailed user profile (Users can only view their own detailed profile)"""
        user = facade.get_user(id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Return detailed profile information
        profile = user.to_dict_safe()
        
        # Add additional profile information if needed
        # For example, user's places and reviews count
        try:
            user_places = facade.get_places_by_user(id)
            user_reviews = facade.get_reviews_by_user(id)
            profile['places_count'] = len(user_places) if user_places else 0
            profile['reviews_count'] = len(user_reviews) if user_reviews else 0
        except:
            # If methods don't exist yet, just include basic info
            profile['places_count'] = 0
            profile['reviews_count'] = 0
        
        return profile, 200
