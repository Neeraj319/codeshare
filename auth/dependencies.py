from fastapi.param_functions import Depends
from auth import models as auth_models
from fastapi import status, HTTPException
import os
from jose import JWTError, jwt
from codeshare.settings import get_oauth_2_scheme
from typing import Union


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
