from fastapi.param_functions import Depends
from auth import schemas as auth_schemas
from auth import dependencies as auth_dependencies
from typing import Union


async def get_super_user(
    user: auth_schemas.UserSchema = Depends(auth_dependencies.get_user_from_token),
) -> Union[auth_schemas.UserSchema, None]:
    """
    takes the UserSchema schema class
    -> returns if the user is not a superuser
    else returns the user

    """
    if not user:
        return None
    if user.is_admin:
        return user
    else:
        return None
