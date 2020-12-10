from logging import Logger
from typing import Union

import structlog
from structlog._config import BoundLoggerLazyProxy


def get_logger(*args, **initial_values) -> Union[BoundLoggerLazyProxy, Logger]:
    """Get logger according to configuration."""
    return structlog.get_logger(*args, **initial_values)
