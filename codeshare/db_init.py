from tortoise import Tortoise
from auth import schemas
from admin import dependencies
from codeshare.settings import DB_URL, installed_models


class DBConnector:
    """
    context manager for database connection
    """

    def __init__(self, db_url, modules) -> None:
        self.db_url = db_url
        self.modules = modules

    async def __aenter__(self):
        await Tortoise.init(db_url=self.db_url, modules=self.modules)

    async def __aexit__(self, exc_type, exc, tb):
        await Tortoise.close_connections()


async def main():
    """
    function to make connection to the database
    """
    await Tortoise.init(db_url=DB_URL, modules={"models": installed_models})


async def close_db_connection():
    """
    closes connection from the database
    """
    await Tortoise.close_connections()


async def create_super_user(username, password):
    """ "
    this function creates superuser on the databse
    """

    await main()
    user = schemas.UserSchema(username=username, password=password, is_admin=True)
    await dependencies.add_superuser(user)
    await close_db_connection()


async def create_tables():
    """
    this function creates tables on the database
    """
    await main()
    await Tortoise.generate_schemas()
    await close_db_connection()
    print("created tables successfully")
