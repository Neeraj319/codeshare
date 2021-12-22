from .models import User
from fastapi import status, HTTPException
from passlib.context import CryptContext
import os
from .schema import PydanticUser
from datetime import datetime, timedelta
from jose import JWTError, jwt


pwd = CryptContext(schemes=[os.environ.get("HASH_FUNCTION")], deprecated="auto")


async def add_user(user: PydanticUser) -> User:
    if len(user.password) < 8:
        raise HTTPException(
            detail="enter a password of length greater than 8",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if len(user.password) > 80:
        raise HTTPException(
            detail="password too long",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if await User.get_or_none(username=user.username):
        raise HTTPException(
            detail="username already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    password = pwd.hash(user.password)
    created_user = await User.create(username=user.username, password=password)
    return created_user


async def authenticate_user(username: str, password: str):
    if user := await User.get_or_none(username=username):
        if not pwd.verify(password, user.password):
            return False
        return user


async def create_token(user):
    to_encode = dict(user)
    del to_encode["password"]

    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=os.environ.get("ALGORITHM")
    )
    return encoded_jwt
