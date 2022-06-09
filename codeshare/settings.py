import os
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import dotenv
dotenv.load_dotenv()

DB_URL = os.environ['DB_URL']


def get_crypto_context():
    print(os.environ.get('HASH_FUNCTION'))
    return CryptContext(schemes=[os.environ.get("HASH_FUNCTION")], deprecated="auto")


def get_oauth_2_scheme():
    return OAuth2PasswordBearer(tokenUrl="token")


installed_models = ["auth.models", 'language.models', "code.models", ]

TORTOISE_ORM = {
    "connections": {
        "default": os.environ['DB_URL'],
    },
    "apps": {
        app[0:app.find('.')]: {
            "models": [app],
            "default_connection": "default",
        }
        for app in installed_models
    },
}
