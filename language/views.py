from typing import List
from fastapi import Depends, HTTPException
from admin.dependencies import get_super_user
from auth.schemas import PydanticUser
from language.models import Language
from .schemas import LanguageSchema
from starlette import status
from language import dependencies


async def post_language(language: LanguageSchema, user: PydanticUser = Depends(get_super_user)):
    if not user:

        raise HTTPException(
            detail="you are not allowed to view this resource",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    created_language = await dependencies.add_language(language=language)
    if not created_language:
        raise HTTPException(
            detail="language with that name already exists",
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    return created_language

# i have not decided yet if i should protect this route or not so
# let's keep it like this for some time


async def get_all_languages() -> List[Language]:
    return await dependencies.all_languages()
