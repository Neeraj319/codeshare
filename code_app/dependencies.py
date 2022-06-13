from code_app import schemas as code_schemas
from code_app import models as code_models
from auth import models as auth_models
from language import models as language_models
import string
import random
from typing import Union
from tortoise.queryset import QuerySet


async def get_code_byid(id: int) -> Union[code_models.Code, None]:
    """
    id -> int
    returns code object or None
    """
    return code_models.Code.get_or_none(id=id)


async def generate_slug():
    """
    function to generate unique slug for the code
    """
    chars = string.ascii_letters
    # generating random string
    url = "".join(random.choice(chars) for _ in range(5))
    for code in await code_models.Code.all():
        if code.url == url:
            generate_slug()  # calls itself unless it finds unique slug
            break
    return url


async def add_code(
    code: code_schemas.CodeSchema, user: auth_models.User, language_id: int
) -> Union[code_models.Code, None]:
    """
    this function adds code to the database\n
    if language with the given id is not available then
    returns None
    """
    if language := await language_models.Language.get_or_none(id=language_id):
        return await code_models.Code.create(
            user=user, language=language, url=await generate_slug(), text=code.text
        )
    return language


async def get_code_by_slug(slug: str) -> Union[code_models.Code, None]:
    """
    returns code from the database with the given slug\n
    if not available returns None
    """
    return await code_models.Code.get_or_none(url=slug)


async def update_code(code: code_models.Code, request_data: code_schemas.CodeSchema):
    """
    updates a particular data from the database
    code -> Code Model
    request_data -> data sent during patch request
    """
    if request_data.__dict__.get("id"):
        del request_data.id  # this is necessary cause you can't alert the primary key
    for key, value in request_data:
        if value is not None:
            if (item := getattr(code, key)) and item != value:
                setattr(code, key, value)
    await code.save()
    return code


async def remove_code(code: code_models.Code):
    """
    removes particular code from the database
    """
    await code.delete()


async def get_all_from_db(user: auth_models.User) -> QuerySet[code_models.Code]:
    """
    returns all the code of the particular user
    """
    return await code_models.Code.filter(user_id=user.id)
