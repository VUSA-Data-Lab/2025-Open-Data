import pandas as pd


def process(df: pd.DataFrame, vname: str) -> pd.DataFrame:
    df = df[df["Klassifikator_en"] == "Republic of Uzbekistan"]
    df = df.drop(columns=["Code", "Klassifikator", "Klassifikator_ru", "Klassifikator_uzc"])

    melted_df = df.melt(id_vars=["Klassifikator_en"], var_name="year", value_name=vname)
    melted_df = melted_df.drop(columns=["Klassifikator_en"])

    return melted_df