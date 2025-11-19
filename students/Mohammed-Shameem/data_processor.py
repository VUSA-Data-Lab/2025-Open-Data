# data_processor.py
import pandas as pd


class NeoProcessor:
    """
    Processes NASA NEO asteroid JSON into structured DataFrames.
    """

    @staticmethod
    def parse_asteroids(json_data: dict) -> pd.DataFrame:
        """
        Converts raw JSON into a flat DataFrame.
        """
        records = []

        neo_by_date = json_data.get("near_earth_objects", {})

        for date, asteroids in neo_by_date.items():
            for a in asteroids:
                diameter = a["estimated_diameter"]["meters"]
                approach = a["close_approach_data"][0]

                records.append({
                    "name": a["name"],
                    "is_hazardous": a["is_potentially_hazardous_asteroid"],
                    "diameter_min_m": diameter["estimated_diameter_min"],
                    "diameter_max_m": diameter["estimated_diameter_max"],
                    "velocity_km_s": float(approach["relative_velocity"]["kilometers_per_second"]),
                    "miss_distance_km": float(approach["miss_distance"]["kilometers"]),
                    "close_approach_date": approach["close_approach_date"],
                    "orbiting_body": approach["orbiting_body"]
                })

        df = pd.DataFrame(records)
        return df

    @staticmethod
    def top_largest(df, num=10):
        """Return top N asteroids by maximum diameter."""
        return df.sort_values(by="diameter_max_m", ascending=False).head(num)

    @staticmethod
    def closest(df):
        """Return the asteroid with the smallest miss distance."""
        return df.sort_values(by="miss_distance_km", ascending=True).iloc[0]
