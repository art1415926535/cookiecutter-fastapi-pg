from typing import List

from fastapi import APIRouter, Depends, Query

from {{cookiecutter.project_slug}} import schemas
from {{cookiecutter.project_slug}} import use_cases as uc
from {{cookiecutter.project_slug}}.core import auth
from {{cookiecutter.project_slug}}.logger import get_logger

from . import deps, errors


router = APIRouter()
log = get_logger()


@router.get(
    "/",
    operation_id="get_items",
    response_model=List[schemas.ItemOut],
    responses={500: errors.OPEN_API_INTERNAL_ERROR},
)
async def get_items(
    _: auth.User = Depends(deps.user),
    uc_list_items: uc.ListItems = Depends(deps.use_case(uc.ListItems)),
    limit: int = Query(5, gt=0, le=20),
    offset: int = Query(0, ge=0),
) -> List[schemas.ItemOut]:
    """Items list."""

    try:
        items = await uc_list_items(limit, offset)
    except uc.Error as e:
        err = schemas.Error(loc=e.loc, msg=e.user_msg, show=True)
        raise errors.InternalError([err])
    return items
