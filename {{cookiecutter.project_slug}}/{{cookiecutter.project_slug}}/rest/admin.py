from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette_exporter import handle_metrics

from {{cookiecutter.project_slug}}.db.checker import check_db_connection
from {{cookiecutter.project_slug}}.logger import get_logger


router = APIRouter()
log = get_logger()


@router.get("/metrics")
def metrics(request: Request):
    """Prometheus metrics."""
    return handle_metrics(request)


@router.get("/version")
async def version(request: Request):
    """Application version."""
    return [{"app": request.app.title, "version": request.app.version}]


@router.get(
    "/readiness",
    responses={
        200: {"description": "Server is ready to process requests"},
        400: {"description": "Server is NOT ready to process requests"},
    },
)
async def readiness(request: Request, full: bool = False):
    """Readiness probe."""
    db_ok = await check_db_connection(request.app.state.db)
    if not db_ok:
        log.error("db check error")

    info = {"db": db_ok}
    all_ok = all(info.values())
    return JSONResponse(
        status_code=200 if all_ok else 400, content=info if full else {}
    )
