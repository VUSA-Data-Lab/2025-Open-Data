import warnings
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")


class VaccinationDataProcessor:
    """Main class for processing and analyzing COVID-19 vaccination data."""

    def __init__(self, data_url: str):
        """Initialize with the URL of the vaccination dataset.

        Args:
            data_url (str): URL to the vaccination CSV file.
        """
        self.data_url = data_url
        self.raw_data = None
        self.processed_data = None

    def load_data(self) -> bool:
        """Load data from the specified URL."""
        print("Loading data from source...")
        try:
            self.raw_data = pd.read_csv(self.data_url)
            print(f"Successfully loaded {len(self.raw_data)} records")
            return True
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error loading data: {e}")
            return False

    def clean_data(self):
        """Clean and prepare data for analysis."""
        print("Cleaning data...")

        # Convert date column to datetime
        self.raw_data["date"] = pd.to_datetime(self.raw_data["date"])

        # Remove rows missing the key metric
        self.processed_data = self.raw_data.dropna(
            subset=["total_vaccinations_per_hundred"]
        )

        print(
            f"Data cleaned. {len(self.processed_data)} valid records remain"
        )

    def get_latest_data_by_country(self, countries=None):
        """Return the most recent vaccination data per country.

        Args:
            countries (list, optional): List of country names. If None, top 10.

        Returns:
            pd.DataFrame: Latest records.
        """
        if self.processed_data is None:
            print("No processed data available")
            return None

        # Latest record for each country
        latest_data = (
            self.processed_data.sort_values("date")
            .groupby("location")
            .tail(1)
        )

        if countries:
            latest_data = latest_data[
                latest_data["location"].isin(countries)
            ]
        else:
            # Top 10 by vaccination rate
            latest_data = latest_data.nlargest(
                10, "total_vaccinations_per_hundred"
            )

        return latest_data

    def get_time_series(self, countries):
        """Return time series for selected countries.

        Args:
            countries (list): List of country names.

        Returns:
            pd.DataFrame: Filtered time series.
        """
        if self.processed_data is None:
            return None

        ts = self.processed_data[
            self.processed_data["location"].isin(countries)
        ]
        return ts[["date", "location", "total_vaccinations_per_hundred"]]


class VaccinationVisualizer:
    """Handle all plotting and visualization."""

    def __init__(self):
        """Set default plotting style."""
        sns.set_style("whitegrid")
        plt.rcParams["figure.figsize"] = (12, 6)

    def plot_top_countries(
        self, data, title="Top Countries by Vaccination Rate"
    ):
        """Horizontal bar chart with average line."""
        plt.figure(figsize=(12, 6))

        sorted_data = data.sort_values(
            "total_vaccinations_per_hundred", ascending=True
        )
        avg_rate = sorted_data["total_vaccinations_per_hundred"].mean()

        plt.barh(
            sorted_data["location"],
            sorted_data["total_vaccinations_per_hundred"],
            color="steelblue",
        )
        plt.axvline(
            x=avg_rate,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Average: {avg_rate:.2f} per 100",
        )

        plt.xlabel("Vaccinations per 100 people")
        plt.ylabel("Country")
        plt.title(title)
        plt.legend()
        plt.tight_layout()
        plt.savefig("top_countries.png", dpi=300, bbox_inches="tight")
        print("Saved chart: top_countries.png")
        plt.show()

    def plot_time_series(self, data, countries):
        """Line chart of vaccination progress over time."""
        plt.figure(figsize=(14, 7))

        for country in countries:
            country_data = data[data["location"] == country]
            plt.plot(
                country_data["date"],
                country_data["total_vaccinations_per_hundred"],
                marker="o",
                label=country,
                linewidth=2,
            )

        plt.xlabel("Date")
        plt.ylabel("Vaccinations per 100 people")
        plt.title("Vaccination Progress Over Time")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("time_series.png", dpi=300, bbox_inches="tight")
        print("Saved chart: time_series.png")
        plt.show()


class ReportGenerator:
    """Generate console reports and summaries."""

    @staticmethod
    def generate_summary(data):
        """Create a dictionary of key statistics."""
        return {
            "total_countries": len(data),
            "avg_vaccination_rate": data["total_vaccinations_per_hundred"]
            .mean(),
            "max_vaccination_rate": data["total_vaccinations_per_hundred"]
            .max(),
            "min_vaccination_rate": data["total_vaccinations_per_hundred"]
            .min(),
            "top_country": data.loc[
                data["total_vaccinations_per_hundred"].idxmax(), "location"
            ],
        }

    @staticmethod
    def print_report(summary, latest_data):
        """Print a nicely formatted report."""
        print("\n" + "=" * 60)
        print("COVID-19 VACCINATION ANALYSIS REPORT")
        print("=" * 60)
        print(f"\nAnalysis Date: {datetime.now():%Y-%m-%d %H:%M}")
        print(f"\nTotal Countries Analyzed: {summary['total_countries']}")
        print(
            f"Average Vaccination Rate: "
            f"{summary['avg_vaccination_rate']:.2f} per 100"
        )
        print(
            f"Highest Rate: {summary['max_vaccination_rate']:.2f} per 100"
        )
        print(f"Top Country: {summary['top_country']}")

        print("\n" + "-" * 60)
        print("TOP 10 COUNTRIES BY VACCINATION RATE")
        print("-" * 60)

        for _, row in latest_data.iterrows():
            print(
                f"{row['location']:30} "
                f"{row['total_vaccinations_per_hundred']:>6.2f} per 100"
            )

        print("=" * 60 + "\n")


def main():
    """Run the complete analysis workflow."""
    DATA_URL = (
        "https://raw.githubusercontent.com/owid/covid-19-data/master/"
        "public/data/vaccinations/vaccinations.csv"
    )
    COUNTRIES_TO_COMPARE = [
        "United States",
        "Germany",
        "Japan",
        "Brazil",
        "India",
    ]

    print("Starting COVID-19 Vaccination Analysis...")
    print("=" * 60 + "\n")

    processor = VaccinationDataProcessor(DATA_URL)

    if not processor.load_data():
        print("Failed to load data. Exiting.")
        return

    processor.clean_data()

    latest_data = processor.get_latest_data_by_country()
    time_series_data = processor.get_time_series(COUNTRIES_TO_COMPARE)

    summary = ReportGenerator.generate_summary(latest_data)
    ReportGenerator.print_report(summary, latest_data)

    visualizer = VaccinationVisualizer()
    visualizer.plot_top_countries(latest_data)
    visualizer.plot_time_series(time_series_data, COUNTRIES_TO_COMPARE)

    print(
        "\nAnalysis complete! Check generated PNG files for visualizations."
    )


if __name__ == "__main__":
    main()
