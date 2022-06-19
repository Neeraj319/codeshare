from fastapi.exceptions import HTTPException
from starlette import status
from fastapi import Depends, Request
from auth import schemas as auth_schemas
from auth import services as auth_services
from codeshare.queries import db_init


async def signup(
    user: auth_schemas.UserSchema,
    request: Request,
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
        route for creating user on the database only non admins can be created from this route
        dose not matter if you send (is_admin, id) or not backend will remove it
    {
      "username": "string",
      "password": "string",
    }

    """

    data = auth_services.add_user(user=user, db_session=db_session)
    db_session.close()
    return data


async def login(
    credentials: auth_schemas.UserSchema,
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
        this route returns `JWT` Token of an user on the database
        every time this route is visited with correct credentials Token gets reset
        only send the data written in docs
    {
      "username": "string",
      "password": "string"
    }
    """
    if user := auth_services.authenticate_user(
        db_session=db_session,
        username=credentials.username,
        password=credentials.password,
    ):

        data = {"token": auth_services.create_token(user)}
        db_session.close()
        return data
    else:
        db_session.close()
        raise HTTPException(
            detail="invalid username or password",
            status_code=status.HTTP_403_FORBIDDEN,
        )


async def user_detail(
    username: int,
    db_session: db_init.DBConnector = Depends(db_init.db_connection),
):
    """
    returns user with the given id
    """
    if user := auth_services.get_user_by_username(
        username=username, db_session=db_session
    ):
        del user.password
        db_session.close()
        return user
    else:
        db_session.close()
        raise HTTPException(
            detail="user not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
