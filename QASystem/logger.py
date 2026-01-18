"""
Centralized logging configuration for PaperBOT.
Provides structured logging with different levels for development and production.
"""

import logging
import sys
from datetime import datetime

# Create logger
logger = logging.getLogger("paperbot")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers
if not logger.handlers:
    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Format: [TIME] [LEVEL] [MODULE] Message
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def get_logger(name: str = "paperbot") -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(f"paperbot.{name}")


# Convenience functions
def log_info(message: str, module: str = "app"):
    """Log info message."""
    get_logger(module).info(message)


def log_error(message: str, module: str = "app", exc_info: bool = False):
    """Log error message."""
    get_logger(module).error(message, exc_info=exc_info)


def log_warning(message: str, module: str = "app"):
    """Log warning message."""
    get_logger(module).warning(message)


def log_debug(message: str, module: str = "app"):
    """Log debug message."""
    get_logger(module).debug(message)


def log_request(method: str, path: str, status: int, duration_ms: float):
    """Log HTTP request."""
    level = logging.INFO if status < 400 else logging.ERROR
    get_logger("http").log(
        level,
        f"{method} {path} - {status} ({duration_ms:.2f}ms)"
    )


def log_upload(filename: str, size_mb: float, success: bool):
    """Log file upload."""
    status = "SUCCESS" if success else "FAILED"
    get_logger("upload").info(f"{status}: {filename} ({size_mb:.2f}MB)")


def log_query(question: str, response_time_ms: float, success: bool):
    """Log Q&A query."""
    status = "SUCCESS" if success else "FAILED"
    # Truncate long questions
    q = question[:50] + "..." if len(question) > 50 else question
    get_logger("query").info(f"{status}: '{q}' ({response_time_ms:.2f}ms)")
