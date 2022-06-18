from language import schemas as language_schemas
from typing import List, Union
from codeshare import queries


def get_language_fromdb(id: int):
    """
    takes id: int returns language of particular id from the database
    or None if it dose not exists
    """
    if language := queries.select(
        table_name="language", condition="where id = %s", condition_values=(id,)
    ):
        language_dict = dict(zip(("id", "name"), language[0]))
        return language_schemas.LanguageSchema(**language_dict)
    return None


def get_language_fromdb_name(name: str):
    """
    takes name: str returns language of particular name from the database
    or None if it dose not exists
    """
    if language := queries.select(
        table_name="language", condition="where name = %s", condition_values=(name,)
    ):
        language_dict = dict(zip(("id", "name"), language[0]))
        return language_schemas.LanguageSchema(**language_dict)
    return None


def add_language(
    language: language_schemas.LanguageSchema,
) -> Union[None, language_schemas.LanguageSchema]:
    """
    adds language to the database if the language already exists then returns none
    """
    if get_language_fromdb_name(language.name):
        return None
    queries.insert(
        table_name="language", values=(language.name,), column_names=("name",)
    )
    language_from_db = get_language_fromdb_name(language.name)
    return language_from_db


def all_languages() -> List[language_schemas.LanguageSchema]:
    """
    returns queryset of all languages from the database
    """
    data = queries.select(table_name="language")
    languages_list = list()
    for language in data:
        languages_list.append(dict(zip(("id", "name"), language)))
    return [language_schemas.LanguageSchema(**language) for language in languages_list]


def update_language(
    language: language_schemas.LanguageSchema,
    request_data: language_schemas.LanguageSchema,
) -> language_schemas.LanguageSchema:
    """
    updates a Language row on the database and returns the updated object

    """
    queries.update(
        table_name="language",
        column_names=tuple(request_data.dict().keys()),
        condition="where id = %s",
        values=(request_data.name,),
        condition_values=(language.id,),
    )
    return get_language_fromdb(language.id)


def delete_language(language: language_schemas.LanguageSchema) -> None:
    """
    deletes language row from the database

    """
    queries.delete(
        table_name="language",
        condition="where id = %s",
        condition_values=(language.id,),
    )
