from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.api import facade

ns = Namespace("reviews", description="Review operations")

review_model = ns.model("Review", {
    "id": fields.String(readonly=True),
    "text": fields.String(required=True),
    "rating": fields.Integer(min=0, max=5),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
    "created_at": fields.String(readonly=True),
    "updated_at": fields.String(readonly=True),
})

@ns.route("")
class ReviewList(Resource):
    @ns.marshal_list_with(review_model)
    def get(self):
        return facade().list_reviews()

    @ns.expect(review_model, validate=True)
    @ns.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""
        current_user_id = get_jwt_identity()
        payload = ns.payload
        payload['user_id'] = current_user_id
        place = facade().get_place(payload['place_id'])
        if place.get('owner_id') == current_user_id:
            ns.abort(403, "Owners cannot review their own places")
            existing_reviews = facade().list_reviews_for_place(payload['place_id'])
            for review in existing_reviews:
                if review.user_id == current_user_id:
                    ns.abort(403, "User has already reviewed this place")
        return facade().create_review(ns.payload), 201

@ns.route("/<string:review_id>")
class ReviewItem(Resource):
    @ns.marshal_with(review_model)
    def get(self, review_id):
        return facade().get_review(review_id)

    @ns.expect(review_model, validate=True)
    @ns.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user_id = get_jwt_identity()
        review = facade().get_review(review_id)
        if review.user_id != current_user_id:
            ns.abort(403, "Permission denied to update this review")
        return facade().update_review(review_id, ns.payload)

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        review = facade().get_review(review_id)
        if review.user_id != current_user_id:
            ns.abort(403, "Permission denied to delete this review")
        facade().delete_review(review_id)
        return {"status": "deleted"}, 204

@ns.route("/place/<string:place_id>")
class PlaceReviews(Resource):
    @ns.marshal_list_with(review_model)
    def get(self, place_id):
        return facade().list_reviews_for_place(place_id)
