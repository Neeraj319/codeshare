from code_app.schemas import CodeSchema
from .models import Code
from auth.models import User
from language.models import Language
import string
import random


async def get_code_byid(id: int):
    return Code.get_or_none(id=id)


async def generate_url():
    chars = string.ascii_letters
    url = "".join(random.choice(chars) for _ in range(5))
    for code in await Code.all():
        if code.url == url:
            generate_url()
            break
    return url


async def add_code(code: CodeSchema, user: User, language_id: int):
    if language := await Language.get_or_none(id=language_id):
        return await Code.create(user=user, language=language, url=await generate_url(), text=code.text)
    return language
