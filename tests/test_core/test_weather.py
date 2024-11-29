from unittest.mock import patch

from app.core.weather import WeatherClient


def test_weather_client_initialization():
    """Test WeatherClient initialization."""
    client = WeatherClient()
    assert client is not None
    assert client.base_url == "https://api.open-meteo.com/v1/"


@patch("requests.Session.get")
def test_get_weather(mock_get, sample_weather_data):
    """Test weather data fetching."""
    mock_get.return_value.json.return_value = sample_weather_data
    mock_get.return_value.status_code = 200

    client = WeatherClient()
    result = client.get_weather(51.5074, -0.1278)

    assert result == sample_weather_data
    mock_get.assert_called_once()
