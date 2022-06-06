import os
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


DB_URL = "sqlite://data/db.sqlite3"


def get_crypto_context():
    return CryptContext(schemes=[os.environ.get("HASH_FUNCTION")], deprecated="auto")


def get_oauth_2_scheme():
    return OAuth2PasswordBearer(tokenUrl="token")


installed_models = ["auth.models", 'core.models', ]

TORTOISE_ORM = {
    "connections": {
        "default": 'sqlite://data/db.sqlite3',
    },
    "apps": {
        app[0:app.find('.')]: {
            "models": [app],
            "default_connection": "default",
        }
        for app in installed_models
    },
}
