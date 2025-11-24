from flask_restx import Namespace, Resource, fields
from hbnb.api import facade

ns = Namespace("users", description="User operations")

user_model = ns.model("User", {
    "id": fields.String(readonly=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True, writeOnly=True),
    "first_name": fields.String,
    "last_name": fields.String,
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

user_public = ns.clone("UserPublic", user_model, {
    "password": fields.Raw(discriminator=True, description="omitted in responses")
})

@ns.route("/")
class UserList(Resource):
    @ns.marshal_list_with(user_model, skip_none=True)
    def get(self):
        """List users (no passwords in response)"""
        return facade().list_users()

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        payload = ns.payload
        return facade().create_user(payload), 201

@ns.route("/<string:user_id>")
class UserItem(Resource):
    @ns.marshal_with(user_model)
    def get(self, user_id):
        return facade().get_user(user_id)

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        payload = ns.payload
        return facade().update_user(user_id, payload)
