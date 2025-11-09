from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from hbnb.api import facade

ns = Namespace("amenities", description="Amenity operations")

amenity_model = ns.model("Amenity", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True),
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

@ns.route("")
class AmenityList(Resource):
    @ns.marshal_list_with(amenity_model)
    def get(self):
        return facade().list_amenities()

    @ns.expect(amenity_model, validate=True)
    @ns.marshal_with(amenity_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only)"""
        # Check if user is admin
        claims = get_jwt()
        if not claims.get("is_admin", False):
            ns.abort(403, "Admin privileges required")

        return facade().create_amenity(ns.payload), 201

@ns.route("/<string:amenity_id>")
class AmenityItem(Resource):
    @ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        return facade().get_amenity(amenity_id)

    @ns.expect(amenity_model, validate=True)
    @ns.marshal_with(amenity_model)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""
        # Check if user is admin
        claims = get_jwt()
        if not claims.get("is_admin", False):
            ns.abort(403, "Admin privileges required")

        return facade().update_amenity(amenity_id, ns.payload)
