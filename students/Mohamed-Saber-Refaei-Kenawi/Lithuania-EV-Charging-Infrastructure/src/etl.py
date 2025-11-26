import os
import xml.etree.ElementTree as ET
import requests
import pandas as pd


class EVDataPipeline:
    """
    Handles the Extraction (Download), Transformation (Cleaning),
    and Loading (Saving) of EV data.
    """

    def __init__(self, url, data_dir="data"):
        self.url = url
        self.data_dir = data_dir
        self.raw_file = os.path.join(data_dir, "lithuania_ev_stations.csv")
        os.makedirs(data_dir, exist_ok=True)

    def _strip_ns(self, tag):
        """Helper to remove XML namespaces."""
        return tag.split('}')[-1] if '}' in tag else tag

    def download_and_parse(self):
        """Downloads XML and parses it into a Pandas DataFrame."""
        print(f"Downloading data from {self.url}...")
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            records = []

            for site in root.iter():
                if self._strip_ns(site.tag) == "energyInfrastructureSite":
                    record = {}
                    for child in site.iter():
                        tag = self._strip_ns(child.tag)
                        if child.text and child.text.strip():
                            if tag not in record:
                                record[tag] = child.text.strip()
                    records.append(record)

            return pd.DataFrame(records)
        except Exception as e:
            print(f"Error downloading data: {e}")
            return pd.DataFrame()

    def clean_data(self, df):
        """Applies data type conversions and cleaning logic."""
        if df.empty:
            return df

        # 1. Numeric conversions
        cols_to_numeric = [
            'latitude', 'longitude',
            'numberOfRefillPoints', 'maxPowerAtSocket'
        ]
        for col in cols_to_numeric:
            df[col] = pd.to_numeric(df.get(col, 0), errors='coerce')

        # 2. Fill missing
        df['connectorType'] = df.get(
            'connectorType', 'Unknown'
        ).fillna("Unknown")

        # 3. Date parsing
        df['lastUpdated'] = pd.to_datetime(
            df.get('lastUpdated'), errors='coerce', utc=True
        )
        df = df.dropna(subset=['lastUpdated', 'latitude', 'longitude'])

        # 4. Filter Dates (Exclude November, Include October)
        df['year'] = df['lastUpdated'].dt.year
        df['month'] = df['lastUpdated'].dt.month

        # Exclude month 11 (November)
        df = df[df['month'] != 11]

        # 5. Feature Engineering
        df['is_fast_charger'] = (df['maxPowerAtSocket'] >= 50).astype(int)

        return df

    def run(self):
        """Executes the pipeline and returns the cleaned DataFrame."""
        df_raw = self.download_and_parse()
        df_clean = self.clean_data(df_raw)

        # Save locally
        df_clean.to_csv(self.raw_file, index=False)
        print(f"Data saved to {self.raw_file}. Records: {len(df_clean)}")
        return df_clean