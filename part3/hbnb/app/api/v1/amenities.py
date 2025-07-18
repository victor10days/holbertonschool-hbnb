from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.services.facade import get_facade
from app.decorators.auth import admin_required

ns = Namespace('amenities', description='Amenity operations')

amenity_model = ns.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String,
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True),
})

facade = get_facade()

@ns.route('/')
class AmenityList(Resource):
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    @jwt_required()
    @admin_required
    def post(self):
        """Create a new amenity (Admin only)"""
        data = ns.payload
        amenity = facade.create_amenity(data)
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
    @jwt_required()
    @admin_required
    def put(self, id):
        """Update an amenity by id (Admin only)"""
        data = ns.payload
        amenity = facade.update_amenity(id, **data)
        if not amenity:
            ns.abort(404, 'Amenity not found')
        return amenity.to_dict()

    @jwt_required()
    @admin_required
    def delete(self, id):
        """Delete an amenity by id (Admin only)"""
        success = facade.delete_amenity(id)
        if not success:
            ns.abort(404, 'Amenity not found')
        return {}, 204
