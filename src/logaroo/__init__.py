"""Logaroo - Bouncy Logging in Python."""

import os
from zoneinfo import ZoneInfo

from logaroo.logger import Logger

logger = Logger(
    level=os.getenv("LOGAROO_LEVEL", "info"),
    template=os.getenv(
        "LOGAROO_TEMPLATE", "[green]{time}[/] | {level:<8} | {color}{icon} {message}"
    ),
    timestamp_format=os.getenv("LOGAROO_TIMESTAMP_FORMAT", "%Y-%m-%d %H:%M:%S.%f"),
    timezone=ZoneInfo(os.getenv("LOGAROO_TIMEZONE", "UTC")),
)

__all__ = ["Logger", "logger"]

__version__ = "0.1.0"
