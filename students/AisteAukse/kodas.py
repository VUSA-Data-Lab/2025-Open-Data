# BIBLIOTEKOS
import requests # API duomenų nuskaitymui
import pandas as pd # Duomenų apdorojimui

URL = "https://get.data.gov.lt/datasets/gov/lhmt/stebejimai/Matavimas"

def gauti_duomenis(url):
    response = requests.get(url)
    # Patikriname ar API atsakė teisingai
    if response.status_code != 200:
        raise Exception(f"Klaida gaunant duomenis: {response.status_code}")
    data = response.json() # Konvertuojame JSON į Python struktūrą
    if "_data" not in data:
        raise KeyError("Atsakyme trūksta '_data' lauko")
    return data["_data"]

def paruosti_duomenis(data):
    df = pd.DataFrame(data) # Sukuriame DataFrame objektą
    df.dropna(inplace=True) # Pašaliname tuščias eilutes
    df.drop_duplicates(inplace=True) # Pašaliname pasikartojančias eilutes
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
    #Papildomi požymiai (vėsinimo/šildymo indeksas)
    #Šilumos poreikio indeksas, jei temperatūra>10
    df["silumos_poreikis"] = df["oro_temp"].apply(lambda x: 10 - x if x < 10 else 0)
    #Vėsinimo poreikio indeksas, jei temperatūra > 25
    df["vesinimo_poreikis"] = df["oro_temp"].apply(lambda x: x - 25 if x > 25 else 0)
    return df

def main():
    measurements = gauti_duomenis(URL)
    df = paruosti_duomenis(measurements)
    # DUOMENŲ IŠVESTIS (PIRMOS 10 EILUČIŲ)
    print("Meteorologinių duomenų ištrauka (pirmos 10 eilučių):")
    print(df.head(10).to_string())

if __name__ == "__main__":
    main()
