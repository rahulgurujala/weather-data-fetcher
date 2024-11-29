from celery import chord

from app.celery_app import celery_app
from app.config import LOCATIONS_CSV_PATH
from app.utils.csv_handler import CSVHandler
from app.utils.logger import setup_logger

from .weather_tasks import fetch_weather_for_location, save_weather_data

logger = setup_logger(__name__)


@celery_app.task
def update_weather_data() -> None:
    """
    Scheduled task to update weather data for all locations.
    Creates a chord of tasks to fetch weather data concurrently.
    """
    try:
        # Read locations from CSV
        csv_handler = CSVHandler()
        locations = csv_handler.read_locations(LOCATIONS_CSV_PATH)

        logger.info(f"Read {len(locations)} locations from CSV: {locations}")

        if not locations:
            logger.warning("No locations found in CSV file")
            return

        # Create a chord of tasks
        task_chord = chord(
            fetch_weather_for_location.s(location) for location in locations
        )(save_weather_data.s())

        logger.info(f"Started weather update for {len(locations)} locations")
        return task_chord

    except Exception as e:
        logger.error(f"Error scheduling weather update tasks: {str(e)}")
        raise
