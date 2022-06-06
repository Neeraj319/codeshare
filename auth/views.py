from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from .models import User
from .dependencies import (
    create_token, authenticate_user, get_super_user, get_user, add_user,)
from .schema import PydanticUser


async def create_user(user: PydanticUser):

    await add_user(user)

    return user


async def login(credentials: PydanticUser):
    if user := await authenticate_user(
        username=credentials.username, password=credentials.password
    ):
        return await create_token(user)
    else:
        raise HTTPException(
            detail="invalid username or password",
            status_code=status.HTTP_403_FORBIDDEN,
        )


async def users(user: PydanticUser = Depends(get_super_user)):
    """
    get all users from the database
    """
    if user:
        return await User.all().values("id", "username")
    else:
        raise HTTPException(
            detail="you are not authorized to access this resource",
            status_code=status.HTTP_403_FORBIDDEN,
        )
