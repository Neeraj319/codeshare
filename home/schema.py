from pydantic import BaseModel
from typing import Optional
from .models import User


class User:
    id: Optional[int]
    username: str
    password: str

    @property
    def username(self):
        return self.username

    @username.setter
    async def username(self, _username):
        if len(_username) > 60:
            return
        if await User.get(user__username == _username):
            return None
        self.username = _username

    @password.setter
    async def password(self, _password):
        if len(_password) > 60:
            return
        if await User.get(user__password == _password):
            return None
        self.username = _password
