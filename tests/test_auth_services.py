from auth import services as auth_services
import pytest
import faker
from auth import schemas
from codeshare import db_init


@pytest.fixture(scope="module")
def db_connection():
    return db_init.db_connection()


@pytest.fixture(scope="module")
def fakerInstance():
    return faker.Faker()


@pytest.fixture(scope="module")
def user_schema(fakerInstance):
    return schemas.UserSchema(
        username=fakerInstance.user_name(),
        password=fakerInstance.password(),
        is_admin=False,
    )


def test_add_user(user_schema: schemas.UserSchema, db_connection):
    user = auth_services.add_user(user=user_schema, db_session=db_connection)
    for key, value in user.dict().items():
        if user_schema.dict().get(key):
            assert value == user_schema.dict().get(key)
    user_schema.id = user.id


def test_get_user_by_username(
    user_schema: schemas.UserSchema,
    db_connection,
):
    user = auth_services.get_user_by_username(
        username=user_schema.username, db_session=db_connection
    )
    del user.password
    for key, value in user.dict().items():
        assert value == user_schema.dict().get(key)


def test_get_user_by_id(
    user_schema: schemas.UserSchema,
    db_connection,
):
    user = auth_services.get_user_by_id(
        user_id=user_schema.id, db_session=db_connection
    )
    del user.password
    for key, value in user.dict().items():
        assert value == user_schema.dict().get(key)


def test_authenticate_user(
    user_schema: schemas.UserSchema,
    db_connection,
):
    user = auth_services.authenticate_user(
        username=user_schema.username,
        password=user_schema.password,
        db_session=db_connection,
    )
    del user.password
    for key, value in user.dict().items():
        assert value == user_schema.dict().get(key)


def create_token(
    user_schema: schemas.UserSchema,
    db_connection,
):
    token = auth_services.create_token(
        user=user_schema,
        db_session=db_connection,
    )
    assert token is not None
