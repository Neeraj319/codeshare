from .schemas import LanguageSchema
from .models import Language
from typing import Union
from tortoise.queryset import QuerySet


async def add_language(language: LanguageSchema) -> Union[None, LanguageSchema]:
    """
    adds language to the database if the language already exists then returns none
    """
    if await Language.get_or_none(name=language.name):
        return None
    created_language = await Language.create(name=language.name)
    response_language = LanguageSchema(
        id=created_language.id, name=created_language.name
    )
    return response_language


async def get_language_fromdb(id: int):
    """
    takes id: int returns language of particular id from the database
    or None if it dose not exists
    """
    if language := await Language.get_or_none(id=id):
        return LanguageSchema(name=language.name, id=language.id)

    return None


async def non_schema_get_language(id: int) -> Union[Language, None]:
    """
    returns Language object if exists else None
    """
    return await Language.get_or_none(id=id)


async def all_languages() -> QuerySet[Language]:
    """
    returns queryset of all languages from the database
    """
    return await Language.all()


async def update_language(language: Language, request_data: LanguageSchema) -> Language:
    """
    updates a Language row on the database and returns the updated object

    """
    del request_data.id
    for attr in request_data:
        if getattr(language, attr[0]):
            setattr(language, attr[0], attr[1])
    await language.save()
    return language


async def delete_language(language: Language) -> None:
    """
    deletes language row from the database

    """
    await language.delete()
