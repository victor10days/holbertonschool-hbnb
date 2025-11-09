from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
amenities_ns = Namespace('amenities', description='Amenity operations')

# Create facade instance
facade = HBnBFacade()

# Define models for Swagger documentation
amenity_model = amenities_ns.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity unique identifier'),
    'name': fields.String(required=True, description='Amenity name'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

amenity_input_model = amenities_ns.model('AmenityInput', {
    'name': fields.String(required=True, description='Amenity name', example='WiFi')
})

amenity_update_model = amenities_ns.model('AmenityUpdate', {
    'name': fields.String(required=True, description='Amenity name')
})


@amenities_ns.route('/')
class AmenityList(Resource):
    """Amenity collection endpoint."""

    @amenities_ns.doc('list_amenities')
    @amenities_ns.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve a list of all amenities."""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @amenities_ns.doc('create_amenity')
    @amenities_ns.expect(amenity_input_model, validate=True)
    @amenities_ns.marshal_with(amenity_model, code=201)
    @amenities_ns.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity."""
        try:
            amenity_data = request.json
            amenity = facade.create_amenity(amenity_data)
            return amenity.to_dict(), 201
        except ValueError as e:
            amenities_ns.abort(400, str(e))


@amenities_ns.route('/<string:amenity_id>')
@amenities_ns.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    """Amenity resource endpoint."""

    @amenities_ns.doc('get_amenity')
    @amenities_ns.marshal_with(amenity_model)
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Retrieve an amenity by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            amenities_ns.abort(404, 'Amenity not found')
        return amenity.to_dict(), 200

    @amenities_ns.doc('update_amenity')
    @amenities_ns.expect(amenity_update_model, validate=True)
    @amenities_ns.marshal_with(amenity_model)
    @amenities_ns.response(400, 'Invalid input data')
    @amenities_ns.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an existing amenity."""
        try:
            amenity_data = request.json
            amenity = facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                amenities_ns.abort(404, 'Amenity not found')
            return amenity.to_dict(), 200
        except ValueError as e:
            amenities_ns.abort(400, str(e))

    @amenities_ns.doc('delete_amenity')
    @amenities_ns.response(204, 'Amenity deleted successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity."""
        result = facade.delete_amenity(amenity_id)
        if not result:
            amenities_ns.abort(404, 'Amenity not found')
        return '', 204
