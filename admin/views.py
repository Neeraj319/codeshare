from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from fastapi import Request
from auth.models import User
from .dependencies import (get_super_user, add_user,)
from auth.schema import PydanticUser
from fastapi_pagination import paginate


async def users(request: Request, admin_user: PydanticUser = Depends(get_super_user)):
    """
    get all users from the database
    """
    if admin_user:
        return paginate(
            [PydanticUser(id=user['id'], username=user['username'], is_admin=user['is_admin'])
             for user in await User.all().values("id", "username", "is_admin")])
    else:
        raise HTTPException(
            detail="you are not authorized to access this resource",
            status_code=status.HTTP_403_FORBIDDEN,
        )


async def create_user(user: PydanticUser, request: Request, admin_user: PydanticUser = Depends(get_super_user)):

    return await add_user(user)
