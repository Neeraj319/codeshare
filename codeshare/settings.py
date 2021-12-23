import os
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

DB_URL = "sqlite://data/db.sqlite3"

pwd = CryptContext(schemes=[os.environ.get("HASH_FUNCTION")], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
