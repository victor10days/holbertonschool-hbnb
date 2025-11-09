from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
users_ns = Namespace('users', description='User operations')

# Create facade instance
facade = HBnBFacade()

# Define models for Swagger documentation
user_model = users_ns.model('User', {
    'id': fields.String(readonly=True, description='User unique identifier'),
    'email': fields.String(required=True, description='User email address'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'is_admin': fields.Boolean(description='Admin status', default=False),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

user_input_model = users_ns.model('UserInput', {
    'email': fields.String(required=True, description='User email address', example='user@example.com'),
    'first_name': fields.String(required=True, description='User first name', example='John'),
    'last_name': fields.String(required=True, description='User last name', example='Doe'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

user_update_model = users_ns.model('UserUpdate', {
    'email': fields.String(description='User email address'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name')
})


@users_ns.route('/')
class UserList(Resource):
    """User collection endpoint."""

    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(user_model)
    def get(self):
        """Retrieve a list of all users."""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @users_ns.doc('create_user')
    @users_ns.expect(user_input_model, validate=True)
    @users_ns.marshal_with(user_model, code=201)
    @users_ns.response(400, 'Invalid input data or email already registered')
    def post(self):
        """Create a new user."""
        try:
            user_data = request.json
            user = facade.create_user(user_data)
            return user.to_dict(), 201
        except ValueError as e:
            users_ns.abort(400, str(e))


@users_ns.route('/<string:user_id>')
@users_ns.param('user_id', 'The user identifier')
class UserResource(Resource):
    """User resource endpoint."""

    @users_ns.doc('get_user')
    @users_ns.marshal_with(user_model)
    @users_ns.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve a user by ID."""
        user = facade.get_user(user_id)
        if not user:
            users_ns.abort(404, 'User not found')
        return user.to_dict(), 200

    @users_ns.doc('update_user')
    @users_ns.expect(user_update_model, validate=True)
    @users_ns.marshal_with(user_model)
    @users_ns.response(400, 'Invalid input data')
    @users_ns.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user."""
        try:
            user_data = request.json
            user = facade.update_user(user_id, user_data)
            if not user:
                users_ns.abort(404, 'User not found')
            return user.to_dict(), 200
        except ValueError as e:
            users_ns.abort(400, str(e))

    @users_ns.doc('delete_user')
    @users_ns.response(204, 'User deleted successfully')
    @users_ns.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user."""
        result = facade.delete_user(user_id)
        if not result:
            users_ns.abort(404, 'User not found')
        return '', 204
