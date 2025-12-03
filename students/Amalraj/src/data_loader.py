from pathlib import Path
from typing import Union

import pandas as pd

from config import DATA_FILE


def load_data(path: Union[str, Path] = None) -> pd.DataFrame:
    """Load the CSV data file into a pandas DataFrame."""
    csv_path = Path(path) if path is not None else DATA_FILE

    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # Ensure correct data types
    df["year"] = df["year"].astype(int)
    df["gdp_per_capita"] = df["gdp_per_capita"].astype(float)
    df["country"] = df["country"].astype(str)

    return df
