from flask_restx import Namespace, Resource, fields
from hbnb.api import facade

ns = Namespace("users", description="User operations")

# Model for creating/updating users (includes password)
user_model = ns.model("User", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
    "first_name": fields.String(required=True, description="User first name"),
    "last_name": fields.String(required=True, description="User last name"),
})

# Model for responses (excludes password)
user_response = ns.model("UserResponse", {
    "id": fields.String(readonly=True, description="User ID"),
    "email": fields.String(readonly=True, description="User email"),
    "first_name": fields.String(readonly=True, description="User first name"),
    "last_name": fields.String(readonly=True, description="User last name"),
    "is_admin": fields.Boolean(readonly=True, description="Admin status"),
    "created_at": fields.String(readonly=True, description="Creation date"),
    "updated_at": fields.String(readonly=True, description="Last update date"),
})


@ns.route("")
class UserList(Resource):
    @ns.marshal_list_with(user_response)
    def get(self):
        """List all users (passwords excluded)"""
        return facade().list_users()

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(user_response, code=201)
    def post(self):
        """Create a new user"""
        payload = ns.payload
        # Facade will handle password hashing
        return facade().create_user(payload), 201


@ns.route("/<string:user_id>")
class UserItem(Resource):
    @ns.marshal_with(user_response)
    def get(self, user_id):
        """Get user by ID (password excluded)"""
        return facade().get_user(user_id)

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(user_response)
    def put(self, user_id):
        """Update user"""
        payload = ns.payload
        return facade().update_user(user_id, payload)
