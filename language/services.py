from language import schemas as language_schemas
from language import models as language_models
from typing import Union
from tortoise.queryset import QuerySet


async def add_language(
    language: language_schemas.LanguageSchema,
) -> Union[None, language_schemas.LanguageSchema]:
    """
    adds language to the database if the language already exists then returns none
    """
    if await language_models.Language.get_or_none(name=language.name):
        return None
    created_language = await language_models.Language.create(name=language.name)
    response_language = language_schemas.LanguageSchema(
        id=created_language.id, name=created_language.name
    )
    return response_language


async def get_language_fromdb(id: int):
    """
    takes id: int returns language of particular id from the database
    or None if it dose not exists
    """
    if language := await language_models.Language.get_or_none(id=id):
        return language_schemas.LanguageSchema(name=language.name, id=language.id)

    return None


async def non_schema_get_language(id: int) -> Union[language_models.Language, None]:
    """
    returns Language object if exists else None
    """
    return await language_models.Language.get_or_none(id=id)


async def all_languages() -> QuerySet[language_models.Language]:
    """
    returns queryset of all languages from the database
    """
    return await language_models.Language.all()


async def update_language(
    language: language_models.Language, request_data: language_schemas.LanguageSchema
) -> language_models.Language:
    """
    updates a Language row on the database and returns the updated object

    """
    del request_data.id
    for attr in request_data:
        if getattr(language, attr[0]):
            setattr(language, attr[0], attr[1])
    await language.save()
    return language


async def delete_language(language: language_models.Language) -> None:
    """
    deletes language row from the database

    """
    await language.delete()
