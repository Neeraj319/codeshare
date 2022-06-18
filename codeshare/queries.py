from codeshare import db_init
from typing import Union, Tuple


def select(
    table_name: str,
    column_names: Union[Tuple, str] = "*",
    condition: str = "",
    condition_values="",
):
    query = "SELECT "
    if isinstance(column_names, tuple):
        query = query + ", ".join(column_names)
    else:
        query += "*"
    query += f' FROM "{table_name}" {condition}'

    with db_init.DBConnector() as conn:
        conn.curr.execute(query=query, vars=condition_values)
        return conn.curr.fetchall()


def insert(table_name: str, column_names: Tuple, values: Tuple):
    if len(column_names) != len(values):
        print("values and columns miss match")
        return
    query = "INSERT INTO " + f'"{table_name}"'
    query += "(" + ",".join(column_names) + ")"
    query += " VALUES (" + ",".join(["%s"] * len(values)) + ")"
    with db_init.DBConnector() as conn:
        conn.curr.execute(query, values)
        conn.connection.commit()
        print(f"{table_name} added")


def delete(table_name: str, condition: str, condition_values: Tuple):
    query = "DELETE FROM " + f'"{table_name}"'
    query += condition
    with db_init.DBConnector() as conn:
        conn.curr.execute(query, condition_values)
        conn.connection.commit()
        print(f"{table_name} deleted")


def update(
    table_name: str,
    column_names: Tuple,
    values: Tuple,
    condition: str,
    condition_values: Tuple,
):
    """
    UPDATE table_name SET {column_names} = {values} WHERE {condition} = {condition_values}
    """
    query = "UPDATE " + f'"{table_name}" SET '
    for index, colum_name in enumerate(column_names):
        query += f" {colum_name} = {'%s' if index == len(column_names) - 1 else '%s,'} "
    query += f"{condition}"
    with db_init.DBConnector() as conn:
        conn.curr.execute(query, values + condition_values)
        conn.connection.commit()
        print(f"{table_name} updated")
