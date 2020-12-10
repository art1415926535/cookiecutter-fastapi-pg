from typing import Optional

from pydantic import BaseModel


class ItemOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: int
