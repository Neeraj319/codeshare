

from .schemas import LanguageSchema
from .models import Language


async def add_language(language: LanguageSchema):
    if await Language.get_or_none(name=language.name):
        return None
    created_language = await Language.create(name=language.name)
    response_language = LanguageSchema(
        id=created_language.id, name=created_language.name)
    return response_language


async def get_language(id: int):
    if language := await Language.get_or_none(id=id):
        return LanguageSchema(name=language.name, id=language.id)

    return None


async def all_languages():
    return await Language.all()
