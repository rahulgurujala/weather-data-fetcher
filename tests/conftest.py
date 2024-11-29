import os

import pytest
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base


@pytest.fixture(scope="session")
def test_db():
    """Create a test database."""
    TEST_DB_URL = "sqlite:///test.db"
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(engine)
    TestSessionLocal = sessionmaker(bind=engine)

    yield TestSessionLocal()

    os.remove("test.db")


@pytest.fixture(scope="session")
def redis_client():
    """Create a Redis client."""
    client = redis.Redis(host="redis", port=6379, db=1)
    yield client
    client.flushdb()


@pytest.fixture
def sample_location_data():
    """Sample location data for testing."""
    return {
        "city": "Test City",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "country": "Test Country",
    }


@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing."""
    return {
        "current_weather": {
            "temperature": 20.5,
            "wind_speed": 5.7,
            "wind_direction": 180,
            "weather_code": 1,
        }
    }
