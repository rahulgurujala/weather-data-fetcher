import pandas as pd

from app.utils.csv_handler import CSVHandler


def test_read_locations(tmp_path):
    """Test reading locations from CSV."""
    # Create a temporary CSV file
    csv_file = tmp_path / "test_locations.csv"
    df = pd.DataFrame(
        [
            {
                "city": "Test City",
                "latitude": 51.5074,
                "longitude": -0.1278,
                "country": "Test Country",
            }
        ]
    )
    df.to_csv(csv_file, index=False)

    locations = CSVHandler.read_locations(str(csv_file))
    assert len(locations) == 1
    assert locations[0]["city"] == "Test City"
