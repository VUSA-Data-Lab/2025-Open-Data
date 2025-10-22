# =============================================
# Išmanusis laistymas pagal meteo.lt prognozes
# Autoriai: Irmantas Kolbergas, Augustas Štaudė
# =============================================

import requests
import pandas as pd
import math
from colorama import Fore, Style
# --- 1. Naudotojo įvestis ---
place = input("Įveskite miestą (pvz. vilnius, siauliai, kaunas): ").strip().lower()#: Pašalina nereikalingus tarpus ir visas raides paverčia mažosiomis raidėmis
soil = input("Įveskite dirvožemio tipą (smėlis / priemolis / molis): ").strip().lower()

# --- 2. Dirvožemio parametrai (vandens sulaikymo koeficientas) ---
soil_coeff = {
    "smėlis": 1.2,      # laistome dažniau
    "priemolis": 1.0,   # vidutinis
    "molis": 0.8        # sulaiko ilgiau
}

kc = 0.9  # pasėlių koeficientas (pvz., žalias vejas / daržovės)
soil_k = soil_coeff.get(soil, 1.0)  # jei blogai įvesta - naudoti 1.0

# --- 3. API duomenų gavimas ---
url = f"https://api.meteo.lt/v1/places/{place}/forecasts/long-term"
print(f"\nGaunami duomenys iš: {url}\n")


resp = requests.get(url)#išsiunčia užklausa nurodytu adresu
if resp.status_code != 200:
    print(" Klaida: nepavyko gauti duomenų. Patikrinkite miesto pavadinimą.")
    exit()

data = resp.json()#konvertuojama python duomenų struktūra

rows = []#masyvas
for rec in data["forecastTimestamps"]:
    rows.append({#įdedami tik reikalingi duomenys i masyva
        "time": rec["forecastTimeUtc"],
        "temperature": rec["airTemperature"],
        "precipitation": rec["totalPrecipitation"]
    })

df = pd.DataFrame(rows)#sukuriama lentele iš duomenu
df["time"] = pd.to_datetime(df["time"])#pasirinkamas laikas
df = df.dropna(subset=["temperature"]).reset_index(drop=True)
# dropna() pašalina eilutes,kuriuose trūksta duoemnu. subset nuorodoma kad žiureti tik į temperatura stulpeli jei nera temperaturos visa eilute yra prašalinama
# --- 4. Paros suvestinė ---
df_daily = (
    df.set_index("time")
      .resample("24h")
      .agg(Tmax=("temperature", "max"),
           Tmin=("temperature", "min"),
           Tmean=("temperature", "mean"),
           precipitation_mm=("precipitation", "sum"))
      .reset_index()
)

# --- 5. Hargreaves ETo apskaičiavimas ---
def eto_hargreaves(tmin, tmax, tmean, lat=55.9):
    """
    Supaprastinta Hargreaves formulė (mm/day)
    Naudoja vidutinę Lietuvos platumą 55.9°N
    """
    # Aproksimuotas Ra (MJ/m²/dienai) ~ 20
    Ra = 20
    eto = 0.0023 * (tmean + 17.8) * math.sqrt(max(0, tmax - tmin)) * Ra
    return eto

# --- 6. Laistymo poreikio apskaičiavimas ---
def irrigation_need(eto, kc, precip_mm, soil_factor=1.0):
    etc = kc * eto
    effective_rain = precip_mm * 0.8  # laikome, kad 80% lietaus efektyvus
    need = max(0, (etc - effective_rain) * soil_factor)
    return need, etc, effective_rain

needs = []
for _, row in df_daily.iterrows():
    eto = eto_hargreaves(row["Tmin"], row["Tmax"], row["Tmean"])
    need, etc, eff_rain = irrigation_need(eto, kc, row["precipitation_mm"], soil_k)
    needs.append({
        "date": row["time"].date(),                         
        "Tmean (°C)": round(row["Tmean"], 1),
        "Precip (mm)": round(row["precipitation_mm"], 1),
        "ETo (mm)": round(eto, 2),
        "ETc (mm)": round(etc, 2),
        "Efektyvus lietus (mm)": round(eff_rain, 2),
        "Litrai/m²": round(need, 2),
    })

df_result = pd.DataFrame(needs)

# --- 7. Rezultatų atvaizdavimas ---
print("\n===== Prognozės santrauka ir laistymo poreikis =====\n")
print(df_result.head(10).to_string(index=False))

# --- 8. Išvados pagal pirmą dieną ---
avg_need = df_result["Litrai/m²"].mean()
print(Style.BRIGHT+ Fore.BLUE +"\nVidutinis laistymo poreikis per prognozuotą laikotarpį:")
print(Style.BRIGHT+ Fore.BLUE +f"{avg_need:.1f} mm per dieną ({avg_need:.1f} L/m²)")

if avg_need == 0:
    print(Style.BRIGHT+ Fore.BLUE +" Artimiausiomis dienomis laistyti nereikia (pakanka kritulių)."+ Style.RESET_ALL)
elif avg_need < 3:
    print(Style.BRIGHT+ Fore.BLUE +" Minimalus laistymas reikalingas kas kelias dienas."+ Style.RESET_ALL)
else:
    print(Style.BRIGHT+ Fore.BLUE +"Reikalingas reguliarus laistymas (kasdien arba kas antrą dieną)." + Style.RESET_ALL)


