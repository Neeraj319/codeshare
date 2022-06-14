from fastapi.exceptions import HTTPException
from starlette import status
from fastapi import Request
from auth import schemas as auth_schemas
from auth import services as auth_services


async def signup(user: auth_schemas.UserSchema, request: Request):
    """
        route for creating user on the database only non admins can be created from this route
        dose not matter if you send (is_admin, id) or not backend will remove it
    {
      "username": "string",
      "password": "string",
    }

    """

    return await auth_services.add_user(user)


async def login(credentials: auth_schemas.UserSchema):
    """
        this route returns `JWT` Token of an user on the database
        every time this route is visited with correct credentials Token gets reset
        only send the data written in docs
    {
      "username": "string",
      "password": "string"
    }
    """
    if user := await auth_services.authenticate_user(
        username=credentials.username, password=credentials.password
    ):
        return {"token": await auth_services.create_token(user)}
    else:
        raise HTTPException(
            detail="invalid username or password",
            status_code=status.HTTP_403_FORBIDDEN,
        )


async def user_detail(user_id: int):
    """
    returns user with the given id
    """
    if user := await auth_services.get_user_by_username(user_id):
        return user
    else:
        raise HTTPException(
            detail="user not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
