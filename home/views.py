from fastapi.exceptions import HTTPException
from starlette import status
from .models import User
from .dependencies import add_user, create_token, authenticate_user
from .schema import PydanticUser

from fastapi.responses import Response


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


async def users():
    """
    get all users from the database
    """
    return await User.all().values("id", "username")
