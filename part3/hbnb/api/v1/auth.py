from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from hbnb.api import facade

ns = Namespace("auth", description="Authentication operations")

# Login model
login_model = ns.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
})

# Login response model
login_response = ns.model("LoginResponse", {
    "access_token": fields.String(description="JWT access token"),
})

# Register model
register_model = ns.model("Register", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
    "first_name": fields.String(required=True, description="User first name"),
    "last_name": fields.String(required=True, description="User last name"),
})

# User response model (without password)
user_response = ns.model("UserResponse", {
    "id": fields.String(readonly=True, description="User ID"),
    "email": fields.String(readonly=True, description="User email"),
    "first_name": fields.String(readonly=True, description="User first name"),
    "last_name": fields.String(readonly=True, description="User last name"),
    "is_admin": fields.Boolean(readonly=True, description="Admin status"),
    "created_at": fields.String(readonly=True, description="Creation date"),
    "updated_at": fields.String(readonly=True, description="Last update date"),
})


@ns.route("/register")
class Register(Resource):
    @ns.expect(register_model, validate=True)
    @ns.marshal_with(user_response, code=201)
    @ns.response(400, "Invalid input or email already exists")
    def post(self):
        """Register a new user"""
        user_data = ns.payload

        # Check if user already exists
        existing_user = facade().get_user_by_email(user_data["email"])
        if existing_user:
            ns.abort(400, "Email already registered")

        # Create the user (facade will hash the password)
        try:
            new_user = facade().create_user(user_data)
            return new_user, 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model, validate=True)
    @ns.marshal_with(login_response, code=200)
    @ns.response(401, "Invalid credentials")
    def post(self):
        """Authenticate user and return JWT token"""
        credentials = ns.payload
        email = credentials.get("email")
        password = credentials.get("password")

        # Get user by email - returns User object with password
        user = facade().get_user_by_email(email)

        # Verify user exists and password is correct
        if not user or not user.verify_password(password):
            ns.abort(401, "Invalid credentials")

        # Create access token with user identity and is_admin claim
        access_token = create_access_token(
            identity=user.id,
            additional_claims={"is_admin": user.is_admin}
        )

        return {"access_token": access_token}, 200
