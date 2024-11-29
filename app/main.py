import sys
from pathlib import Path

from app.config import LOCATIONS_CSV_PATH
from app.core.database import init_db
from app.tasks.scheduler import update_weather_data
from app.utils.logger import setup_logger

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
            sys.exit(1)

        logger.info("Application initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        sys.exit(1)


def start_weather_update():
    """Start the weather update process."""
    try:
        logger.info("Starting weather update process")
        result = update_weather_data.delay()
        return result
    except Exception as e:
        logger.error(f"Error starting weather update: {str(e)}")
        raise


if __name__ == "__main__":
    init_application()
    start_weather_update()
