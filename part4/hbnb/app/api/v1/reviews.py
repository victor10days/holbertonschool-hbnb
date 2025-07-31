from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade

ns = Namespace('reviews', description='Review operations')

review_model = ns.model('Review', {
    'id': fields.String(readonly=True),
    'content': fields.String(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True),
    'rating': fields.Integer,
})

facade = get_facade()

@ns.route('/')
class ReviewList(Resource):
    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = ns.payload
        review = facade.create_review(**data)
        return review.to_dict(), 201

    @ns.marshal_list_with(review_model)
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews]

@ns.route('/<string:id>')
@ns.response(404, 'Review not found')
class ReviewResource(Resource):
    @ns.marshal_with(review_model)
    def get(self, id):
        """Get a review by id"""
        review = facade.get_review(id)
        if not review:
            ns.abort(404, 'Review not found')
        return review.to_dict()

    @ns.expect(review_model)
    @ns.marshal_with(review_model)
    def put(self, id):
        """Update a review by id"""
        data = ns.payload
        review = facade.update_review(id, **data)
        if not review:
            ns.abort(404, 'Review not found')
        return review.to_dict()

    def delete(self, id):
        """Delete a review by id"""
        success = facade.delete_review(id)
        if not success:
            ns.abort(404, 'Review not found')
        return {}, 204
