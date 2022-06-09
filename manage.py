import sys
from codeshare.db_init import create_tables, create_super_user
from tortoise import run_async
import os


def create_app(directory):
    os.system(
        f"mkdir {directory} && cd {directory} && touch __init__.py urls.py views.py models.py dependencies.py schemas.py"
    )


try:
    first, main, *extra = sys.argv
except ValueError:
    pass


def command_create_tables(*args):
    run_async(create_tables())


def createsuperuser(*args):
    username = input('username: ')
    password = input('password:')
    run_async(create_super_user(username, password))


def createsuperuserauto(*args):
    run_async(create_super_user('123', '123'))


commands = {
    'create_tables': [command_create_tables, "creates table on the database"],
    "createsuperuser": [createsuperuser, "creates a super user by asking username and password"],
    "createsuperuserauto": [createsuperuserauto, "creates a superuser without asking username or password"],
    "create_app": [create_app, "creates an app to the current working directory"],
}


def manage_help():
    print(
        """
        Welcome to manage.py help down is the list of commands you can use 
        """
    )
    for key, value in commands.items():
        print(f"{key} | {value[1]}")


commands['help'] = [manage_help, "shows all the commands available"]

if values := commands.get(main):
    values[0](*extra)
else:
    print('no such command found run "help" for more')
