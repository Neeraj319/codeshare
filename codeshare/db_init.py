from tortoise import Tortoise


class DBConnector:
    def __init__(self, db_url, modules) -> None:
        self.db_url = db_url
        self.modules = modules

    async def __aenter__(self):
        await Tortoise.init(db_url=self.db_url, modules=self.modules)

    async def __aexit__(self, exc_type, exc, tb):
        await Tortoise.close_connections()


async def main():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["home.models"]}
    )


async def close_db_connection():
    await Tortoise.close_connections()


async def create_table():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["home.models"]}
    )
    await Tortoise.generate_schemas(safe=True)
