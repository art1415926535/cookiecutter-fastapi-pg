from typing import Callable, Dict, List, Literal, Optional

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger()

LogLevels = Literal["critical", "error", "warning", "info", "debug"]

_loggers: Dict[str, Callable[..., None]] = {
    "critical": log.critical,
    "error": log.error,
    "warning": log.warning,
    "info": log.info,
    "debug": log.debug,
}


class _LoggedError(Exception):
    """Base error with logger."""

    def __init__(
        self,
        message: str,
        loc: List[str] = None,
        log_level: Optional[LogLevels] = "error",
        **kwargs,
    ):
        if loc is None:
            loc = []
        self.loc: List[str] = loc

        if log_level is not None:
            _loggers[log_level](message, **kwargs)

        super().__init__(message)


class UseCaseError(_LoggedError):
    """User-friendly error message."""

    pass
