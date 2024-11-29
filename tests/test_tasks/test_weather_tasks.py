from unittest.mock import patch

import pytest

from app.tasks.weather_tasks import fetch_weather_for_location


@pytest.mark.celery(result_backend="redis://")
def test_fetch_weather_task(sample_location_data, sample_weather_data):
    """Test weather fetching task."""
    with patch("app.core.weather.WeatherClient.get_weather") as mock_get:
        mock_get.return_value = sample_weather_data

        result = fetch_weather_for_location.apply(
            args=[sample_location_data]
        ).get()

        assert result["success"] is True
        assert result["location"] == sample_location_data
        assert result["weather_data"] == sample_weather_data
