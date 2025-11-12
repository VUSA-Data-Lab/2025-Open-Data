# data_processor.py
"""Duomenų apdorojimo modulis (OOP)."""
import pandas as pd
import numpy as np
from unidecode import unidecode
from config import FAILAS_SAULES, FAILAS_VEJO

def normalizuoti_pavadinima(pavadinimas: str) -> str:
    """Pagalbinė funkcija, standartizuojanti teksto eilutę."""
    return unidecode(pavadinimas).lower().strip()

class RegionDataProcessor:
    """Klasė, skirta apdoroti regionų saulės ir vėjo duomenis."""
    def __init__(self):
        self.saules_map = {}
        self.vejo_map = {}
        self.bendri_regionai = []
        self._find_common_regions()

    def _find_common_regions(self):
        try:
            xls_saules = pd.ExcelFile(FAILAS_SAULES)
            self.saules_map = {normalizuoti_pavadinima(p): p for p in xls_saules.sheet_names}
            xls_vejo = pd.ExcelFile(FAILAS_VEJO)
            self.vejo_map = {normalizuoti_pavadinima(p): p for p in xls_vejo.sheet_names}
            self.bendri_regionai = sorted(list(set(self.saules_map.keys()) & set(self.vejo_map.keys())))
        except FileNotFoundError:
            raise FileNotFoundError("Klaida: Duomenų failai nerasti. Patikrinkite `config.py`.")

    def get_sun_data(self, regionas_norm: str) -> pd.DataFrame:
        sheet_name = self.saules_map[regionas_norm]
        df = pd.read_excel(FAILAS_SAULES, sheet_name=sheet_name, skiprows=3)
        df = df.iloc[:, :14]
        df.columns = ['Metai','Sau','Vas','Kov','Bal','Geg','Bir','Lie','Rgp','Rgs','Spa','Lap','Grd','Suma']
        df['Metai'] = pd.to_numeric(df['Metai'], errors='coerce')
        df = df.dropna(subset=['Metai'])
        df = df.replace('*', np.nan)
        df['Metai'] = df['Metai'].astype(int)
        return df

    def get_wind_data(self, regionas_norm: str) -> pd.DataFrame:
        sheet_name = self.vejo_map[regionas_norm]
        df = pd.read_excel(FAILAS_VEJO, sheet_name=sheet_name, skiprows=1)
        df = df.iloc[:, :11]
        df.columns = ['Laikotarpis','Rodiklis','Š','ŠR','R','PR','P','PV','V','ŠV','Tyka']
        df['Laikotarpis'] = df['Laikotarpis'].ffill()
        df = df.dropna(subset=['Rodiklis'])
        df['Tyka'].fillna(0, inplace=True)
        return df