from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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

# Model for regular user updates (without email/password)
user_update_model = ns.model("UserUpdate", {
    "first_name": fields.String(description="User first name"),
    "last_name": fields.String(description="User last name"),
})

# Model for admin user updates (includes email and password)
admin_user_update_model = ns.model("AdminUserUpdate", {
    "email": fields.String(description="User email"),
    "password": fields.String(description="User password"),
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
    @jwt_required()
    def post(self):
        """Create a new user (Admin only)"""
        # Check if user is admin
        claims = get_jwt()
        if not claims.get("is_admin", False):
            ns.abort(403, "Admin privileges required")

        payload = ns.payload
        # Facade will handle password hashing
        return facade().create_user(payload), 201


@ns.route("/<string:user_id>")
class UserItem(Resource):
    @ns.marshal_with(user_response)
    def get(self, user_id):
        """Get user by ID (password excluded)"""
        return facade().get_user(user_id)

    @ns.expect(admin_user_update_model, validate=False)
    @ns.marshal_with(user_response)
    @jwt_required()
    def put(self, user_id):
        """Update user (regular users can only update their own first/last name, admins can update any user)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        payload = ns.payload

        # Check if user is authorized
        if not is_admin and current_user_id != user_id:
            ns.abort(403, "Permission denied to update this user")

        # Regular users cannot update email or password
        if not is_admin:
            if 'email' in payload or 'password' in payload:
                ns.abort(403, "Only admins can update email or password")

        # If admin is updating email, check for uniqueness
        if is_admin and 'email' in payload:
            existing_user = facade().get_user_by_email(payload['email'])
            if existing_user and existing_user.id != user_id:
                ns.abort(400, "Email already in use")

        return facade().update_user(user_id, payload)
