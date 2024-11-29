import csv
from typing import List, Dict, Any
import pandas as pd
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class CSVHandler:
    """Handler for CSV file operations."""

    @staticmethod
    def read_locations(file_path: str) -> List[Dict[str, Any]]:
        """
        Read locations from a CSV file.

        Args:
            file_path: Path to the CSV file

        Returns:
            List of dictionaries containing location data
        """
        try:
            df = pd.read_csv(file_path)
            # Convert DataFrame to list of dictionaries
            locations = df.to_dict("records")
            logger.info(
                f"Successfully read {len(locations)} locations from {file_path}"
            )
            return locations
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            raise

    @staticmethod
    def validate_location_data(location: Dict[str, Any]) -> bool:
        """
        Validate location data format.

        Args:
            location: Dictionary containing location data

        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = {"city", "latitude", "longitude"}

        # Check if all required fields are present
        if not all(field in location for field in required_fields):
            logger.error(
                f"Missing required fields in location data: {location}"
            )
            return False

        # Validate latitude and longitude
        try:
            lat = float(location["latitude"])
            lon = float(location["longitude"])

            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                logger.error(
                    f"Invalid coordinates in location data: {location}"
                )
                return False
        except ValueError:
            logger.error(
                f"Invalid coordinate format in location data: {location}"
            )
            return False

        return True
