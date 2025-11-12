# main.py
"""Pagrindinis programos paleidimo failas."""
import warnings
from data_processing import RegionDataProcessor
from data_visualization import DataVisualizer

def main():
    """Pagrindinė programos funkcija."""
    warnings.simplefilter(action='ignore', category=FutureWarning)
    try:
        processor = RegionDataProcessor()
        if not processor.bendri_regionai:
            print("KLAIDA: Nerasta bendrų regionų tarp abiejų Excel failų.")
            return
        print(f"Rasti bendri regionai: {', '.join(b.title() for b in processor.bendri_regionai)}\n")
        visualizer = DataVisualizer()
        for regionas_norm in processor.bendri_regionai:
            orig_saules_lapas = processor.saules_map[regionas_norm]
            orig_vejo_lapas = processor.vejo_map[regionas_norm]
            print("="*80)
            print(f"--- APDOROJAMI DUOMENYS REGIONUI: {orig_vejo_lapas.upper()} ---")
            print("="*80)
            df_saules = processor.get_sun_data(regionas_norm)
            df_vejo = processor.get_wind_data(regionas_norm)
            visualizer.print_data_tables(df_saules, df_vejo, orig_saules_lapas, orig_vejo_lapas)
            visualizer.plot_and_save_charts(df_saules, df_vejo, orig_saules_lapas)
            print("\n\n")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Įvyko netikėta klaida: {e}")

if __name__ == "__main__":
    main()