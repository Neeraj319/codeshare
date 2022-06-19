from codeshare import db_init
from typing import Union, Tuple


def select(
    session: db_init.DBConnector,
    table_name: str,
    column_names: Union[Tuple, str] = "*",
    condition: str = "",
    condition_values="",
):
    """
    table_name -> table name
    column_names -> column names to be selected
    condition -> condition to be applied
    condition_values -> values of the condition
    SELECT {column_names} FROM {table_name} WHERE {condition} = {condition_values}
    """
    query = "SELECT "
    if isinstance(column_names, tuple):
        query = query + ", ".join(column_names)
    else:
        query += "*"
    query += f' FROM "{table_name}" {condition}'

    session.curr.execute(query=query, vars=condition_values)
    return session.curr.fetchall()


def insert(
    session: db_init.DBConnector,
    table_name: str,
    column_names: Tuple,
    values: Tuple,
):
    """
    table_name -> table name
    column_names -> column names
    values -> values of the columns
    INSERT INTO {table_name} ({column_names}) VALUES ({values})
    """
    if len(column_names) != len(values):
        print("values and columns miss match")
        return
    query = "INSERT INTO " + f'"{table_name}"'
    query += "(" + ",".join(column_names) + ")"
    query += " VALUES (" + ",".join(["%s"] * len(values)) + ")"

    session.curr.execute(query, values)
    session.connection.commit()
    print(f"{table_name} added")


def delete(
    session: db_init.DBConnector,
    table_name: str,
    condition: str,
    condition_values: Tuple,
):
    """
    table_name -> table name
    condition -> condition to be applied
    condition_values -> values of the condition
    DELETE FROM {table_name} WHERE {condition} = {condition_values}

    """

    query = "DELETE FROM " + f'"{table_name}"'
    query += condition
    session.curr.execute(query, condition_values)
    session.connection.commit()
    print(f"{table_name} deleted")


def update(
    session: db_init.DBConnector,
    table_name: str,
    column_names: Tuple,
    values: Tuple,
    condition: str,
    condition_values: Tuple,
):
    """
    table_name -> table name
    column_names -> column names
    values -> values of the columns to be updated
    condition -> condition to be applied
    condition_values -> values of the condition
    UPDATE table_name SET {column_names} = {values} WHERE {condition} = {condition_values}
    """
    query = "UPDATE " + f'"{table_name}" SET '
    for index, colum_name in enumerate(column_names):
        query += f" {colum_name} = {'%s' if index == len(column_names) - 1 else '%s,'} "
    query += f"{condition}"
    print(query)
    session.curr.execute(query, values + condition_values)
    session.connection.commit()
    print(f"{table_name} updated")
