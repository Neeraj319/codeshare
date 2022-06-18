from auth import schemas as auth_schemas
from datetime import datetime, timedelta
from typing import NewType, Union
from codeshare.settings import get_crypto_context
from fastapi import status, HTTPException
import os
from jose import jwt
from codeshare import queries


def get_user_by_username(
    username: str,
) -> Union[auth_schemas.UserSchema, None]:
    """
    username -> username of the user\n
    returns the User or None:
    """
    data = queries.select(
        table_name="user", condition="where username = %s", condition_values=(username,)
    )
    if not data:
        return None
    user_dict = dict(zip(("id", "username", "password", "is_admin"), data[0]))
    return auth_schemas.UserSchema(**user_dict)


def add_user(user: auth_schemas.UserSchema) -> auth_schemas.UserResponseSchema:
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
    # generating password hash
    password = get_crypto_context().hash(user.password)
    if get_user_by_username(user.username):
        raise HTTPException(
            detail="username already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    queries.insert("user", ("username", "password"), (user.username, password))
    user = get_user_by_username(user.username)
    del user.password
    return user


JWT = NewType(
    "JWT",
    {"username": str, "is_admin": bool, "id": int},
)


def authenticate_user(username: str, password: str):
    """
    verifies weather the user exists in database or not
    and validates the password
    """
    user = get_user_by_username(username=username)
    if not user:
        return None
    else:
        if get_crypto_context().verify(password, user.password):
            return user
        else:
            return None


def create_token(user: auth_schemas.UserSchema) -> JWT:
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
