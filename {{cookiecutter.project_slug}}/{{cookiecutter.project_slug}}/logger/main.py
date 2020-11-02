from logging import Logger
from typing import Literal, Protocol, Union, cast

import structlog
from structlog._config import BoundLoggerLazyProxy

from . import logging_setup, structlog_setup


LowerLogLevels = Literal["critical", "error", "warning", "info", "debug"]
UpperLogLevels = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


class _LoggerSettings(Protocol):
    log_level: LowerLogLevels = "error"
    log_type: Literal["kv", "json", "console"] = "kv"
    log_time_iso_format: bool
    log_utc: bool


def configure(logger_settings: _LoggerSettings) -> None:
    """Configure loggers."""
    upper_log_level = cast(UpperLogLevels, logger_settings.log_level.upper())

    structlog_setup.configure_structlog(
        renderer=logger_settings.log_type,
        time_iso_format=logger_settings.log_time_iso_format,
        utc=logger_settings.log_utc,
    )
    logging_setup.configure_logging(upper_log_level)


def get_logger(*args, **initial_values) -> Union[BoundLoggerLazyProxy, Logger]:
    """Get logger according to configuration."""
    return structlog.get_logger(*args, **initial_values)
