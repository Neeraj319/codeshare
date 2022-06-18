from code_app import schemas as code_schemas
import string
import random
from typing import Union, List
from codeshare import queries
from auth import schemas as auth_schemas
from language import services as language_services


def get_code_byid(id: int) -> Union[code_schemas.CodeSchema, None]:
    """
    id -> int
    returns code object or None
    """
    data = queries.select(
        table_name="code", condition="where id = %s", condition_values=(id,)
    )
    if data:
        return code_schemas.CodeSchema(**dict(zip(("id", "slug", "text"), data[0])))
    return None


def get_all_from_db(
    user: auth_schemas.UserResponseSchema,
) -> List[code_schemas.CodeSchema]:
    """
    returns all the code of the particular user
    """
    data = queries.select(
        table_name="code", condition="where user_id = %s", condition_values=(user.id,)
    )
    codes_list = list()
    for code in data:
        codes_list.append(dict(zip(("id", "slug", "text"), code)))
    return [code_schemas.CodeSchema(**code) for code in codes_list]


def generate_slug():
    """
    function to generate unique slug for the code
    """
    chars = string.ascii_letters
    slug = "".join(random.choice(chars) for _ in range(5))

    if code := queries.select(
        table_name="code", condition="where slug = %s", condition_values=(slug,)
    ):
        if code[0][3] == slug:
            generate_slug()  # calls itself unless it finds unique slug
    return slug


def get_code_by_slug(slug: str) -> Union[code_schemas.CodeSchema, None]:
    """
    returns code from the database with the given slug\n
    if not available returns None
    """
    if data := queries.select(
        table_name="code", condition="where slug = %s", condition_values=(slug,)
    ):
        code_dict = dict(zip(("id", "text", "language_id", "slug", "user_id"), data[0]))
        return code_schemas.CodeSchema(**code_dict)


def add_code(
    code: code_schemas.CodeSchema,
    user: auth_schemas.UserResponseSchema,
    language_id: int,
) -> Union[code_schemas.CodeSchema, None]:
    """
    this function adds code to the database\n
    if language with the given id is not available then
    returns None
    """
    if language := language_services.get_language_fromdb(language_id):
        slug = generate_slug()
        print(slug)
        queries.insert(
            table_name="code",
            column_names=("user_id", "language_id", "text", "slug"),
            values=(
                user.id,
                language.id,
                code.text,
                slug,
            ),
        )
        return get_code_by_slug(slug=slug)


def update_code(
    code: code_schemas.CodeSchema, request_data: code_schemas.CodeUpdateSchema
):
    """
    updates a particular data from the database
    code -> Code Model
    request_data -> data sent during patch request
    """
    for key, value in request_data.dict().items():
        if value is None:
            del request_data.__dict__[key]
    if language_services.get_language_fromdb(id=request_data.language_id):
        queries.update(
            table_name="code",
            column_names=tuple(request_data.dict().keys()),
            values=tuple(request_data.dict().values()),
            condition="where slug = %s",
            condition_values=(code.slug,),
        )

        return get_code_by_slug(slug=code.slug)
    return None


def remove_code(code: code_schemas.CodeSchema):
    """
    removes particular code from the database
    """
    queries.delete(
        table_name="code", condition="where slug = %s", condition_values=(code.slug,)
    )
