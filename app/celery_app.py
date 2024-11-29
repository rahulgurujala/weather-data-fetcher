from celery import Celery
from app.config import CELERY_CONFIG

# Initialize Celery
celery_app = Celery("weather_app")

# Configure Celery
celery_app.conf.update(CELERY_CONFIG)

# Configure the periodic tasks
celery_app.conf.beat_schedule = {
    "update-weather-data": {
        "task": "app.tasks.scheduler.update_weather_data",
        "schedule": 60.0,  # Every 60 seconds
        "options": {"queue": "weather_tasks"},
    }
}
