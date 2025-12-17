# main.py
import argparse
from data_fetcher import NasaNeoFetcher
from data_processor import NeoProcessor
from visualization import NeoVisualizer


def main():
    """
    Main program flow:
    1. Parse arguments
    2. Fetch data from NASA
    3. Process into DataFrame
    4. Show summary information
    5. Export CSV
    6. Show top and closest asteroids
    7. Save & show visualizations
    """

    parser = argparse.ArgumentParser(description="NASA NEO Asteroid Data Fetcher")
    parser.add_argument("--start", type=str, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, required=True, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    start_date = args.start
    end_date = args.end

    api_key = "DEMO_KEY"  # Replace with your own key for more reliability

    print("Fetching data from NASA...")
    fetcher = NasaNeoFetcher(api_key)
    raw_data = fetcher.fetch_neo_data(start_date, end_date)

    print("Processing data...")
    processor = NeoProcessor()
    df = processor.parse_asteroids(raw_data)

    print("\nSummary:")
    print(df.head())

    print("\nNumber of asteroids:", len(df))
    print("Hazardous asteroids:", df["is_hazardous"].sum())

    print("\nExporting dataset to asteroid_data.csv...")
    df.to_csv("asteroid_data.csv", index=False)
    print("CSV export complete.")

    print("\nTop 10 Largest Asteroids:")
    print(processor.top_largest(df))

    print("\nClosest Asteroid to Earth:")
    print(processor.closest(df))

    print("\nGenerating visualizations (and saving PNG files)...")
    NeoVisualizer.plot_diameter_distribution(df, save=True)
    NeoVisualizer.plot_hazardous_pie(df, save=True)
    NeoVisualizer.plot_velocity(df, save=True)

    print("Charts saved as PNG files.")


if __name__ == "__main__":
    main()
