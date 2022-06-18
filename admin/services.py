from codeshare.settings import get_crypto_context
from auth import schemas as auth_schemas
from codeshare.settings import get_crypto_context
from typing import List, Tuple, Union
from auth import services as auth_services
from codeshare import queries
from code_app import schemas as code_schemas

_T = Tuple[bool, str]


def get_users() -> List[auth_schemas.UserResponseSchema]:
    """
    returns all the users from the database in a list
    """
    data = queries.select(
        table_name="user", column_names=("id", "username", "is_admin")
    )
    users_list = list()
    for user in data:
        users_list.append(dict(zip(("id", "username", "is_admin"), user)))
    return [auth_schemas.UserResponseSchema(**user) for user in users_list]


def add_superuser(user: auth_schemas.UserSchema) -> None:
    """
    takes the UserSchema as parameter and creates the user if
    user if same username is not passes returns None
    """
    if auth_services.get_user_by_username(user.username):
        print("username already exists")
        return
    password = get_crypto_context().hash(user.password)
    queries.insert(
        "user", ("username", "password", "is_admin"), (user.username, password, True)
    )
    print("user added successfully")


def remove_user(user: auth_schemas.UserSchema) -> None:
    """
    takes the user as parameter and removes the user from the database
    """
    queries.delete("user", "where username = %s", (user.username,))


def update_user(
    user: auth_schemas.UserResponseSchema, request_data: auth_schemas.UserUpdateSchema
) -> Union[_T, auth_schemas.UserResponseSchema]:
    """
    user -> User model, request_data -> UserUpdateSchema
    returns the same but updated user
    """
    if auth_services.get_user_by_username(user.username):
        columns = tuple(request_data.dict().keys())
        queries.update(
            table_name="user",
            column_names=columns,
            condition="where username = %s",
            values=(request_data.username, request_data.is_admin),
            condition_values=(user.username,),
        )
        updated_user = auth_services.get_user_by_username(user.username)
        del updated_user.password
        return (True, updated_user)
    return (False, "user does not exist")


def get_all_code_from_db() -> List[code_schemas.CodeSchema]:
    """
    returns Code QuerySet from the db
    """
    data = queries.select(table_name="code")
    code_list = list()
    for code in data:
        code_list.append(
            dict(zip(("id", "text", "language_id", "user_id", "slug"), code))
        )
    # print([code_schemas.CodeSchema(**code) for code in code_list])
    print(code_list)
    return [code_schemas.CodeSchema(**code) for code in code_list]


def add_user(
    user: auth_schemas.UserSchema,
) -> Union[_T, auth_schemas.UserResponseSchema]:
    """
    takes the user pydantic model as parameter (id, username, password, is_admin)
    adds the new user to the database and returns a tuple (bool, User)
    """
    if len(user.password) < 8:
        return (False, "enter a password of length greater than 8")
    if len(user.password) > 80:
        return (False, "your password is too long")
    if auth_services.get_user_by_username(username=user.username):
        return (False, "username already exists")
    password = get_crypto_context().hash(user.password)

    queries.insert(
        "user",
        column_names=("username", "password", "is_admin"),
        values=(user.username, password, user.is_admin),
    )
    user = auth_services.get_user_by_username(username=user.username)
    del user.password
    return (True, user)
