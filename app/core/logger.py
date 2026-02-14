"""Simple logging configuration helper."""

import logging


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger for local/dev usage."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return module-level logger."""
    return logging.getLogger(name)
