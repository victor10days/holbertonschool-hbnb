from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
reviews_ns = Namespace('reviews', description='Review operations')

# Create facade instance
facade = HBnBFacade()

# Define models for Swagger documentation
review_model = reviews_ns.model('Review', {
    'id': fields.String(readonly=True, description='Review unique identifier'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

review_input_model = reviews_ns.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text', example='Great place!'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', example=5),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

review_update_model = reviews_ns.model('ReviewUpdate', {
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)')
})


@reviews_ns.route('/')
class ReviewList(Resource):
    """Review collection endpoint."""

    @reviews_ns.doc('list_reviews')
    @reviews_ns.marshal_list_with(review_model)
    def get(self):
        """Retrieve a list of all reviews."""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

    @reviews_ns.doc('create_review')
    @reviews_ns.expect(review_input_model, validate=True)
    @reviews_ns.marshal_with(review_model, code=201)
    @reviews_ns.response(400, 'Invalid input data or related entity not found')
    def post(self):
        """Create a new review."""
        try:
            review_data = request.json
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            reviews_ns.abort(400, str(e))


@reviews_ns.route('/<string:review_id>')
@reviews_ns.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Review resource endpoint."""

    @reviews_ns.doc('get_review')
    @reviews_ns.marshal_with(review_model)
    @reviews_ns.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve a review by ID."""
        review = facade.get_review(review_id)
        if not review:
            reviews_ns.abort(404, 'Review not found')
        return review.to_dict(), 200

    @reviews_ns.doc('update_review')
    @reviews_ns.expect(review_update_model, validate=True)
    @reviews_ns.marshal_with(review_model)
    @reviews_ns.response(400, 'Invalid input data')
    @reviews_ns.response(404, 'Review not found')
    def put(self, review_id):
        """Update an existing review."""
        try:
            review_data = request.json
            review = facade.update_review(review_id, review_data)
            if not review:
                reviews_ns.abort(404, 'Review not found')
            return review.to_dict(), 200
        except ValueError as e:
            reviews_ns.abort(400, str(e))

    @reviews_ns.doc('delete_review')
    @reviews_ns.response(204, 'Review deleted successfully')
    @reviews_ns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review."""
        result = facade.delete_review(review_id)
        if not result:
            reviews_ns.abort(404, 'Review not found')
        return '', 204


@reviews_ns.route('/place/<string:place_id>')
@reviews_ns.param('place_id', 'The place identifier')
class PlaceReviews(Resource):
    """Reviews for a specific place endpoint."""

    @reviews_ns.doc('get_place_reviews')
    @reviews_ns.marshal_list_with(review_model)
    @reviews_ns.response(200, 'Success')
    def get(self, place_id):
        """Retrieve all reviews for a specific place."""
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
