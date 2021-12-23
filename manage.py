import sys
from codeshare.db_init import create_tables
from tortoise import run_async

if sys.argv[1] == "create_tables":

    run_async(create_tables())
