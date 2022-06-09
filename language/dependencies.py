from .schemas import LanguageSchema
from .models import Language


async def add_language(language: LanguageSchema):
    if await Language.get_or_none(name=language.name):
        return None
    created_language = await Language.create(name=language.name)
    response_language = LanguageSchema(
        id=created_language.id, name=created_language.name)
    return response_language


async def get_language_fromdb(id: int):
    if language := await Language.get_or_none(id=id):
        return LanguageSchema(name=language.name, id=language.id)

    return None


async def non_schema_get_language(id: int):

    return await Language.get_or_none(id=id)


async def all_languages():
    return await Language.all()


async def update_language(language: Language, request_data=LanguageSchema):
    del request_data.id
    for attr in request_data:
        if getattr(language, attr[0]):
            setattr(language, attr[0], attr[1])
    await language.save()
    return language


async def delete_language(language: Language):
    await language.delete()
