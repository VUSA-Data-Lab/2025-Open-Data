# =============================================
# Išmanusis laistymas pagal meteo.lt prognozes
# Autoriai: Irmantas Kolbergas, Augustas Štaudė
# =============================================

import requests
import pandas as pd
import math
from colorama import Fore, Style
from typing import Dict, Any, List

API_URL_TEMPLATE = "https://api.meteo.lt/v1/places/{place}/forecasts/long-term"
SOIL_COEFFICIENTS = {
    "smėlis": 1.2,      # Laistome dažniau, nes vanduo greitai susigeria.
    "priemolis": 1.0,   # Vidutinis sulaikymas.
    "molis": 0.8        # Sulaiko vandenį ilgiau, laistome rečiau.
}
DEFAULT_SOIL_TYPE = "priemolis"
CROP_COEFFICIENT = 0.9  # Koeficientas vejai, daržovėms.
EFFECTIVE_RAIN_RATIO = 0.8  # Priimame, kad 80% lietaus yra efektyvus pasėliams.

def get_user_input() -> (str, str):
    """
    Gauna iš naudotojo miesto ir dirvožemio tipo įvestį.
    """
    place = input("Įveskite miestą (pvz. vilnius, siauliai, kaunas): ").strip().lower()
    soil = input(f"Įveskite dirvožemio tipą ({' / '.join(SOIL_COEFFICIENTS.keys())}): ").strip().lower()
    return place, soil

def fetch_weather_data(place: str) -> List[Dict[str, Any]]:
    """
    Atsisiunčia orų prognozės duomenis iš meteo.lt API.
    """
    url = API_URL_TEMPLATE.format(place=place)
    print(f"\nGaunami duomenys iš: {url}\n")
    try:
        response = requests.get(url, timeout=10) # Pridėtas timeout
        response.raise_for_status()  # Automatiškai patikrina, ar statusas nėra 2xx
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Klaida: Nepavyko gauti duomenų. Patikrinkite miesto pavadinimą ir interneto ryšį. (Klaida: {e})" + Style.RESET_ALL)
        return []

    data = response.json()
    # Išrenkame tik reikalingus laukus
    forecast_data = [
        {
            "time": rec["forecastTimeUtc"],
            "temperature": rec.get("airTemperature"), # .get() saugesnis, jei lauko nebūtų
            "precipitation": rec.get("totalPrecipitation")
        }
        for rec in data.get("forecastTimestamps", [])
    ]
    return forecast_data

def process_to_daily_summary(forecast_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Konvertuoja valandinius prognozės duomenis į dienų suvestinę.
    """
    if not forecast_data:
        return pd.DataFrame()

    df = pd.DataFrame(forecast_data)
    df["time"] = pd.to_datetime(df["time"])
    df = df.dropna(subset=["temperature"]).reset_index(drop=True)

    df_daily = (
        df.set_index("time")
          .resample("D")
          .agg(
              Tmax=("temperature", "max"),
              Tmin=("temperature", "min"),
              Tmean=("temperature", "mean"),
              precipitation_mm=("precipitation", "sum")
          )
          .reset_index()
    )
    return df_daily

def calculate_irrigation_needs(df_daily: pd.DataFrame, soil_type: str) -> pd.DataFrame:
    """
    Apskaičiuoja laistymo poreikį kiekvienai dienai.
    """
    if df_daily.empty:
        return pd.DataFrame()

    soil_k = SOIL_COEFFICIENTS.get(soil_type, SOIL_COEFFICIENTS[DEFAULT_SOIL_TYPE])
    
    def eto_hargreaves(tmin, tmax, tmean):
        Ra = 20  # Saulės radiacijos koeficiantas Lietuvoje
        eto = 0.0023 * (tmean + 17.8) * math.sqrt(max(0, tmax - tmin)) * Ra
        return eto

    results = []
    for _, row in df_daily.iterrows():
        eto = eto_hargreaves(row["Tmin"], row["Tmax"], row["Tmean"])
        etc = CROP_COEFFICIENT * eto
        effective_rain = row["precipitation_mm"] * EFFECTIVE_RAIN_RATIO
        need = max(0, (etc - effective_rain) * soil_k)
        
        results.append({
            "Data": row["time"].date(),
            "Vid. temp. (°C)": round(row["Tmean"], 1),
            "Krituliai (mm)": round(row["precipitation_mm"], 1),
            "ETo (mm)": round(eto, 2),
            "ETc (mm)": round(etc, 2),
            "Efektyvus lietus (mm)": round(effective_rain, 2),
            "Reikia laistyti (L/m²)": round(need, 2),
        })
        
    return pd.DataFrame(results)

def display_results_and_conclusion(df_result: pd.DataFrame):
    """
    Atvaizduoja rezultatus lentelėje ir pateikia galutinę išvadą.
    """
    if df_result.empty:
        print(Fore.YELLOW + "Nepavyko apskaičiuoti rezultatų, nes trūksta duomenų." + Style.RESET_ALL)
        return

    print("\n===== Prognozės santrauka ir laistymo poreikis =====\n")
    print(df_result.head(7).to_string(index=False))

    avg_need = df_result["Reikia laistyti (L/m²)"].mean()
    
    print(Style.BRIGHT + Fore.BLUE + "\nIŠVADA:")
    print(f"Vidutinis laistymo poreikis per artimiausią savaitę: {avg_need:.1f} L/m² per dieną." + Style.RESET_ALL)

    if avg_need < 0.5:
        recommendation = "Artimiausiomis dienomis laistyti nereikia (pakanka kritulių arba garavimas mažas)."
    elif avg_need < 3.0:
        recommendation = "Minimalus laistymas reikalingas kas 2-3 dienas, kad palaikyti drėgmę."
    else:
        recommendation = "Reikalingas reguliarus laistymas (kasdien arba kas antrą dieną)."
    
    print(Style.BRIGHT + Fore.GREEN + recommendation + Style.RESET_ALL)

def main():
    """Pagrindinė programos funkcija, kuri valdo visą logikos eigą."""
    place, soil = get_user_input()
    
    raw_data = fetch_weather_data(place)
    
    if not raw_data: # Jei duomenų gauti nepavyko, baigiame darbą
        return
        
    daily_summary_df = process_to_daily_summary(raw_data)
    
    final_results_df = calculate_irrigation_needs(daily_summary_df, soil)
    
    display_results_and_conclusion(final_results_df)

main()
