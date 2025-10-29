from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
places_ns = Namespace('places', description='Place operations')

# Create facade instance
facade = HBnBFacade()

# Define models for Swagger documentation
place_model = places_ns.model('Place', {
    'id': fields.String(readonly=True, description='Place unique identifier'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'owner': fields.Raw(description='Owner details'),
    'amenities': fields.List(fields.Raw, description='List of amenities'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

place_input_model = places_ns.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title', example='Cozy Apartment'),
    'description': fields.String(description='Place description', example='A nice place to stay'),
    'price': fields.Float(required=True, description='Price per night', example=100.0),
    'latitude': fields.Float(required=True, description='Latitude (-90 to 90)', example=40.7128),
    'longitude': fields.Float(required=True, description='Longitude (-180 to 180)', example=-74.0060),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs', example=[])
})

place_update_model = places_ns.model('PlaceUpdate', {
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude (-90 to 90)'),
    'longitude': fields.Float(description='Longitude (-180 to 180)')
})


@places_ns.route('/')
class PlaceList(Resource):
    """Place collection endpoint."""

    @places_ns.doc('list_places')
    @places_ns.marshal_list_with(place_model)
    def get(self):
        """Retrieve a list of all places."""
        places = facade.get_all_places()
        result = []
        for place in places:
            place_dict = place.to_dict()
            # Add owner details
            if place.owner:
                place_dict['owner'] = place.owner.to_dict()
            # Add amenities details
            place_dict['amenities'] = [amenity.to_dict() for amenity in place.amenities]
            result.append(place_dict)
        return result, 200

    @places_ns.doc('create_place')
    @places_ns.expect(place_input_model, validate=True)
    @places_ns.marshal_with(place_model, code=201)
    @places_ns.response(400, 'Invalid input data or related entity not found')
    def post(self):
        """Create a new place."""
        try:
            place_data = request.json
            place = facade.create_place(place_data)

            # Build response with owner and amenities details
            result = place.to_dict()
            result['owner'] = place.owner.to_dict()
            result['amenities'] = [amenity.to_dict() for amenity in place.amenities]

            return result, 201
        except ValueError as e:
            places_ns.abort(400, str(e))


@places_ns.route('/<string:place_id>')
@places_ns.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """Place resource endpoint."""

    @places_ns.doc('get_place')
    @places_ns.marshal_with(place_model)
    @places_ns.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve a place by ID with owner and amenities details."""
        place = facade.get_place(place_id)
        if not place:
            places_ns.abort(404, 'Place not found')

        # Build response with nested owner and amenities
        result = place.to_dict()
        result['owner'] = place.owner.to_dict()
        result['amenities'] = [amenity.to_dict() for amenity in place.amenities]

        return result, 200

    @places_ns.doc('update_place')
    @places_ns.expect(place_update_model, validate=True)
    @places_ns.marshal_with(place_model)
    @places_ns.response(400, 'Invalid input data')
    @places_ns.response(404, 'Place not found')
    def put(self, place_id):
        """Update an existing place."""
        try:
            place_data = request.json
            place = facade.update_place(place_id, place_data)
            if not place:
                places_ns.abort(404, 'Place not found')

            # Build response with owner and amenities details
            result = place.to_dict()
            result['owner'] = place.owner.to_dict()
            result['amenities'] = [amenity.to_dict() for amenity in place.amenities]

            return result, 200
        except ValueError as e:
            places_ns.abort(400, str(e))

    @places_ns.doc('delete_place')
    @places_ns.response(204, 'Place deleted successfully')
    @places_ns.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place."""
        result = facade.delete_place(place_id)
        if not result:
            places_ns.abort(404, 'Place not found')
        return '', 204


@places_ns.route('/<string:place_id>/reviews')
@places_ns.param('place_id', 'The place identifier')
class PlaceReviews(Resource):
    """Place reviews endpoint."""

    @places_ns.doc('get_place_reviews')
    def get(self, place_id):
        """Retrieve all reviews for a specific place."""
        # Validate place exists
        place = facade.get_place(place_id)
        if not place:
            places_ns.abort(404, 'Place not found')

        # Get reviews for this place
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
