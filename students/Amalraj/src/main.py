from config import COUNTRIES, END_YEAR, OUTPUT_DIR, START_YEAR
from data_loader import load_data
from data_processor import compute_growth, compute_summary_statistics, filter_data
from visualizer import plot_gdp_over_time


def main() -> None:
    """Main entry point for the open data analysis program."""
    print("Loading data...")
    df = load_data()

    print("Filtering data...")
    filtered_df = filter_data(df, COUNTRIES, START_YEAR, END_YEAR)
    print(f"\nFiltered data:\n{filtered_df}")

    print("\nComputing summary statistics...")
    summary_df = compute_summary_statistics(filtered_df)
    print("\nSummary statistics (GDP per capita):")
    print(summary_df.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    print("\nComputing growth between first and last year...")
    growth_df = compute_growth(filtered_df)
    print("\nGDP per capita growth (%):")
    print(growth_df.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    print("\nCreating plot...")
    gdp_over_time_path = plot_gdp_over_time(filtered_df, OUTPUT_DIR)

    print(f"\nSaved line chart to: {gdp_over_time_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
