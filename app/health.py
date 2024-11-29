import redis
from sqlalchemy import text

from app.config import REDIS_URL
from app.core.database import get_db


def check_database():
    """Check if database is accessible."""
    try:
        with get_db() as db:
            db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def check_redis():
    """Check if Redis is accessible."""
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
        return True
    except Exception:
        return False


def health_check():
    """Perform complete health check."""
    return {
        "status": (
            "healthy" if check_database() and check_redis() else "unhealthy"
        ),
        "database": "connected" if check_database() else "disconnected",
        "redis": "connected" if check_redis() else "disconnected",
    }
