from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade  # We'll define this for singleton
from app.models.user import User

ns = Namespace('users', description='User operations')

user_model = ns.model('User', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    # password is not returned!
})

facade = get_facade()

@ns.route('/')
class UserList(Resource):
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = ns.payload
        user = facade.create_user(**data)
        return user.to_dict(), 201
    @ns.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users]
@ns.route('/<string:id>')
@ns.response(404, 'User not found')
class UserResource(Resource):
    @ns.marshal_with(user_model)
    def get(self, id):
        """Get user by id"""
        user = facade.get_user(id)
        if user is None:
            ns.abort(404, 'User not found')
        return user.to_dict()
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, id):
        """Update user by id"""
        data = ns.payload
        user = facade.update_user(id, **data)
        if user is None:
            ns.abort(404, 'User not found')
        return user.to_dict()
