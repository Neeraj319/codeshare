from codeshare.settings import get_crypto_context
from fastapi.param_functions import Depends
from auth import models as auth_models
from fastapi import status, HTTPException
import os
from auth import schemas as auth_schemas
from datetime import datetime, timedelta
from jose import JWTError, jwt
from codeshare.settings import get_crypto_context, get_oauth_2_scheme
from typing import NewType, Union


async def add_user(user: auth_schemas.UserSchema) -> auth_models.User:
    """
    basically adds user to the database by doing bunch of checks
    """
    # password validation
    if len(user.password) < 8:
        print("password is too short")
        raise HTTPException(
            detail="enter a password of length greater than 8",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if len(user.password) > 80:
        print("password is too long")
        raise HTTPException(
            detail="password too long",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if user.username == "":
        raise HTTPException(
            detail="username is empty",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    # check for unique username
    if await auth_models.User.get_or_none(username=user.username):
        print("username already exists")
        raise HTTPException(
            detail="username already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    # generating password hash
    password = get_crypto_context().hash(user.password)
    # saving the user to the database
    created_user = await auth_models.User.create(
        username=user.username, password=password
    )
    return auth_schemas.UserResponseSchema(**created_user.__dict__)


async def authenticate_user(username: str, password: str):
    """
    verifies weather the user exists in database or not
    and validates the password
    """
    if user := await auth_models.User.get_or_none(username=username):
        if not get_crypto_context().verify(password, user.password):
            return False
        return user


JWT = NewType(
    "JWT",
    {"username": str, "is_admin": bool, "id": int},
)


async def create_token(user: auth_schemas.UserSchema) -> JWT:
    """
    (do not pass password even if you do i will delete it :) )\n
    function to to create a jwt token of passed user
    returns the created JWT token

    """
    to_encode = dict(user)
    del to_encode["password"]

    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=os.environ.get("ALGORITHM")
    )
    return encoded_jwt


async def get_user_from_token(
    token: str = Depends(get_oauth_2_scheme()),
) -> Union[auth_models.User, None]:
    """
    token -> JWT token \n
    validates token and returns User object or None
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if user := await auth_models.User.get_or_none(username=username):
        return user
    else:
        raise credentials_exception


async def get_user_by_username(username: str) -> Union[auth_models.User, None]:
    """
    username -> username of the user\n
    returns the User or None
    """
    return await auth_models.User.get_or_none(username=username)
