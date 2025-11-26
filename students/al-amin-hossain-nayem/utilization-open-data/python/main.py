from fetcher import fetch_data
from processor import process_data
from utils import save_to_json

# --- Configuration ---
COUNTRIES = {
    "bangladesh": "BGD",
    "lithuania": "LTU"
}

INDICATORS = {
    "population": "SP.POP.TOTL",
    "education": [
        "SE.PRM.ENRR",  # School enrollment, primary
        "SE.ADT.LITR.ZS" # Literacy rate, adult total (% of people ages 15 and above)
    ]
}

OUTPUT_FILE = "../react-app/public/processed.json"

# --- Main Logic ---
def main():
    """
    Main function to fetch, process, and save World Bank data.
    """
    final_data = {
        "population": {},
        "education": {},
        "districts": {
            "bangladesh": [
                { "name": "Dhaka", "population": 10200000, "education_rate": 74.5 },
                { "name": "Chittagong", "population": 5200000, "education_rate": 65.2 },
                { "name": "Khulna", "population": 1800000, "education_rate": 70.1 },
                { "name": "Rajshahi", "population": 900000, "education_rate": 68.9 }
            ],
            "lithuania": [
                { "name": "Vilnius", "population": 580000, "education_rate": 99.8 },
                { "name": "Kaunas", "population": 300000, "education_rate": 99.7 },
                { "name": "Klaipėda", "population": 150000, "education_rate": 99.6 }
            ]
        }
    }

    # --- Population Data ---
    for country_name, country_code in COUNTRIES.items():
        print(f"Fetching population data for {country_name.title()}...")
        raw_pop_data = fetch_data(country_code, INDICATORS["population"])
        if raw_pop_data:
            final_data["population"][country_name] = process_data(raw_pop_data)

    # --- Education Data ---
    for country_name, country_code in COUNTRIES.items():
        print(f"Fetching education data for {country_name.title()}...")
        
        all_edu_data = []
        for indicator in INDICATORS["education"]:
            raw_edu_data = fetch_data(country_code, indicator)
            if raw_edu_data:
                processed_edu_data = process_data(raw_edu_data)
                # Add indicator info to each entry
                for entry in processed_edu_data:
                    entry['indicator'] = indicator
                all_edu_data.extend(processed_edu_data)
        
        final_data["education"][country_name] = sorted(all_edu_data, key=lambda x: x['year'], reverse=True)


    # --- Save to File ---
    save_to_json(final_data, OUTPUT_FILE)
    print(f"Data successfully saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()