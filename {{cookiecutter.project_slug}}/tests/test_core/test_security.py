from {{cookiecutter.project_slug}}.core import security


def test_password_hashing():
    password = "123456"
    hashed_password = security.get_password_hash(password)

    assert hashed_password != password

    assert security.verify_password(
        plain_password=password, hashed_password=hashed_password
    )
