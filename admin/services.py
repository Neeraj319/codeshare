from codeshare.settings import get_crypto_context
from auth import models as auth_models
from auth import schemas as auth_schemas
from codeshare.settings import get_crypto_context
from typing import List, Tuple, Union
from tortoise.queryset import QuerySet
from code_app import models as codemodels

_T = Tuple[bool, str]


async def get_users() -> List[auth_schemas.UserResponseSchema]:
    """
    returns all the users from the database in a list
    """
    users = await auth_models.User.all().values("id", "username", "is_admin")
    return [auth_schemas.UserResponseSchema(**user) for user in users]


async def add_superuser(user: auth_schemas.UserSchema) -> None:
    """
    takes the UserSchema as parameter and creates the user if
    user if same username is not passes returns None
    """
    if await auth_models.User.get_or_none(username=user.username):
        print("username already exists")
        return
    password = get_crypto_context().hash(user.password)
    await auth_models.User.create(
        username=user.username, password=password, is_admin=True
    )


async def remove_user(user: auth_models.User) -> None:
    """
    takes the user as parameter and removes the user from the database
    """
    await user.delete()


async def update_user(
    user: auth_models.User, request_data: auth_schemas.UserUpdateSchema
) -> Union[_T, auth_schemas.UserResponseSchema]:
    """
    user -> User model, request_data -> UserUpdateSchema
    returns the same but updated user
    """
    # deleting password cause its not good to update password from here
    if hasattr(request_data, "password"):
        del request_data.password

    for key, value in request_data:
        if (item := getattr(user, key)) and item != value:
            if key == "username" and value == "":
                return (False, "username cannot be empty")
            setattr(user, key, value) if value else ...
    await user.save()
    return (True, auth_schemas.UserResponseSchema(**user.__dict__))


async def get_all_from_db() -> QuerySet[codemodels.Code]:
    """
    returns Code QuerySet from the db
    """
    return await codemodels.Code.all()


async def add_user(
    user: auth_schemas.UserSchema,
) -> Union[_T, auth_schemas.UserResponseSchema]:
    """
    takes the user pydantic model as parameter (id, username, password, is_admin)
    adds the new user to the database and returns a tuple (bool, User)
    """
    if len(user.password) < 8:
        return (False, "enter a password of length greater than 8")
    if len(user.password) > 80:
        return (False, "your password is too long")
    if await auth_models.User.get_or_none(username=user.username):
        return (False, "username already exists")
    password = get_crypto_context().hash(user.password)

    created_user = await auth_models.User.create(
        username=user.username, password=password, is_admin=user.is_admin
    )

    return (True, auth_schemas.UserResponseSchema(**created_user.__dict__))
