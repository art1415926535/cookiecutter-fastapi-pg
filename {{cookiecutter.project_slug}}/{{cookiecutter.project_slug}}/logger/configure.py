import logging
import os

import structlog
from dotenv import load_dotenv
from structlog.contextvars import merge_contextvars


load_dotenv()


def bool_var(name, default=None):
    return os.getenv(name, default).lower() in ("true", "t", "1")


LOG_LEVEL = os.getenv("LOG_LEVEL", "error").lower()
LOG_TYPE = os.getenv("LOG_TYPE", "json").lower()
LOG_TIME_ISO_FORMAT: bool = bool_var("LOG_TIME_ISO_FORMAT", "false")
LOG_UTC: bool = bool_var("LOG_UTC", "true")


_renderers = {
    "json": structlog.processors.JSONRenderer(),
    "kv": structlog.processors.KeyValueRenderer(),
    "console": structlog.dev.ConsoleRenderer(),
}

shared_processors = [
    merge_contextvars,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.format_exc_info,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(
        fmt="iso" if LOG_TIME_ISO_FORMAT else None,
        utc=LOG_UTC,
        key="ts",
    ),
]
structlog_processors = shared_processors + [
    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
]
structlog.configure(
    processors=structlog_processors,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

formatter = structlog.stdlib.ProcessorFormatter(
    processor=_renderers[LOG_TYPE], foreign_pre_chain=shared_processors
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(LOG_LEVEL.upper())
