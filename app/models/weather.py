from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Location(Base):
    """Model for storing location information."""

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship with WeatherData
    weather_data = relationship("WeatherData", back_populates="location")


class WeatherData(Base):
    """Model for storing weather information."""

    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    precipitation = Column(Float)
    weather_code = Column(Integer)
    raw_data = Column(JSON)  # Store complete API response
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with Location
    location = relationship("Location", back_populates="weather_data")
