from fastapi.param_functions import Depends
from .models import User
from fastapi import status, HTTPException
import os
from .schema import PydanticUser
from datetime import datetime, timedelta
from jose import JWTError, jwt
from codeshare.settings import get_crypto_context, get_oauth_2_scheme


async def authenticate_user(username: str, password: str):
    if user := await User.get_or_none(username=username):
        if not get_crypto_context().verify(password, user.password):
            return False
        return user


async def create_token(user):
    to_encode = dict(user)
    del to_encode["password"]

    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ["SECRET_KEY"], algorithm=os.environ.get("ALGORITHM")
    )
    return encoded_jwt


async def get_user_from_token(token: str = Depends(get_oauth_2_scheme())):
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
    if user := await User.get(username=username):
        return user
    else:
        raise credentials_exception


async def get_user(user: PydanticUser = Depends(get_user_from_token)):
    return user
