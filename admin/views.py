from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from fastapi import Request
from .dependencies import (get_super_user, add_user, get_users)
from auth.schema import PydanticUser
from fastapi_pagination import paginate


async def users(request: Request, admin_user: PydanticUser = Depends(get_super_user)):
    """
    get all users from the database
    """
    if admin_user:
        return paginate(await get_users())
    else:
        raise HTTPException(
            detail="you are not authorized to access this resource",
            status_code=status.HTTP_403_FORBIDDEN,
        )


async def create_user(user: PydanticUser, request: Request, admin_user: PydanticUser = Depends(get_super_user)):

    return await add_user(user)
