from typing import Callable, Dict, List, Literal, Optional

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger()

LogLevels = Literal[
    "critical", "exception", "error", "warning", "info", "debug"
]

_loggers: Dict[str, Callable[..., None]] = {
    "critical": log.critical,
    "exception": log.exception,
    "error": log.error,
    "warning": log.warning,
    "info": log.info,
    "debug": log.debug,
}


class _LoggedError(Exception):
    """Base error with logger."""

    def __init__(
        self,
        msg: str,
        user_msg: Optional[str] = None,
        loc: Optional[List[str]] = None,
        log_level: Optional[LogLevels] = "error",
        **kwargs,
    ):
        if loc is None:
            loc = []
        self.loc: List[str] = loc

        self.user_msg: Optional[str] = user_msg

        if log_level is not None:
            _loggers[log_level](msg, **kwargs)

        super().__init__(msg)


class Error(_LoggedError):
    """Base error."""

    pass


class PermissionDenied(_LoggedError):
    """Permission error."""

    pass


class NotFoundError(_LoggedError):
    """NotFound error."""

    pass
