from codeshare.settings import get_crypto_context
from fastapi.param_functions import Depends
from auth.models import User
from auth.schemas import PydanticUser, PydanticUserResponseModel, UserUpdateSchema
from codeshare.settings import get_crypto_context
from auth.dependencies import get_user_from_token
from typing import List, Tuple, Union

_T = Tuple[bool, str]


async def add_user(user: PydanticUser) -> Union[_T, User]:
    """
    takes the user pydantic model as parameter (id, username, password, is_admin)
    adds the new user to the database and returns a tuple (bool, User)
    """
    if len(user.password) < 8:
        return (False, "enter a password of length greater than 8")
    if len(user.password) > 80:
        return (False, "your password is too long")
    if await User.get_or_none(username=user.username):
        return (False, "username already exists")
    password = get_crypto_context().hash(user.password)

    created_user = await User.create(
        username=user.username, password=password, is_admin=user.is_admin
    )
    user = {
        "id": created_user.id,
        "username": created_user.username,
        "is_admin": created_user.is_admin,
    }
    return (True, user)


async def get_super_user(
    user: PydanticUser = Depends(get_user_from_token),
) -> Union[PydanticUser, None]:
    """
    takes the PydanticUser schema class
    -> returns if the user is not a superuser
    else returns the user

    """
    if user.is_admin:
        return user
    else:
        return None


async def get_users() -> List[PydanticUserResponseModel]:
    """
    returns all the users from the database in a list
    """
    users = await User.all().values("id", "username", "is_admin")
    return [PydanticUserResponseModel(**user) for user in users]


async def add_superuser(user: PydanticUser) -> None:
    """
    takes the PydanticUser as parameter and creates the user if
    user if same username is not passes returns None
    """
    if await User.get_or_none(username=user.username):
        print("username already exists")
        return
    password = get_crypto_context().hash(user.password)
    await User.create(username=user.username, password=password, is_admin=True)


async def remove_user(user: User) -> None:
    """
    takes the user as parameter and removes the user from the database
    """
    await user.delete()


async def update_user(user: User, request_data: UserUpdateSchema) -> _T:
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
    return (True, PydanticUserResponseModel(**user.__dict__))
