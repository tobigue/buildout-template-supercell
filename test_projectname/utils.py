import logging


def log_stderr(func):
    """Decorator for redirecting loggers to stderr."""
    def inner(*args, **kwargs):
        logging.getLogger().handlers = [logging.StreamHandler()]
        return func(*args, **kwargs)
    return inner
