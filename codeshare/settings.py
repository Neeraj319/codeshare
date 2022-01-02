import os
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


DB_URL = "sqlite://data/db.sqlite3"


def get_crypto_context():
    return CryptContext(schemes=[os.environ.get("HASH_FUNCTION")], deprecated="auto")


def get_oauth_2_scheme():
    return OAuth2PasswordBearer(tokenUrl="token")
