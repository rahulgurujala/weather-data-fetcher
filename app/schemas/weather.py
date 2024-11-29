from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, validator


class LocationBase(BaseModel):
    """Base schema for location data."""

    city: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    country: Optional[str] = None

    @validator("latitude")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return round(v, 6)

    @validator("longitude")
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return round(v, 6)


class LocationCreate(LocationBase):
    """Schema for creating a new location."""

    pass


class LocationResponse(LocationBase):
    """Schema for location response."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WeatherDataBase(BaseModel):
    """Base schema for weather data."""

    temperature: float
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    precipitation: Optional[float] = None
    weather_code: Optional[int] = None
    raw_data: Dict[str, Any]


class WeatherDataCreate(WeatherDataBase):
    """Schema for creating weather data."""

    location_id: int


class WeatherDataResponse(WeatherDataBase):
    """Schema for weather data response."""

    id: int
    location_id: int
    timestamp: datetime
    created_at: datetime
    location: LocationResponse

    model_config = ConfigDict(from_attributes=True)


class WeatherBatchResponse(BaseModel):
    """Schema for batch weather data response."""

    location: LocationResponse
    weather: WeatherDataResponse
    success: bool
    error: Optional[str] = None
