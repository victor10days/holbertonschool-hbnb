# Facade Pattern Implementation for the HBNB API

from app.persistence.repository import get_repository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class Facade:
    def __init__(self):
        self.user_repo = get_repository('user')
        self.amenity_repo = get_repository('amenity')
        self.place_repo = get_repository('place')
        self.review_repo = get_repository('review')

    # USER (already covered above, for reference)
    def create_user(self, name, email, password):
        user = User(name, email, password)
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, **kwargs):
        return self.user_repo.update(user_id, **kwargs)

    # AMENITY
    def create_amenity(self, name, description, place_id=None):
        amenity = Amenity(name, description, place_id)
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, **kwargs):
        return self.amenity_repo.update(amenity_id, **kwargs)

    # PLACE
    def create_place(self, name, location, owner_id, amenities=None, reviews=None):
        place = Place(name, location, owner_id, amenities, reviews)
        self.place_repo.add(place)
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, **kwargs):
        return self.place_repo.update(place_id, **kwargs)

    # REVIEW
    def create_review(self, content, user_id, place_id, rating=None):
        review = Review(content, user_id, place_id, rating)
        self.review_repo.add(review)
        # Optionally, add this review's id to the corresponding Place's reviews
        place = self.place_repo.get(place_id)
        if place:
            place.add_review(review.id)
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, **kwargs):
        return self.review_repo.update(review_id, **kwargs)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

# Singleton pattern so you always get the same facade
_facade = None
def get_facade():
    global _facade
    if _facade is None:
        _facade = Facade()
    return _facade
