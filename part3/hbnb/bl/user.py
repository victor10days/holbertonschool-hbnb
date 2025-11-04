from dataclasses import dataclass, field
from .base import BaseModel

@dataclass
class User(BaseModel):
    email: str = ""
    password: str = ""  # not returned in responses
    first_name: str = ""
    last_name: str = ""

    def validate(self) -> None:
        if not self.email or "@" not in self.email:
            raise ValueError("email must be a valid address")
        if not self.password:
            raise ValueError("password is required")
