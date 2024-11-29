# app/main.py
from pathlib import Path
from app.core.database import init_db
from app.utils.logger import setup_logger
from app.config import LOCATIONS_CSV_PATH
from app.models.weather import Location, WeatherData  # noqa

logger = setup_logger(__name__)


def init_application():
    """Initialize the application."""
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")

        # Check if locations.csv exists
        if not Path(LOCATIONS_CSV_PATH).exists():
            logger.error(f"Locations file not found: {LOCATIONS_CSV_PATH}")
            return False

        logger.info("Application initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        return False


if __name__ == "__main__":
    init_application()
