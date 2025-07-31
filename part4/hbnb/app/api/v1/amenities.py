from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade

ns = Namespace('amenities', description='Amenity operations')

amenity_model = ns.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String,
    'place_id': fields.String,
})

facade = get_facade()

@ns.route('/')
class AmenityList(Resource):
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = ns.payload
        amenity = facade.create_amenity(**data)
        return amenity.to_dict(), 201

    @ns.marshal_list_with(amenity_model)
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities]

@ns.route('/<string:id>')
@ns.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @ns.marshal_with(amenity_model)
    def get(self, id):
        """Get an amenity by id"""
        amenity = facade.get_amenity(id)
        if not amenity:
            ns.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, id):
        """Update an amenity by id"""
        data = ns.payload
        amenity = facade.update_amenity(id, **data)
        if not amenity:
            ns.abort(404, 'Amenity not found')
        return amenity.to_dict()
