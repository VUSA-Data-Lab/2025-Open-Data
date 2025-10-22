# BIBLIOTEKOS
import requests   # API duomenų nuskaitymui
import pandas as pd  # Duomenų apdorojimui
import json       # Gražiam JSON formatavimui

# DUOMENŲ NUSKAITYMAS IŠ API

# LHMT atvirų duomenų API adresas
url = "https://get.data.gov.lt/datasets/gov/lhmt/stebejimai/Matavimas"

# Siunčiame GET užklausą
response = requests.get(url)

# Patikriname ar API atsakė teisingai
if response.status_code == 200:
    data = response.json()  # Konvertuojame JSON į Python struktūrą
else:
    raise Exception(f"Klaida gaunant duomenis: {response.status_code}")

# DUOMENŲ PARUOŠIMAS

# Ištraukiame faktinius matavimus
measurements = data["_data"]

# Sukuriame DataFrame objektą
df = pd.DataFrame(measurements)

# Pašaliname tuščias eilutes
df.dropna(inplace=True)

# Pašaliname pasikartojančias eilutes
df.drop_duplicates(inplace=True)

# Atrenkame tik svarbiausius stulpelius
columns = [
    "stebejimo_laikas",
    "stoties_pavadinimas",
    "oro_temp",
    "vejo_greitis",
    "santyk_oro_dregme",
    "kritutliu_kiekis"
]
df = df[columns]

# Konvertuojame datą į datetime formatą
df["stebejimo_laikas"] = pd.to_datetime(df["stebejimo_laikas"])


# DUOMENŲ IŠVESTIS (PIRMOS 10 EILUČIŲ)

print("🔹 Meteorologinių duomenų ištrauka (pirmos 10 eilučių):")
print(df.head(10).to_string())

