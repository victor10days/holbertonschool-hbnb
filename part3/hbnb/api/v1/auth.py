from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from hbnb.api import facade

ns = Namespace("auth", description="Authentication operations")

#Login model
login_model = ns.model("Login", {
    "username": fields.String(required=True, description="The user's username"),
    "password": fields.String(required=True, description="The user's password"),
})

#Login response model
login_response_model = ns.model("LoginResponse", {
    "access_token": fields.String(description="JWT access token"),
})

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model, validate=True)
    @ns.marshal_with(login_response_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        data = ns.payload
        username = data.get("username")
        password = data.get("password")

        user = facade().authenticate_user(username, password)
        if not user:
            ns.abort(401, "Invalid username or password")

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}
