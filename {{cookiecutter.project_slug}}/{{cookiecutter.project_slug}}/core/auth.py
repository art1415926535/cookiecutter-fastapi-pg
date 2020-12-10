from typing import Final, List, Optional
from uuid import UUID

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger()


class User:
    user_uuid_jwt_field: Final[str] = "sub"

    def __init__(self, uuid: UUID, name: str, roles: List[str]):
        self.uuid: Final[UUID] = uuid
        self.name: Final[str] = name
        self.roles: Final[List[str]] = roles

    @property
    def is_admin(self):
        return "admin" in self.roles

    @classmethod
    def from_jwt(cls, payload: Optional[dict]) -> "Optional[User]":
        if payload is None:
            return None

        if cls.user_uuid_jwt_field not in payload:
            log.error("sub not found in jwt", jwt_payload=payload)
            return None

        try:
            user_uuid = UUID(payload[cls.user_uuid_jwt_field])
            roles = payload["realm_access"]["roles"]
            name = payload["name"]
        except Exception as e:
            log.exception("extraction user info error", exc_info=e)
            return None

        return cls(uuid=user_uuid, name=name, roles=roles)
