from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def ensure_output_dir(output_dir: Path) -> None:
    """Create the output directory if it does not exist."""
    output_dir.mkdir(parents=True, exist_ok=True)


def plot_gdp_over_time(
    df: pd.DataFrame,
    output_dir: Path,
    filename: str = "uae_gdp_over_time.png",
) -> Path:
    """Plot GDP per capita over time for UAE."""
    ensure_output_dir(output_dir)

    plt.figure()
    plt.plot(df["year"], df["gdp_per_capita"], marker="o")

    plt.xlabel("Year")
    plt.ylabel("GDP per capita (USD)")
    plt.title("UAE GDP per Capita Over Time")
    plt.tight_layout()

    output_path = output_dir / filename
    plt.savefig(output_path)
    plt.close()
    return output_path
