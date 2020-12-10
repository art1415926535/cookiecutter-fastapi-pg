from typing import Callable, Optional, Type

import sentry_sdk
from databases import Database
from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuth2, OAuthFlows
from fastapi.security import OAuth2AuthorizationCodeBearer

from {{cookiecutter.project_slug}}.core import auth, security
from {{cookiecutter.project_slug}}.settings import ServiceSettings
from {{cookiecutter.project_slug}}.use_cases import DatabaseUseCase


def service_settings(request: Request) -> ServiceSettings:
    return request.app.state.settings


def db(request: Request) -> Database:
    return request.app.state.db


def use_case(
    repository_type: Type[DatabaseUseCase],
) -> Callable[[], DatabaseUseCase]:
    def wrap(db_: Database = Depends(db)) -> DatabaseUseCase:
        return repository_type(db_)

    return wrap


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="", tokenUrl="", auto_error=False
)


def update_oauth2_scheme(authorization_url="", token_url=""):
    oauth2_scheme.model = OAuth2(
        flows=OAuthFlows(
            authorizationCode={
                "authorizationUrl": authorization_url,
                "tokenUrl": token_url,
                "refreshUrl": token_url,
            }
        )
    )


def user_or_none(
    token: Optional[str] = Depends(oauth2_scheme),
    settings: ServiceSettings = Depends(service_settings),
) -> Optional[auth.User]:
    if token is None:
        return None

    jwt = security.decode_jwt(token, settings)
    user_ = auth.User.from_jwt(jwt)
    if user_ is None:
        return user_

    sentry_sdk.set_user(
        {"id": user_.uuid, "name": user_.name, "roles": user_.roles}
    )
    return user_


def user(user_maybe: Optional[auth.User] = Depends(user_or_none)) -> auth.User:
    if user_maybe is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_maybe
