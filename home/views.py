from .models import User
from tortoise.contrib.pydantic import pydantic_model_creator
from .dependencies import add_user
from .schema import PydanticUser
from fastapi import Depends


async def create_user(user: PydanticUser):
    user_ = Depends(await add_user(user))
    return user_.__dict__["dependency"]


async def users():
    """
    get all users from the database
    """
    return await User.all()
