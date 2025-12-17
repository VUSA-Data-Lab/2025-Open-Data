# data_fetcher.py
import requests
from typing import Dict


class NasaNeoFetcher:
    """
    Handles communication with the NASA NEO API.
    """

    BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_neo_data(self, start_date: str, end_date: str) -> Dict:
        """
        Fetches asteroid data from NASA NEO API.
        Returns parsed JSON.

        :param start_date: YYYY-MM-DD
        :param end_date: YYYY-MM-DD
        :return: dict response
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key
        }

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception(f"NASA API request failed: {response.status_code}")

        return response.json()
