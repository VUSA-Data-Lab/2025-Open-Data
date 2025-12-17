import pandas as pd
import dask.dataframe as dd

# .compute() converts to pandas dataframe
df = dd.read_json('rta_20*.json', orient='records', lines=False).compute()

df['dataLaikas'] = pd.to_datetime(df['dataLaikas'])
df['registravimoData'] = pd.to_datetime(df['registravimoData'])
df['paskutinioRedagavimoLaikas'] = pd.to_datetime(df['paskutinioRedagavimoLaikas'])

df.to_csv("data2.csv", encoding='utf-8', index=True)
