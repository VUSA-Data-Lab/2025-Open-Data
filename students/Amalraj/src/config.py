from pathlib import Path

# Go up one level from src → UAE, then into data
DATA_FILE = Path("..") / "data" / "economy.csv"

COUNTRIES = ["UAE"]

START_YEAR = 2010
END_YEAR = 2023

# Save output one level up as well (inside UAE/output)
OUTPUT_DIR = Path("..") / "output"
