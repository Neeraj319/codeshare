import psycopg2

from auth import schemas as auth_schemas

from admin import services as admin_services
from codeshare import settings


class DBConnector:
    """
    context manager for database connection
    """

    def __init__(self) -> None:
        self.connection = psycopg2.connect(settings.DB_URL)
        self.curr = self.connection.cursor()

    def __enter__(self):
        print("enter")

    def __exit__(self, exc_type, exc, tb):
        self.curr.close()
        self.connection.close()

    def close(self):
        self.curr.close()
        self.connection.close()


def db_connection():
    return DBConnector()


def create_super_user(username, password):
    """
    this function creates superuser on the databse
    """

    user = auth_schemas.UserSchema(username=username, password=password, is_admin=True)
    admin_services.add_superuser(user)


def create_tables():
    """
    this function creates tables on the database
    """
    with open("/app/schema.sql", "r") as f:
        schema = f.read()
        with DBConnector() as conn:
            conn.curr.execute(schema)
            conn.connection.commit()

    print("created tables successfully")
