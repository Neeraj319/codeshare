from fastapi.param_functions import Depends
from .models import User
from fastapi import status, HTTPException
from .schema import PydanticUser
from codeshare.settings import pwd


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
