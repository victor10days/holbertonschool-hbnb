from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade

ns = Namespace('places', description='Place operations')

place_model = ns.model('Place', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'location': fields.String(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String),
    'reviews': fields.List(fields.String),
})

facade = get_facade()

@ns.route('/')
class PlaceList(Resource):
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = ns.payload
        place = facade.create_place(**data)
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
    def put(self, id):
        """Update a place by id"""
        data = ns.payload
        place = facade.update_place(id, **data)
        if not place:
            ns.abort(404, 'Place not found')
        return place.to_dict()
