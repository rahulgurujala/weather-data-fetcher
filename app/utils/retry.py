import time
from functools import wraps
from typing import Callable

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def retry_with_backoff(
    retries: int = 3,
    backoff_in_seconds: int = 1,
    max_backoff_in_seconds: int = 30,
    exponential: bool = True,
):
    """
    Retry decorator with exponential backoff.

    Args:
        retries: Maximum number of retries
        backoff_in_seconds: Initial backoff time
        max_backoff_in_seconds: Maximum backoff time
        exponential: Whether to use exponential backoff
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            current_backoff = backoff_in_seconds

            while retry_count < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retry_count += 1
                    if retry_count == retries:
                        logger.error(
                            f"Max retries ({retries}) reached for \
                                {func.__name__}"
                        )
                        raise e

                    logger.warning(
                        f"Attempt {retry_count} failed for {func.__name__}. "
                        f"Retrying in {current_backoff} seconds..."
                    )
                    time.sleep(current_backoff)

                    if exponential:
                        current_backoff = min(
                            current_backoff * 2, max_backoff_in_seconds
                        )

        return wrapper

    return decorator
