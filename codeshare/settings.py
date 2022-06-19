""""
this is the main file for every config of the system 
every configuration that the system needs are to be added 
in this file
"""


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
