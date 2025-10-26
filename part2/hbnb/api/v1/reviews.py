from flask_restx import Namespace, Resource, fields
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
    def post(self):
        return facade().create_review(ns.payload), 201

@ns.route("/<string:review_id>")
class ReviewItem(Resource):
    @ns.marshal_with(review_model)
    def get(self, review_id):
        return facade().get_review(review_id)

    @ns.expect(review_model, validate=True)
    @ns.marshal_with(review_model)
    def put(self, review_id):
        return facade().update_review(review_id, ns.payload)

    def delete(self, review_id):
        facade().delete_review(review_id)
        return {"status": "deleted"}, 204

@ns.route("/place/<string:place_id>")
class PlaceReviews(Resource):
    @ns.marshal_list_with(review_model)
    def get(self, place_id):
        return facade().list_reviews_for_place(place_id)
