import requests

BASE_URL = "https://api.worldbank.org/v2/"

def fetch_data(country_code, indicator_code):
    """
    Fetches data from the World Bank API for a specific country and indicator.
    """
    url = f"{BASE_URL}country/{country_code}/indicator/{indicator_code}?format=json&per_page=100"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if len(data) > 1 and data[1] is not None:
            return data[1]
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {country_code} and {indicator_code}: {e}")
        return None
