class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(user_id={self.user_id}, name='{self.name}', email='{self.email}')"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (self.user_id == other.user_id and
                self.name == other.name and
                self.email == other.email)
