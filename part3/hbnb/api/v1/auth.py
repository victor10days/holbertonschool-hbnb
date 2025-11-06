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
