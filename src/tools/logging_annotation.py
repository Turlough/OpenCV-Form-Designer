import functools
import logging

# Create a global logger
logger = logging.getLogger(__name__)


def log_use(func):
    """Decorator that logs the method name when it's called."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # logger = logging.getLogger(func.__module__)  # Get logger for the module
        logger.info(f"Calling method: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
