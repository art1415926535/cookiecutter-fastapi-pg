from typing import List

from fastapi import HTTPException

from {{cookiecutter.project_slug}} import schemas


class BadRequest(HTTPException):
    def __init__(self, detail: List[schemas.Error]):
        super().__init__(status_code=400, detail=[d.dict() for d in detail])


class PermissionDenied(HTTPException):
    def __init__(self, detail: List[schemas.Error]):
        super().__init__(status_code=403, detail=[d.dict() for d in detail])


class NotFound(HTTPException):
    def __init__(self, detail: List[schemas.Error]):
        super().__init__(status_code=404, detail=[d.dict() for d in detail])


class InternalError(HTTPException):
    def __init__(self, detail: List[schemas.Error]):
        super().__init__(status_code=500, detail=[d.dict() for d in detail])


OPEN_API_BAD_REQUEST = {
    "model": schemas.ErrorsDetail,
    "description": "Bad Request",
}

OPEN_API_PERMISSION = {
    "model": schemas.ErrorsDetail,
    "description": "Permission denied",
}

OPEN_API_NOT_FOUND = {
    "model": schemas.ErrorsDetail,
    "description": "Not Found",
}

OPEN_API_INTERNAL_ERROR = {
    "model": schemas.ErrorsDetail,
    "description": "Internal error",
}
