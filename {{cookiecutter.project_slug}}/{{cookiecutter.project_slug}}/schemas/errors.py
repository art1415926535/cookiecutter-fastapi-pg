from typing import List

from pydantic import BaseModel


class Error(BaseModel):
    loc: List[str]
    msg: str
    show: bool


class ErrorsDetail(BaseModel):
    detail: List[Error]
