import pytest
from databases import Database

from {{cookiecutter.project_slug}} import schemas
from {{cookiecutter.project_slug}} import use_cases as uc
from {{cookiecutter.project_slug}}.core import security


@pytest.mark.asyncio
async def test_create_user(db: Database):
    create_user = uc.CreateUser(db)
    email = "a@a.aa"
    password = "123456"

    new_user_data = schemas.UserCreate(
        email=email,
        password=password,
    )
    await create_user(new_user_data)

    query = (
        "SELECT first_name, last_name, email, password "
        "FROM users WHERE email = :email"
    )
    user_from_db = await db.fetch_one(query, values={"email": email})

    assert user_from_db is not None
    assert user_from_db["first_name"] is None
    assert user_from_db["last_name"] is None
    assert user_from_db["email"] == email
    assert security.verify_password(password, user_from_db["password"])
