import sys
from codeshare.db_init import create_tables
from tortoise import run_async
import os


def create_app(directory):
    os.system(
        f"mkdir {directory} && cd {directory} && touch __init__.py url.py views.py models.py dependency.py schema.py"
    )


try:
    args = sys.argv
    if len(args) == 2:
        if sys.argv[1] == "create_tables":
            run_async(create_tables())
    elif len(args) == 3:
        if sys.argv[1] == "createapp" and sys.argv[2]:
            create_app(sys.argv[2])

        else:
            print("provide an app name")
except Exception as e:
    print("invalid arguments")
