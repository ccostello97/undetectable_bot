"""Centralized logging configuration for undetectable bot."""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure logging for the entire application.

    Args:
        level: The logging level to use. Defaults to INFO.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
