from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade

ns = Namespace('users', description='User operations')
user_model = ns.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
})

facade = get_facade()

@ns.route('/')
class UserList(Resource):
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        data = ns.payload
        try:
            user = facade.create_user(**data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.marshal_list_with(user_model)
    def get(self):
        users = facade.get_all_users()
        return [u.to_dict() for u in users]

@ns.route('/<string:id>')
@ns.response(404, 'User not found')
class UserResource(Resource):
    @ns.marshal_with(user_model)
    def get(self, id):
        user = facade.get_user(id)
        if not user:
            ns.abort(404, 'User not found')
        return user.to_dict()

    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, id):
        data = ns.payload
        user = facade.update_user(id, **data)
        if not user:
            ns.abort(404, 'User not found')
        return user.to_dict()
