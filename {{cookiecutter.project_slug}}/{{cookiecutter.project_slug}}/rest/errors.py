from typing import List

from fastapi import HTTPException

from {{cookiecutter.project_slug}} import schemas


class BadRequestError(HTTPException):
    def __init__(self, detail: List[schemas.Error]):
        super().__init__(status_code=400, detail=[d.dict() for d in detail])


OPEN_API_BAD_REQUEST = {
    "model": schemas.ErrorsDetail,
    "description": "Bad Request",
}
