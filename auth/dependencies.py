from fastapi.param_functions import Depends
from fastapi import status, HTTPException
import os
from jose import JWTError, jwt
from codeshare.settings import get_oauth_2_scheme
from typing import Union
from auth import schemas as auth_schmeas
from auth import services as auth_services


async def get_user_from_token(
    token: str = Depends(get_oauth_2_scheme()),
) -> Union[auth_schmeas.UserResponseSchema, None]:
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
    if user := auth_services.get_user_by_username(username):
        del user.password
        return user
    else:
        raise credentials_exception
