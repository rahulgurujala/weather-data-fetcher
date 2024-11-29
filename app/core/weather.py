from typing import Any, Dict
from urllib.parse import urljoin

import requests

from app.config import API_TIMEOUT, OPEN_METEO_API_URL, WEATHER_PARAMS
from app.utils.logger import setup_logger
from app.utils.retry import retry_with_backoff

logger = setup_logger(__name__)


class WeatherClient:
    """Client for interacting with the Open-Meteo API."""

    def __init__(
        self, base_url: str = OPEN_METEO_API_URL, timeout: int = API_TIMEOUT
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    @retry_with_backoff()
    def get_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Fetch weather data for a specific location.

        Args:
            latitude: Location latitude
            longitude: Location longitude

        Returns:
            Dictionary containing weather data
        """
        endpoint = "forecast"
        url = urljoin(self.base_url, endpoint)

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
            **WEATHER_PARAMS,
        }

        try:
            response = self.session.get(
                url, params=params, timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            logger.info(
                f"Successfully fetched weather data for coordinates: \
                    {latitude}, {longitude}"
            )
            return data

        except requests.RequestException as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            raise

    def get_batch_weather(
        self, locations: list[Dict[str, Any]]
    ) -> list[Dict[str, Any]]:
        """
        Fetch weather data for multiple locations.

        Args:
            locations: List of dictionaries containing location data

        Returns:
            List of dictionaries containing weather data
        """
        results = []
        for location in locations:
            try:
                weather_data = self.get_weather(
                    latitude=location["latitude"],
                    longitude=location["longitude"],
                )
                results.append(
                    {"location": location, "weather_data": weather_data}
                )
            except Exception as e:
                logger.error(
                    f"Failed to fetch weather for location \
                        {location}: {str(e)}"
                )
                results.append({"location": location, "error": str(e)})

        return results

    def close(self):
        """Close the requests session."""
        self.session.close()
