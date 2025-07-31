from app.persistence.repository import get_repository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = get_repository('user')

    def create_user(self, first_name, last_name, email):
        user = User(first_name, last_name, email)
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, **kwargs):
        return self.user_repo.update(user_id, **kwargs)

_facade = None
def get_facade():
    global _facade
    if _facade is None:
        _facade = HBnBFacade()
    return _facade


