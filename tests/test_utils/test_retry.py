import pytest

from app.utils.retry import retry_with_backoff


def test_retry_mechanism():
    """Test retry decorator."""
    attempt_count = 0

    @retry_with_backoff(retries=3, backoff_in_seconds=0)
    def failing_function():
        nonlocal attempt_count
        attempt_count += 1
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        failing_function()

    assert attempt_count == 3
