from app.persistence.repository import get_repository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = get_repository('user')

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

_facade = None
def get_facade():
    global _facade
    if _facade is None:
        _facade = HBnBFacade()
    return _facade


