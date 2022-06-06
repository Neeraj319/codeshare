from tortoise import Tortoise, run_async
from .settings import DB_URL, installed_models
from auth import dependencies, schema


class DBConnector:
    def __init__(self, db_url, modules) -> None:
        self.db_url = db_url
        self.modules = modules

    async def __aenter__(self):
        await Tortoise.init(db_url=self.db_url, modules=self.modules)

    async def __aexit__(self, exc_type, exc, tb):
        await Tortoise.close_connections()


async def main():
    await Tortoise.init(db_url=DB_URL, modules={"models": installed_models})


async def close_db_connection():
    await Tortoise.close_connections()


async def create_super_user(username, password):
    await main()
    user = schema.PydanticUser(
        username=username, password=password, is_admin=True)
    await dependencies.add_user(user)
    await close_db_connection()


async def create_tables():
    await Tortoise.init(db_url=DB_URL, modules={"models": installed_models})
    await Tortoise.generate_schemas(safe=True)
    # await create_super_user("admin", "admin")
    await Tortoise.close_connections()
    print('created tables successfully')
