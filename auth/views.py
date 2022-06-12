from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from fastapi import Request
from .dependencies import (
    create_token,
    authenticate_user,
    add_user,
    get_user_by_username,
)
from .schemas import PydanticUser


async def signup(user: PydanticUser, request: Request):
    return await add_user(user)


async def login(credentials: PydanticUser):
    if user := await authenticate_user(
        username=credentials.username, password=credentials.password
    ):
        return {"token": await create_token(user)}
    else:
        raise HTTPException(
            detail="invalid username or password",
            status_code=status.HTTP_403_FORBIDDEN,
        )


async def user_detail(user_id: int):
    if user := await get_user_by_username(user_id):
        return user
    else:
        raise HTTPException(
            detail="user not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
