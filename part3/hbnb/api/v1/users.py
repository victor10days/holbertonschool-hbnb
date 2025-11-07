from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
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

# Model for regular user updates (without email/password) :
user_update_model = ns.model("UserUpdate", {
    "first_name": fields.String(description="User first name"),
    "last_name": fields.String(description="User last name"),
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
    @jwt_required()
    def put(self, user_id):
        """Update user"""
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            ns.abort(403, "Permission denied to update this user")
        payload = ns.payload
        if 'email' in payload or 'password' in payload:
            ns.abort(400, "Cannot update email or password via this endpoint")
        return facade().update_user(user_id, payload)
