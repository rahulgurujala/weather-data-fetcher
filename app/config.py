import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{BASE_DIR}/data/weather.db"
)

# API Configuration
OPEN_METEO_API_URL = os.getenv(
    "OPEN_METEO_API_URL", "https://api.open-meteo.com/v1/"
)
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Celery Configuration
CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "enable_utc": True,
    "task_track_started": True,
    "worker_max_tasks_per_child": 100,
    "task_time_limit": 600,  # 10 minutes
    "task_soft_time_limit": 300,  # 5 minutes
    "worker_prefetch_multiplier": 1,  # One task per worker at a time
    "task_routes": {"app.tasks.*": {"queue": "weather_tasks"}},
}

# Retry Configuration
RETRY_CONFIG = {
    "max_retries": 3,
    "initial_backoff": 1,
    "max_backoff": 30,
    "exponential_backoff": True,
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "/var/log/celery-weather-app/app.log")

# CSV Configuration
LOCATIONS_CSV_PATH = os.path.join(BASE_DIR, "data", "locations.csv")

# Weather Data Configuration
WEATHER_PARAMS = {
    "temperature_unit": "celsius",
    "windspeed_unit": "kmh",
    "precipitation_unit": "mm",
    "forecast_days": 1,
}
