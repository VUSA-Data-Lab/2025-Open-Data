from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
CLEAN_FILE = DATA_DIR / "population_clean.csv"

def prepare_clean_data_from_world_bank(raw_path, out_path):
    raw_path = Path(raw_path)
    out_path = Path(out_path)

    df_raw = pd.read_csv(raw_path, skiprows=4)

    id_vars = ["Country Name", "Country Code"]
    value_vars = [c for c in df_raw.columns if c.isdigit()]

    df_long = df_raw.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="Year",
        value_name="Population"
    )

    df_long = df_long.dropna(subset=["Population"])
    df_long["Year"] = df_long["Year"].astype(int)
    df_long["Population"] = df_long["Population"].astype(float)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_long.to_csv(out_path, index=False)


def load_clean_data(path=CLEAN_FILE):
    """
    Load the cleaned population CSV.
    """
    df = pd.read_csv(path)
    df["Year"] = df["Year"].astype(int)
    df["Population"] = df["Population"].astype(float)
    return df
