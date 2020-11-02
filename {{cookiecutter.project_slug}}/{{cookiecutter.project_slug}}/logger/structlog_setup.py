from typing import Literal

import structlog


RendererTypes = Literal["json", "kv", "console"]
_renderers = {
    "json": structlog.processors.JSONRenderer(),
    "kv": structlog.processors.KeyValueRenderer(),
    "console": structlog.dev.ConsoleRenderer(),
}


def configure_structlog(
    renderer: RendererTypes, time_iso_format: bool, utc: bool
) -> None:
    """Configure structlog."""
    processors = [
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(
            fmt="iso" if time_iso_format else None, utc=utc, key="ts"
        ),
        _renderers[renderer],
    ]

    structlog.configure(processors=processors, cache_logger_on_first_use=True)
