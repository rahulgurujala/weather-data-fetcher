from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.config import RETRY_CONFIG
from app.core.database import get_db
from app.core.weather import WeatherClient
from app.models.weather import Location, WeatherData
from app.schemas.weather import LocationCreate, WeatherDataCreate
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@celery_app.task(
    bind=True,
    max_retries=RETRY_CONFIG["max_retries"],
    default_retry_delay=RETRY_CONFIG["initial_backoff"],
)
def fetch_weather_for_location(
    self, location_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Task to fetch weather data for a single location.

    Args:
        location_data: Dictionary containing location information

    Returns:
        Dictionary containing weather data and location information
    """
    try:
        weather_client = WeatherClient()
        weather_data = weather_client.get_weather(
            latitude=location_data["latitude"],
            longitude=location_data["longitude"],
        )

        return {
            "location": location_data,
            "weather_data": weather_data,
            "success": True,
        }

    except Exception as exc:
        logger.error(
            f"Error fetching weather data for location {location_data}: {exc}"
        )
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        return {"location": location_data, "success": False, "error": str(exc)}
    finally:
        weather_client.close()


@celery_app.task
def save_weather_data(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Callback task to save weather data to database.

    Args:
        results: List of dictionaries containing weather data and location
        information

    Returns:
        Dictionary containing summary of the operation
    """
    success_count = 0
    error_count = 0

    with get_db() as db:
        for result in results:
            try:
                if result["success"]:
                    location_data = result["location"]
                    weather_data = result["weather_data"]

                    # Create or update location
                    location = _get_or_create_location(db, location_data)

                    # Create weather data entry
                    _create_weather_data(db, location.id, weather_data)

                    success_count += 1
                else:
                    error_count += 1
                    logger.error(
                        f"Failed to process weather data: \
                        {result.get('error')}"
                    )

            except Exception as e:
                error_count += 1
                logger.error(f"Error saving weather data: {str(e)}")

    return {
        "total_processed": len(results),
        "successful": success_count,
        "failed": error_count,
    }


def _get_or_create_location(
    db: Session, location_data: Dict[str, Any]
) -> Location:
    """Helper function to get or create a location in the database."""
    location = (
        db.query(Location)
        .filter(
            Location.latitude == location_data["latitude"],
            Location.longitude == location_data["longitude"],
        )
        .first()
    )

    if not location:
        location_create = LocationCreate(**location_data)
        location = Location(**location_create.model_dump())
        db.add(location)
        db.commit()
        db.refresh(location)

    return location


def _create_weather_data(
    db: Session, location_id: int, weather_data: Dict[str, Any]
) -> WeatherData:
    """Helper function to create weather data in the database."""
    current_weather = weather_data.get("current_weather", {})

    weather_create = WeatherDataCreate(
        location_id=location_id,
        temperature=current_weather.get("temperature"),
        wind_speed=current_weather.get("windspeed"),
        wind_direction=current_weather.get("winddirection"),
        weather_code=current_weather.get("weathercode"),
        raw_data=weather_data,
    )

    db_weather = WeatherData(**weather_create.model_dump())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)

    return db_weather
