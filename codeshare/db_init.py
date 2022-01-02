from tortoise import Tortoise
from .settings import DB_URL, installed_models


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


async def create_tables():
    await Tortoise.init(db_url=DB_URL, modules={"models": installed_models})
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()
