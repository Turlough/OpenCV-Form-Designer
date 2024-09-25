import functools
import logging

# Create a global logger
logger = logging.getLogger(__name__)


def log_use(func):
    """Decorator that logs the method name when it's called."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        clz = args[0].__class__.__name__
        method = func.__name__
        logger.debug(f"{clz}.{method}{args[1:]} {kwargs=}")
        return func(*args, **kwargs)

    return wrapper
