from admin import services
from auth import schemas, services as auth_services
from codeshare import db_init
import pytest
import faker


@pytest.fixture(scope="module")
def db_connection():
    return db_init.db_connection()


@pytest.fixture(scope="module")
def fakerInstance():
    return faker.Faker()


@pytest.fixture(scope="module")
def user_schema_admin(fakerInstance):
    return schemas.UserSchema(
        username=fakerInstance.user_name(),
        password=fakerInstance.password(),
        is_admin=True,
    )


@pytest.fixture(scope="module")
def user_schema(fakerInstance):
    return schemas.UserSchema(
        username=fakerInstance.user_name(),
        password=fakerInstance.password(),
        is_admin=False,
    )


@pytest.mark.run(order=1)
def test_add_user(
    user_schema: schemas.UserSchema,
    user_schema_admin: schemas.UserSchema,
    db_connection,
):
    state, _ = services.add_user(
        user=user_schema_admin,
        db_session=db_connection,
    )
    assert state == True
    state, _ = services.add_user(
        user=user_schema,
        db_session=db_connection,
    )
    assert state == True


@pytest.mark.run(order=2)
def test_update_user(
    user_schema: schemas.UserSchema,
    user_schema_admin: schemas.UserSchema,
    db_connection,
    fakerInstance,
):
    user_name = fakerInstance.user_name()
    update_user_schema = schemas.UserUpdateSchema(username=user_name, is_admin=True)
    user_from_db = auth_services.get_user_by_username(
        db_session=db_connection, username=user_schema.username
    )
    user_schema.username = user_name
    state, _ = services.update_user(
        db_session=db_connection,
        user=user_from_db,
        request_data=update_user_schema,
    )
    assert state == True

    user_name = fakerInstance.user_name()
    update_user_schema = schemas.UserUpdateSchema(username=user_name, is_admin=False)
    user_from_db = auth_services.get_user_by_username(
        db_session=db_connection, username=user_schema_admin.username
    )
    user_schema_admin.username = user_name
    state, _ = services.update_user(
        db_session=db_connection,
        user=user_from_db,
        request_data=update_user_schema,
    )
    assert state == True


@pytest.mark.run(order=3)
def test_delete_user(
    user_schema: schemas.UserSchema,
    user_schema_admin: schemas.UserSchema,
    db_connection,
):
    state = services.remove_user(
        user=user_schema,
        db_session=db_connection,
    )
    assert state == True
    state = services.remove_user(
        user=user_schema_admin,
        db_session=db_connection,
    )
    assert state == True
