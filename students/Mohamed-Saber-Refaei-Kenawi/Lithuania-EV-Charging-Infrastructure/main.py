"""
Main entry point for the EV Charging Infrastructure Analysis project.
Orchestrates data extraction, transformation, and visualization.
"""

from src.etl import EVDataPipeline
from src.visualizer import EVVisualizer


def main():
    # 1. Configuration
    # Split long URL for PEP8 compliance
    base_url = "https://ev.vialietuva.lt/publicdata"
    data_endpoint = "/EnergyInfrastructureTablePublication"
    data_url = f"{base_url}{data_endpoint}"

    # 2. Extract, Transform, Load (ETL)
    pipeline = EVDataPipeline(url=data_url)
    df = pipeline.run()

    if df.empty:
        print("No data available to process.")
        return

    # 3. Visualization and Analysis
    viz = EVVisualizer(df)
    viz.generate_map()
    viz.generate_growth_chart()
    viz.generate_power_distribution()

    print("\nProject execution completed successfully.")


if __name__ == "__main__":
    main()