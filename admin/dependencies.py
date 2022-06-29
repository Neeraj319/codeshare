from fastapi.param_functions import Depends
from auth import schemas as auth_schemas
from auth import dependencies as auth_dependencies
from typing import Union
from fastapi import HTTPException, status


async def get_super_user(
    user: auth_schemas.UserSchema = Depends(auth_dependencies.get_user_from_token),
) -> Union[auth_schemas.UserSchema, None]:
    """
    takes the UserSchema schema class
    -> returns if the user is not a superuser
    else returns the user

    """
    CREDENTIAL_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not allowed to view this resource",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if user.is_admin:
        return user
    else:
        raise CREDENTIAL_EXCEPTION
