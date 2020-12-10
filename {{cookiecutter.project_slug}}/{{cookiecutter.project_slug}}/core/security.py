from typing import Optional, Protocol

import jose.jwt

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger()


class _JWTSettings(Protocol):
    jwt_secret: str
    jwt_algorithm: str
    jwt_audience: Optional[str]


def decode_jwt(jwt: str, jwt_settings: _JWTSettings) -> Optional[dict]:
    try:
        return jose.jwt.decode(
            token=jwt,
            key=jwt_settings.jwt_secret,
            algorithms=jwt_settings.jwt_algorithm,
            audience=jwt_settings.jwt_audience,
        )
    except jose.ExpiredSignatureError:
        log.warning("user jwt with expired signature")
    except jose.JOSEError as e:
        log.exception("jose error", jwt=jwt, exc_info=e)

    return None
