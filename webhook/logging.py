import inspect
import logging
import sys
from pathlib import Path
from typing import Union

from loguru import logger

from .settings import settings


class InterceptHandler(logging.Handler):
    """Default handler from examples in loguru documentation.

    This handler intercepts all log requests and passes them to loguru.

    For more info see:
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """Propagate logs to loguru.

        Args:
            record: The log record to propagate.
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        # Use inspect.stack() to properly determine the depth
        stack = inspect.stack()
        depth = 0
        logging_file = Path(logging.__file__).resolve() if logging.__file__ else None
        intercept_handler_file = Path(__file__).resolve()
        skipped_files = {logging_file, intercept_handler_file}

        # Walk up the stack to find the first frame outside of logging modules
        for frame_info in stack:
            frame_file = (
                Path(frame_info.filename).resolve() if frame_info.filename else None
            )

            # Skip frames from logging module and InterceptHandler
            if frame_file not in skipped_files and frame_info.function != "emit":
                break

            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_logging() -> None:  # pragma: no cover
    """Configure loguru logger with file rotation and console output."""
    intercept_handler = InterceptHandler()

    # Remove all existing handlers
    logger.remove()

    # Add console handler with configured log level
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True,
    )

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Add file handler with rotation by size
    logger.add(
        log_dir / "webhook.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",  # Rotate when file reaches 10 MB
        retention="30 days",  # Keep logs for 30 days
        compression="zip",  # Compress rotated logs
    )

    # Configure standard logging to use InterceptHandler
    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    # Clear handlers for uvicorn loggers
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn."):
            logging.getLogger(logger_name).handlers = []

    # Change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]

    logger.info("Logging configured successfully")
