from tortoise import run_async
from db_init import create_table


run_async(create_table())
