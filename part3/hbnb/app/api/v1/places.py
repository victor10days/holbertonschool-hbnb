from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import get_facade
from app.decorators.auth import require_ownership, admin_required

ns = Namespace('places', description='Place operations')

place_model = ns.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(readonly=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True),
})

facade = get_facade()

@ns.route('/')
class PlaceList(Resource):
    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place"""
        data = ns.payload
        current_user_id = get_jwt_identity()
        data['owner_id'] = current_user_id
        place = facade.create_place(data)
        return place.to_dict(), 201

    def get(self):
        """Get all places with basic information"""
        places = facade.get_all_places()
        result = []
        for place in places:
            place_dict = place.to_dict()
            # Add frontend compatibility fields
            place_dict['price_per_night'] = place_dict['price']
            place_dict['city'] = getattr(place, 'city', 'Unknown')
            place_dict['country'] = getattr(place, 'country', 'Unknown')
            place_dict['description'] = getattr(place, 'description', place.title)
            result.append(place_dict)
        return result

@ns.route('/<string:id>')
@ns.response(404, 'Place not found')
class PlaceResource(Resource):
    def get(self, id):
        """Get a place by id with detailed information"""
        place = facade.get_place(id)
        if not place:
            ns.abort(404, 'Place not found')
        
        place_dict = place.to_dict()
        
        # Add owner information
        if place.owner_id:
            owner = facade.get_user(place.owner_id)
            if owner:
                place_dict['owner'] = {
                    'first_name': owner.first_name,
                    'last_name': owner.last_name
                }
        
        # Add reviews
        reviews = facade.get_reviews_by_place(id)
        place_dict['reviews'] = []
        for review in reviews:
            review_dict = review.to_dict()
            # Add user info to review
            user = facade.get_user(review.user_id)
            if user:
                review_dict['user'] = {
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            place_dict['reviews'].append(review_dict)
        
        # Add amenities (placeholder for now)
        place_dict['amenities'] = []
        
        # Convert price to price_per_night for frontend compatibility
        place_dict['price_per_night'] = place_dict['price']
        place_dict['city'] = getattr(place, 'city', 'Unknown')
        place_dict['country'] = getattr(place, 'country', 'Unknown')
        place_dict['description'] = getattr(place, 'description', place.title)
        
        return place_dict

    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    @jwt_required()
    @require_ownership('place')
    def put(self, id):
        """Update a place by id"""
        data = ns.payload
        # Remove owner_id from data to prevent changing ownership
        data.pop('owner_id', None)
        place = facade.update_place(id, **data)
        if not place:
            ns.abort(404, 'Place not found')
        return place.to_dict()

@ns.route('/<string:place_id>/reviews')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, 'Place not found')
        
        reviews = facade.get_reviews_by_place(place_id)
        result = []
        for review in reviews:
            review_dict = review.to_dict()
            # Add user information to review
            user = facade.get_user(review.user_id)
            if user:
                review_dict['user'] = {
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            result.append(review_dict)
        return result
    
    @jwt_required()
    def post(self, place_id):
        """Add a review to a specific place"""
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, 'Place not found')
        
        from flask import request
        data = request.get_json() or {}
        current_user_id = get_jwt_identity()
        
        # Validate required fields
        if not data.get('text'):
            return {'error': 'Review text is required'}, 400
        if not data.get('rating'):
            return {'error': 'Rating is required'}, 400
        
        try:
            rating = int(data['rating'])
            if not (1 <= rating <= 5):
                return {'error': 'Rating must be between 1 and 5'}, 400
        except (ValueError, TypeError):
            return {'error': 'Rating must be a valid number'}, 400
        
        review_data = {
            'text': data['text'],
            'rating': rating,
            'user_id': current_user_id,
            'place_id': place_id
        }
        
        try:
            review = facade.create_review(review_data)
            review_dict = review.to_dict()
            # Add user information
            user = facade.get_user(current_user_id)
            if user:
                review_dict['user'] = {
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            return review_dict, 201
        except Exception as e:
            return {'error': str(e)}, 400
