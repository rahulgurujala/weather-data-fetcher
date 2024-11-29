from unittest.mock import patch

import pytest

from app.tasks.scheduler import update_weather_data


@pytest.mark.celery(result_backend="redis://")
def test_update_weather_data(sample_location_data):
    """Test weather update scheduler."""
    with patch("app.utils.csv_handler.CSVHandler.read_locations") as mock_read:
        mock_read.return_value = [sample_location_data]

        result = update_weather_data.apply().get()

        assert result is not None
