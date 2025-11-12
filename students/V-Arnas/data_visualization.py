# data_visualizer.py
"""
Duomenų vizualizavimo modulis, naudojant OOP principus.

Šiame modulyje aprašyta `DataVisualizer` klasė, kuri atsako už
duomenų pateikimą: lentelių spausdinimą į konsolę ir grafikų generavimą.
"""
import matplotlib.pyplot as plt
from tabulate import tabulate
from data_processing import normalizuoti_pavadinima
import pandas as pd # Reikalingas tipų anotacijoms

class DataVisualizer:
    """Klasė, skirta duomenų pateikimui ir vizualizavimui."""

    @staticmethod
    def _format_wind_table(df: pd.DataFrame):
        """
        Specializuota funkcija, kuri suformatuoja vėjo duomenis
        pagal pageidaujamą vizualinį stilių, grupuodama eilutes.
        """
        header = (
            "| {:<13} | {:<9} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5} | {:>5} | {:>6} |"
            .format("Laikotarpis", "Rodiklis", "Š", "ŠR", "R", "PR", "P", "PV", "V", "ŠV", "Tyka")
        )
        separator = "-" * len(header)
        
        print(separator)
        print(header)
        print(separator)

        for laikotarpis in df['Laikotarpis'].unique():
            laikotarpio_df = df[df['Laikotarpis'] == laikotarpis]
            proc_eilute = laikotarpio_df[laikotarpio_df['Rodiklis'] == '%'].iloc[0]
            ms_eilute = laikotarpio_df[laikotarpio_df['Rodiklis'] == 'm/s'].iloc[0]

            print(
                "| {:<13} | {:<9} | {:>5.0f} | {:>5.0f} | {:>5.0f} | {:>5.0f} | {:>5.0f} | {:>5.0f} | {:>5.0f} | {:>5.0f} | {:>6.0f} |"
                .format(
                    laikotarpis, proc_eilute['Rodiklis'], proc_eilute['Š'], proc_eilute['ŠR'], proc_eilute['R'],
                    proc_eilute['PR'], proc_eilute['P'], proc_eilute['PV'], proc_eilute['V'], proc_eilute['ŠV'], proc_eilute['Tyka']
                )
            )
            
            print(
                "| {:<13} | {:<9} | {:>5.1f} | {:>5.1f} | {:>5.1f} | {:>5.1f} | {:>5.1f} | {:>5.1f} | {:>5.1f} | {:>5.1f} | {:>6.1f} |"
                .format(
                    "", ms_eilute['Rodiklis'], ms_eilute['Š'], ms_eilute['ŠR'], ms_eilute['R'],
                    ms_eilute['PR'], ms_eilute['P'], ms_eilute['PV'], ms_eilute['V'], ms_eilute['ŠV'], ms_eilute['Tyka']
                )
            )
            
            print(separator)

    @staticmethod
    def print_data_tables(df_saules, df_vejo, saules_lapas, vejo_lapas):
        """Išspausdina suformatuotas ir PILNAS saulės bei vėjo duomenų lenteles."""
        print(f"\n--- 1. {saules_lapas}: Saulės spindėjimo trukmės duomenys ---\n")
        
        # Pakeičiame 'nan' į '-' prieš spausdinant
        df_saules_display = df_saules.fillna('-')

        # PATAISYMAS: Nebenaudojame .head() ir .tail(), spausdiname visą lentelę
        print(tabulate(df_saules_display, headers='keys', tablefmt='psql', showindex=False))
        
        print(f"\n--- 2. {vejo_lapas}: Vėjo greičio duomenys ---\n")
        # Kviečiame savo specializuotą formatavimo funkciją, kuri spausdina viską
        DataVisualizer._format_wind_table(df_vejo)

    @staticmethod
    def plot_and_save_charts(df_saules, df_vejo, region_name):
        """Sukuria ir išsaugo saulės ir vėjo duomenų grafikus."""
        # Saulės grafiko kodas lieka toks pat
        plt.figure(figsize=(12, 6))
        plt.plot(df_saules['Metai'], df_saules['Suma'], marker='o', linestyle='-', color='orange')
        plt.title(f'Metinė saulės spindėjimo trukmė: {region_name}', fontsize=16)
        plt.xlabel('Metai', fontsize=12)
        plt.ylabel('Bendra trukmė (valandos)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        sun_filename = f"{normalizuoti_pavadinima(region_name)}_saules_spindejimas.png"
        plt.savefig(sun_filename)
        plt.close()
        print(f"\nGrafikas sėkmingai išsaugotas faile: {sun_filename}")

        # Vėjo grafiko kodas lieka toks pat
        df_metu = df_vejo[(df_vejo['Laikotarpis'] == 'Metų') & (df_vejo['Rodiklis'] == '%')]
        if not df_metu.empty:
            wind_data = df_metu.iloc[0]
            directions = ['Š', 'ŠR', 'R', 'PR', 'P', 'PV', 'V', 'ŠV']
            frequencies = wind_data[directions]
            plt.figure(figsize=(12, 6))
            plt.bar(directions, frequencies, color='skyblue')
            plt.title(f'Metinis vėjo pasikartojimo dažnis pagal kryptis: {region_name}', fontsize=16)
            plt.xlabel('Vėjo kryptis', fontsize=12)
            plt.ylabel('Pasikartojimo dažnis (%)', fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            wind_filename = f"{normalizuoti_pavadinima(region_name)}_vejo_pasiskirstymas.png"
            plt.savefig(wind_filename)
            plt.close()
            print(f"Grafikas sėkmingai išsaugotas faile: {wind_filename}")