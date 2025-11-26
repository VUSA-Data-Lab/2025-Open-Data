from pathlib import Path
import argparse

from app import create_app
from app.data_loader import prepare_clean_data_from_world_bank, load_clean_data
from app.processor import get_country_timeseries
from app.visualizer import plot_country_timeseries_cli

DATA_DIR = Path("data")
RAW = DATA_DIR / "world_bank_raw.csv"
CLEAN = DATA_DIR / "population_clean.csv"


def prepare():
    prepare_clean_data_from_world_bank(RAW, CLEAN)
    print("Cleaned dataset saved to:", CLEAN)


def run_web():
    app = create_app(str(CLEAN))
    app.run(debug=True)


def run_cli(code):
    df = load_clean_data(CLEAN)
    ts = get_country_timeseries(df, code)

    export = f"static/exports/{code}_cli.png"
    plot_country_timeseries_cli(ts, code, save_path=export)
    print("Chart saved to:", export)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prepare-data", action="store_true")
    p.add_argument("--web", action="store_true")
    p.add_argument("--cli")
    args = p.parse_args()

    if args.prepare_data:
        prepare()
    elif args.web:
        run_web()
    elif args.cli:
        run_cli(args.cli)
    else:
        p.print_help()
