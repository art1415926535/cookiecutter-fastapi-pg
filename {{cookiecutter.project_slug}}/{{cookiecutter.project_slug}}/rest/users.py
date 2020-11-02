from fastapi import APIRouter, Depends, Query, status

from {{cookiecutter.project_slug}} import schemas
from {{cookiecutter.project_slug}} import use_cases as uc
from {{cookiecutter.project_slug}}.logger import get_logger

from . import deps, errors


router = APIRouter()
log = get_logger()


@router.get("/", response_model=schemas.Users)
async def get_users_list(
    list_users: uc.ListUsers = Depends(deps.use_case(uc.ListUsers)),
    limit: int = Query(5, gt=0, le=20),
    offset: int = Query(0, ge=0),
) -> schemas.Users:
    """Users list."""

    users = await list_users(limit, offset)
    return users


@router.post(
    "/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    responses={400: errors.OPEN_API_BAD_REQUEST},
)
async def create_new_user(
    user_create: schemas.UserCreate,
    create_user: uc.CreateUser = Depends(deps.use_case(uc.CreateUser)),
) -> schemas.User:
    """Create user."""
    try:
        user = await create_user(user_create)
    except uc.UseCaseError as e:
        err = schemas.Error(loc=["body"] + e.loc, msg=str(e), show=True)
        raise errors.BadRequestError([err])
    return user
