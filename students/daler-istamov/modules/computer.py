import pandas as pd


def compute(births_df: pd.DataFrame, deaths_df: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(births_df, deaths_df, on="year", how="inner")
    merged["natural_growth"] = merged.births - merged.deaths
    return merged