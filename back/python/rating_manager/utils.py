import logging
from functools import wraps
import time


def retry(exceptions: tuple, max_attempts: int = 5, raise_exc: bool = False, delay: int = 1, show=True):
    def decorator_retry(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            tries = max_attempts
            while tries:
                try:
                    return func(self, *args, **kwargs)
                except exceptions as e:
                    time.sleep(delay)
                    if show:
                        self.logger.warning(e) if self is not None else print(f"Attempt failed: {str(e)}")

                    tries -= 1
                    if raise_exc and not tries:
                        raise

                except Exception as e:
                    if show:
                        self.logger.exception(str(e)) if self is not None else print(f"Attempt failed: {str(e)}")
                    if raise_exc:
                        raise
                    break
            return None

        return inner

    return decorator_retry


def init_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers() is False:
        logger.setLevel(logging.DEBUG)
        channel = logging.StreamHandler()
        channel.setFormatter(logging.Formatter(
            '[%(asctime)s | %(levelname)s] '
            '## [EXTRA: %(filename)s | %(funcName)s | %(lineno)s] ## - %(name)s - %(message)s'))
        channel.setLevel(logging.DEBUG)
        logger.addHandler(channel)

    return logger


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
