import logging
from typing import Literal

import structlog


LogLevels = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


def configure_logging(level: LogLevels) -> None:
    """Configure basic logger."""
    logging.basicConfig(
        format="%(message)s",
        level=level,
        handlers=[StructlogHandler()],
        force=True,
    )


class StructlogHandler(logging.Handler):
    """Feeds all events back into structlog."""

    def __init__(self, *args, **kw):  # noqa: D107
        super(StructlogHandler, self).__init__(*args, **kw)
        self._log = structlog.get_logger()
        self._loggers = {
            50: self._log.critical,
            40: self._log.error,
            30: self._log.warning,
            20: self._log.info,
            10: self._log.debug,
        }

    def emit(self, record) -> None:  # noqa: D102
        msg = record.getMessage()
        exec_info = record.exc_info
        try:
            self._loggers[record.levelno](
                msg, name=record.name, exc_info=exec_info is not None
            )
        except KeyError:
            self._log.info(
                msg,
                name=record.name,
                lvl=record.levelname,
                exc_info=exec_info is not None,
            )
