from app.persistence.repository import get_repository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = get_repository('user')
        self.place_repo = get_repository('place')
        self.review_repo = get_repository('review')
        self.amenity_repo = get_repository('amenity')

    # User methods
    def create_user(self, user_data):
        if isinstance(user_data, User):
            # If user_data is already a User object, use it directly
            user = user_data
        else:
            # If user_data is a dict, create User from it
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data.get('password'),
                is_admin=user_data.get('is_admin', False)
            )
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, **kwargs):
        return self.user_repo.update(user_id, **kwargs)

    def get_places_by_user(self, user_id):
        places = self.place_repo.get_all()
        return [place for place in places if hasattr(place, 'owner_id') and place.owner_id == user_id]

    def get_reviews_by_user(self, user_id):
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.user_id == user_id]
    
    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place_id == place_id]

    # Place methods
    def create_place(self, place_data):
        if isinstance(place_data, Place):
            place = place_data
        else:
            place = Place(
                title=place_data['title'],
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude']
            )
            # Add owner_id if provided
            if 'owner_id' in place_data:
                place.owner_id = place_data['owner_id']
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, **kwargs):
        return self.place_repo.update(place_id, **kwargs)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # Review methods
    def create_review(self, review_data):
        if isinstance(review_data, Review):
            review = review_data
        else:
            # Get valid IDs for validation
            valid_user_ids = [user.id for user in self.get_all_users()]
            valid_place_ids = [place.id for place in self.get_all_places()]
            
            review = Review(
                text=review_data['text'],
                user_id=review_data['user_id'],
                place_id=review_data['place_id'],
                valid_user_ids=valid_user_ids,
                valid_place_ids=valid_place_ids,
                rating=review_data.get('rating', 5)
            )
        self.review_repo.add(review)
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, **kwargs):
        return self.review_repo.update(review_id, **kwargs)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    # Amenity methods
    def create_amenity(self, amenity_data):
        if isinstance(amenity_data, Amenity):
            amenity = amenity_data
        else:
            amenity = Amenity(
                name=amenity_data['name'],
                description=amenity_data.get('description', '')
            )
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, **kwargs):
        return self.amenity_repo.update(amenity_id, **kwargs)

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

_facade = None
def get_facade():
    global _facade
    if _facade is None:
        _facade = HBnBFacade()
    return _facade


