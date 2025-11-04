from __future__ import annotations
from typing import Dict, Any, List
from .persistence.memory_repo import MemoryRepository
from .bl.user import User
from .bl.amenity import Amenity
from .bl.place import Place
from .bl.review import Review
from .errors import NotFound, BadRequest

class HbnbFacade:
    def __init__(self, repo: MemoryRepository | None = None):
        self.repo = repo or MemoryRepository()

    # ===== Users =====
    def create_user(self, user_data: dict):
    """Create a new user with hashed password"""
    from hbnb.bl.user import User

    plain_password = user_data.get("password")
    user = User(**user_data)
    user.validate()
    if plain_password:
        user.hash_password(plain_password)
    self.repo.add(user)
    return self._user_public(user)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        user = self.repo.get(User, user_id)
        if not user:
            raise NotFound()
        return self._user_public(user)

    def list_users(self) -> List[Dict[str, Any]]:
        return [self._user_public(u) for u in self.repo.list(User)]

    def update_user(self, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        user = self.repo.get(User, user_id)
        if not user:
            raise NotFound()
        for k, v in payload.items():
            if k == "id":
                continue
            setattr(user, k, v)
        user.validate()
        user.touch()
        self.repo.update(user)
        return self._user_public(user)

    def _user_public(self, user: User) -> Dict[str, Any]:
        d = user.to_dict()
        d.pop("password", None)
        return d

    # ===== Amenities =====
    def create_amenity(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        amenity = Amenity(**payload)
        amenity.validate()
        self.repo.add(amenity)
        return amenity.to_dict()

    def get_amenity(self, amenity_id: str) -> Dict[str, Any]:
        a = self.repo.get(Amenity, amenity_id)
        if not a:
            raise NotFound()
        return a.to_dict()

    def list_amenities(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self.repo.list(Amenity)]

    def update_amenity(self, amenity_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        a = self.repo.get(Amenity, amenity_id)
        if not a:
            raise NotFound()
        for k, v in payload.items():
            if k == "id":
                continue
            setattr(a, k, v)
        a.validate()
        a.touch()
        self.repo.update(a)
        return a.to_dict()

    # ===== Places =====
    def create_place(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # ensure owner exists
        owner_id = payload.get("owner_id")
        if not self.repo.get(User, owner_id):
            raise BadRequest("owner_id must reference an existing User")
        # ensure amenities exist
        for aid in payload.get("amenity_ids", []) or []:
            if not self.repo.get(Amenity, aid):
                raise BadRequest("amenity_ids must reference existing Amenities")
        place = Place(**payload)
        place.validate()
        self.repo.add(place)
        return self._place_expanded(place)

    def get_place(self, place_id: str) -> Dict[str, Any]:
        p = self.repo.get(Place, place_id)
        if not p:
            raise NotFound()
        return self._place_expanded(p)

    def list_places(self) -> List[Dict[str, Any]]:
        return [self._place_expanded(p) for p in self.repo.list(Place)]

    def update_place(self, place_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        p = self.repo.get(Place, place_id)
        if not p:
            raise NotFound()
        if "owner_id" in payload and not self.repo.get(User, payload["owner_id"]):
            raise BadRequest("owner_id must reference an existing User")
        if "amenity_ids" in payload:
            for aid in payload["amenity_ids"] or []:
                if not self.repo.get(Amenity, aid):
                    raise BadRequest("amenity_ids must reference existing Amenities")
        for k, v in payload.items():
            if k == "id":
                continue
            setattr(p, k, v)
        p.validate()
        p.touch()
        self.repo.update(p)
        return self._place_expanded(p)

    def _place_expanded(self, place: Place) -> Dict[str, Any]:
        d = place.to_dict()
        owner = self.repo.get(User, place.owner_id)
        d["owner"] = None if not owner else {
            "id": owner.id, "first_name": owner.first_name, "last_name": owner.last_name,
            "email": owner.email
        }
        d["amenities"] = [self.repo.get(Amenity, aid).to_dict() for aid in place.amenity_ids if self.repo.get(Amenity, aid)]
        return d

    # ===== Reviews =====
    def create_review(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.repo.get(User, payload.get("user_id")):
            raise BadRequest("user_id must reference an existing User")
        if not self.repo.get(Place, payload.get("place_id")):
            raise BadRequest("place_id must reference an existing Place")
        review = Review(**payload)
        review.validate()
        self.repo.add(review)
        return review.to_dict()

    def get_review(self, review_id: str) -> Dict[str, Any]:
        r = self.repo.get(Review, review_id)
        if not r:
            raise NotFound()
        return r.to_dict()

    def list_reviews(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.repo.list(Review)]

    def list_reviews_for_place(self, place_id: str) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.repo.list(Review, predicate=lambda x: x.place_id == place_id)]

    def update_review(self, review_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        r = self.repo.get(Review, review_id)
        if not r:
            raise NotFound()
        for k, v in payload.items():
            if k == "id":
                continue
            setattr(r, k, v)
        r.validate()
        r.touch()
        self.repo.update(r)
        return r.to_dict()

    def delete_review(self, review_id: str) -> None:
        if not self.repo.get(Review, review_id):
            raise NotFound()
        self.repo.delete(Review, review_id)
