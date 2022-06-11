import os
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import dotenv

dotenv.load_dotenv()

DB_URL = os.environ["DB_URL"]


def get_crypto_context():
    return CryptContext(schemes=[os.environ.get("HASH_FUNCTION")], deprecated="auto")


def get_oauth_2_scheme():
    return OAuth2PasswordBearer(tokenUrl="token")


installed_models = [
    "auth.models",
    "language.models",
    "code_app.models",
]
