from celery import Celery
from app.config import CELERY_CONFIG, REDIS_URL

# Initialize Celery
celery_app = Celery("weather_app")

# Configure Celery
celery_app.conf.update(CELERY_CONFIG)

# Optional: Add any beat schedule if needed
celery_app.conf.beat_schedule = {
    "update-weather-data": {
        "task": "app.tasks.update_weather_data",
        "schedule": 3600.0,  # Run every hour
    },
}
