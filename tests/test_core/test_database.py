from app.core.database import get_db, init_db
from app.models.weather import Location


def test_database_initialization(test_db):
    """Test database initialization."""
    init_db()
    assert test_db is not None


def test_get_db():
    """Test database session management."""
    with get_db() as db:
        assert db is not None
        # Try a simple query
        result = db.query(Location).first()
        assert result is None or isinstance(result, Location)


def test_location_creation(test_db, sample_location_data):
    """Test creating a location in database."""
    location = Location(**sample_location_data)
    test_db.add(location)
    test_db.commit()

    saved_location = test_db.query(Location).first()
    assert saved_location.city == sample_location_data["city"]
    assert saved_location.latitude == sample_location_data["latitude"]
