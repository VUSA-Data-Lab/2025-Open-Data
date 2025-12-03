from typing import List

import pandas as pd


def filter_data(
    df: pd.DataFrame,
    countries: List[str],
    start_year: int,
    end_year: int,
) -> pd.DataFrame:
    """Filter the dataset by countries and year range."""
    mask_countries = df["country"].isin(countries)
    mask_years = (df["year"] >= start_year) & (df["year"] <= end_year)
    filtered = df.loc[mask_countries & mask_years].copy()
    filtered.sort_values(by=["country", "year"], inplace=True)
    filtered.reset_index(drop=True, inplace=True)
    return filtered


def compute_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute average, min and max GDP per capita for each country."""
    grouped = df.groupby("country")["gdp_per_capita"]
    summary = grouped.agg(
        mean_gdp="mean",
        min_gdp="min",
        max_gdp="max",
    )
    return summary.reset_index()


def compute_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Compute GDP per capita growth from first to last year for each country."""
    results = []

    for country, group in df.groupby("country"):
        group_sorted = group.sort_values("year")
        first_row = group_sorted.iloc[0]
        last_row = group_sorted.iloc[-1]

        first_value = first_row["gdp_per_capita"]
        last_value = last_row["gdp_per_capita"]

        if first_value == 0:
            growth_percent = None
        else:
            growth_percent = (last_value - first_value) / first_value * 100

        results.append(
            {
                "country": country,
                "first_year": int(first_row["year"]),
                "last_year": int(last_row["year"]),
                "first_value": float(first_value),
                "last_value": float(last_value),
                "growth_percent": float(growth_percent)
                if growth_percent is not None
                else None,
            }
        )

    return pd.DataFrame(results)
