from flask_restx import Namespace, Resource, fields
from hbnb.api import facade

ns = Namespace("places", description="Place operations")

amenity_inline = ns.model("AmenityInline", {
    "id": fields.String,
    "name": fields.String,
})

owner_inline = ns.model("OwnerInline", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
})

place_model = ns.model("Place", {
    "id": fields.String(readonly=True),
    "name": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenity_ids": fields.List(fields.String),
    "owner": fields.Nested(owner_inline, readonly=True),
    "amenities": fields.List(fields.Nested(amenity_inline), readonly=True),
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

@ns.route("")
class PlaceList(Resource):
    @ns.marshal_list_with(place_model)
    def get(self):
        return facade().list_places()

    @ns.expect(place_model, validate=True)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        return facade().create_place(ns.payload), 201

@ns.route("/<string:place_id>")
class PlaceItem(Resource):
    @ns.marshal_with(place_model)
    def get(self, place_id):
        return facade().get_place(place_id)

    @ns.expect(place_model, validate=True)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        return facade().update_place(place_id, ns.payload)
