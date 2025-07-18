from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import get_facade
from app.decorators.auth import require_ownership

ns = Namespace('reviews', description='Review operations')

review_model = ns.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True),
    'user_id': fields.String(readonly=True),
    'place_id': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True),
})

facade = get_facade()

@ns.route('/')
class ReviewList(Resource):
    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""
        data = ns.payload
        current_user_id = get_jwt_identity()
        data['user_id'] = current_user_id
        review = facade.create_review(data)
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
    @jwt_required()
    @require_ownership('review')
    def put(self, id):
        """Update a review by id"""
        data = ns.payload
        # Remove user_id and place_id from data to prevent changing them
        data.pop('user_id', None)
        data.pop('place_id', None)
        review = facade.update_review(id, **data)
        if not review:
            ns.abort(404, 'Review not found')
        return review.to_dict()

    @jwt_required()
    @require_ownership('review')
    def delete(self, id):
        """Delete a review by id"""
        success = facade.delete_review(id)
        if not success:
            ns.abort(404, 'Review not found')
        return {}, 204
