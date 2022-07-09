import psycopg2
from codeshare import settings


class DBConnector:
    """
    context manager for database connection
    """

    def __init__(self) -> None:
        self.connection = psycopg2.connect(settings.DB_URL)
        self.curr = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.curr.close()
        self.connection.close()

    def close(self):
        self.curr.close()
        self.connection.close()


def db_connection() -> DBConnector:
    """
    returns the database connection object
    """
    return DBConnector()


def create_super_user(username, password):
    """
    this function creates superuser on the databse
    """

    # this is done manually to prevent circular imports
    hash = settings.get_crypto_context().hash(password)
    with DBConnector() as conn:
        # check if username already exists or not
        conn.curr.execute('SELECT * FROM "user" WHERE username = %s', (username,))
        data = conn.curr.fetchone()
        if not data:
            conn.curr.execute(
                'insert into "user" (username, password, is_admin) values (%s, %s, %s)',
                (username, hash, True),
            )
            conn.connection.commit()
            return
        print("username already exists")


def create_tables(path: str = "/app/schema.sql"):
    """
    this function creates tables on the database
    """
    with open(path, "r") as f:
        schema = f.read()
        with DBConnector() as conn:
            conn.curr.execute(schema)
            conn.connection.commit()
    print("created tables successfully")
