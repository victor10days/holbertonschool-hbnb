from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import get_facade
from app.decorators.auth import require_ownership, admin_required

ns = Namespace('places', description='Place operations')

place_model = ns.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(readonly=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True),
})

facade = get_facade()

@ns.route('/')
class PlaceList(Resource):
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place"""
        data = ns.payload
        current_user_id = get_jwt_identity()
        data['owner_id'] = current_user_id
        place = facade.create_place(data)
        return place.to_dict(), 201

    @ns.marshal_list_with(place_model)
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places]

@ns.route('/<string:id>')
@ns.response(404, 'Place not found')
class PlaceResource(Resource):
    @ns.marshal_with(place_model)
    def get(self, id):
        """Get a place by id"""
        place = facade.get_place(id)
        if not place:
            ns.abort(404, 'Place not found')
        return place.to_dict()

    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    @jwt_required()
    @require_ownership('place')
    def put(self, id):
        """Update a place by id"""
        data = ns.payload
        # Remove owner_id from data to prevent changing ownership
        data.pop('owner_id', None)
        place = facade.update_place(id, **data)
        if not place:
            ns.abort(404, 'Place not found')
        return place.to_dict()
