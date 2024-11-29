from typing import List

from pydantic import BaseModel

from .weather import LocationBase


class WeatherRequest(BaseModel):
    """Schema for weather data request."""

    location: LocationBase


class BatchWeatherRequest(BaseModel):
    """Schema for batch weather data request."""

    locations: List[LocationBase]
