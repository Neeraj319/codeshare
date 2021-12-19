from .models import User
from tortoise.contrib.pydantic import pydantic_model_creator


async def create_user(user: pydantic_model_creator(User)):
    await User.create(**dict(user))
    return user


async def users():
    """
    just a random comment to check for docker stuff
    """
    return await User.all()