from codeshare.settings import get_crypto_context
from fastapi.param_functions import Depends
from auth.models import User
from fastapi import status, HTTPException
from auth.schema import PydanticUser, PydanticUserResponseModel
from codeshare.settings import get_crypto_context
from auth.dependencies import get_user_from_token


async def add_user(user: PydanticUser) -> User:
    if len(user.password) < 8:
        print('password is too short')
        raise HTTPException(
            detail="enter a password of length greater than 8",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if len(user.password) > 80:
        print('password is too long')
        raise HTTPException(
            detail="password too long",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if await User.get_or_none(username=user.username):
        print('username already exists')
        raise HTTPException(
            detail="username already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    password = get_crypto_context().hash(user.password)
    created_user = await User.create(username=user.username, password=password, is_admin=user.is_admin)
    user = {
        'id': created_user.id,
        'username': created_user.username,
        'is_admin': created_user.is_admin
    }
    return user


async def get_super_user(user: PydanticUser = Depends(get_user_from_token)):
    if user.is_admin:
        print('lxa')
        return user
    else:
        return None


async def get_users():
    users = await User.all().values("id", "username", "is_admin")
    return [PydanticUserResponseModel(**user) for user in users]
