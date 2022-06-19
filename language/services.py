from unicodedata import name
from language import schemas as language_schemas
from typing import List, Union
from codeshare import queries


def get_language_fromdb(id: int, db_session):
    """
    takes id: int returns language of particular id from the database
    or None if it dose not exists
    """
    if language := queries.select(
        session=db_session,
        table_name="language",
        condition="where id = %s",
        condition_values=(id,),
    ):
        language_dict = dict(zip(("id", "name"), language[0]))
        return language_schemas.LanguageSchema(**language_dict)
    return None


def get_language_fromdb_name(name: str, db_session):
    """
    takes name: str returns language of particular name from the database
    or None if it dose not exists
    """
    if language := queries.select(
        table_name="language",
        condition="where name = %s",
        condition_values=(name,),
        session=db_session,
    ):
        language_dict = dict(zip(("id", "name"), language[0]))
        return language_schemas.LanguageSchema(**language_dict)
    return None


def add_language(
    language: language_schemas.LanguageSchema,
    user_id: int,
    db_session,
) -> Union[None, language_schemas.LanguageSchema]:
    """
    adds language to the database if the language already exists then returns none
    """
    if get_language_fromdb_name(name=language.name, db_session=db_session):
        return None
    queries.insert(
        table_name="language",
        values=(
            language.name,
            user_id,
        ),
        column_names=(
            "name",
            "user_id",
        ),
        session=db_session,
    )
    language_from_db = get_language_fromdb_name(
        name=language.name, db_session=db_session
    )
    return language_from_db


def all_languages(db_session) -> List[language_schemas.LanguageSchema]:
    """
    returns queryset of all languages from the database
    """
    data = queries.select(
        table_name="language",
        session=db_session,
    )
    languages_list = list()
    for language in data:
        languages_list.append(dict(zip(("id", "name"), language)))
    return [language_schemas.LanguageSchema(**language) for language in languages_list]


def update_language(
    language: language_schemas.LanguageSchema,
    request_data: language_schemas.LanguageSchema,
    db_session,
) -> language_schemas.LanguageSchema:
    """
    updates a Language row on the database and returns the updated object

    """
    queries.update(
        table_name="language",
        column_names=("name",),
        condition="where id = %s",
        values=(request_data.name,),
        condition_values=(language.id,),
        session=db_session,
    )
    return get_language_fromdb(id=language.id, db_session=db_session)


def delete_language(language: language_schemas.LanguageSchema, db_session) -> None:
    """
    deletes language row from the database

    """
    queries.delete(
        table_name="language",
        condition="where id = %s",
        condition_values=(language.id,),
        session=db_session,
    )
