import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# PEP8 standartas: Klasės pavadinimas CamelCase, metodai snake_case.

class EarthquakeAnalyzer:
    """
    Klasė, skirta gauti, apdoroti ir vizualizuoti USGS žemės drebėjimų duomenis.
    """

    def __init__(self, url):
        """
        Inicijuoja analizatorių su duomenų šaltinio nuoroda.
        """
        self.url = url
        self.data = None
        self.df = None

    def fetch_data(self):
        """
        Atsiunčia duomenis iš API JSON formatu.
        """
        try:
            print(f"Siunčiami duomenys iš: {self.url}...")
            response = requests.get(self.url)
            response.raise_for_status()  # Patikrina, ar nėra HTTP klaidų
            self.data = response.json()
            print("Duomenys sėkmingai gauti.")
        except requests.exceptions.RequestException as e:
            print(f"Klaida gaunant duomenis: {e}")

    def process_data(self):
        """
        Konvertuoja JSON duomenis į Pandas DataFrame ir atlieka valymą.
        """
        if not self.data or 'features' not in self.data:
            print("Nėra duomenų apdorojimui.")
            return

        earthquakes = []
        for feature in self.data['features']:
            props = feature['properties']
            # Konvertuojame laiko žymą (timestamp) į skaitomą formatą
            time_readable = datetime.fromtimestamp(props['time'] / 1000).strftime('%Y-%m-%d %H:%M')
            
            earthquakes.append({
                'location': props['place'],
                'magnitude': props['mag'],
                'time': time_readable,
                'url': props['url']
            })

        # Sukuriame DataFrame
        self.df = pd.DataFrame(earthquakes)
        
        # Filtravimas: paliekame tik tuos, kurių magnitudė > 0 (išvalome klaidingus įrašus)
        self.df = self.df[self.df['magnitude'] > 0]
        
        # Rikiavimas pagal stiprumą
        self.df = self.df.sort_values(by='magnitude', ascending=False)
        print("Duomenys apdoroti ir surikiuoti.")

    def get_statistics(self):
        """
        Grąžina pagrindinę statistiką.
        """
        if self.df is None:
            return "Nėra duomenų."
        
        stats = {
            'Viso įvykių': len(self.df),
            'Vidutinė magnitudė': round(self.df['magnitude'].mean(), 2),
            'Stipriausias drebėjimas': self.df.iloc[0]['magnitude'],
            'Stipriausia vieta': self.df.iloc[0]['location']
        }
        return stats

    def visualize_top_5(self):
        """
        Sukuria stulpelinę diagramą 5 stipriausiems žemės drebėjimams.
        """
        if self.df is None:
            print("Nėra duomenų vizualizacijai.")
            return

        top_5 = self.df.head(5)

        plt.figure(figsize=(10, 6))
        plt.barh(top_5['location'], top_5['magnitude'], color='salmon')
        plt.xlabel('Magnitudė')
        plt.title('Top 5 stipriausi žemės drebėjimai (per pastarąją parą)')
        plt.gca().invert_yaxis()  # Didžiausia reikšmė viršuje
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Išsaugome grafiką
        plt.savefig('rezultatas_grafikas.png')
        print("Grafikas išsaugotas kaip 'rezultatas_grafikas.png'.")
        plt.show()

def main():
    # USGS (United States Geological Survey) atvirieji duomenys
    # Pastarosios paros visi žemės drebėjimai
    DATA_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

    app = EarthquakeAnalyzer(DATA_URL)
    
    # Vykdymo eiga
    app.fetch_data()
    app.process_data()
    
    # Rezultatų išvedimas į konsolę
    stats = app.get_statistics()
    print("\n--- STATISTIKA ---")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n--- 5 STIPRIAUSI DREBĖJIMAI ---")
    print(app.df.head(5)[['time', 'magnitude', 'location']].to_string(index=False))

    # Vizualizacija
    app.visualize_top_5()

if __name__ == "__main__":
    main()
