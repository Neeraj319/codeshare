from fastapi.param_functions import Depends
from .models import User
from fastapi import status, HTTPException
from passlib.context import CryptContext
import os
from fastapi.security import OAuth2PasswordBearer
from .schema import PydanticUser
from datetime import datetime, timedelta
from jose import JWTError, jwt


pwd = CryptContext(schemes=[os.environ.get("HASH_FUNCTION")], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def add_user(user: PydanticUser) -> User:
    if len(user.password) < 8:
        raise HTTPException(
            detail="enter a password of length greater than 8",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if len(user.password) > 80:
        raise HTTPException(
            detail="password too long",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    if await User.get_or_none(username=user.username):
        raise HTTPException(
            detail="username already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    password = pwd.hash(user.password)
    created_user = await User.create(username=user.username, password=password)
    return created_user


async def authenticate_user(username: str, password: str):
    if user := await User.get_or_none(username=username):
        if not pwd.verify(password, user.password):
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


async def get_user_from_token(token: str = Depends(oauth2_scheme)):
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
