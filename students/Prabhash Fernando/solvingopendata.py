import requests
import pandas as pd
import matplotlib.pyplot as plt

url_unemp = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_a?geo=LT&age=Y15-74&sex=T&unit=PC_ACT"
resp_unemp = requests.get(url_unemp)
data_unemp = resp_unemp.json()

time_index = data_unemp["dimension"]["time"]["category"]["index"]
index_to_time = {v: k for k, v in time_index.items()}
records = []
for idx_str, val in data_unemp["value"].items():
  idx = int(idx_str)
  tc = index_to_time.get(idx)
  if tc is not None:
    records.append((tc, val))

df_unemp = pd.DataFrame(records, columns=["year_str", "unemployment"])
df_unemp["year"] = pd.to_datetime(df_unemp["year_str"], format="%Y").dt.year
df_unemp = df_unemp.sort_values("year").reset_index(drop=True)

url_gdp = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?geo=LT&na_item=B1GQ&unit=CP_MEUR"
resp_gdp = requests.get(url_gdp)
data_gdp = resp_gdp.json()

time_index = data_gdp["dimension"]["time"]["category"]["index"]
index_to_time = {v: k for k, v in time_index.items()}
records_gdp = []
for idx_str, val in data_gdp["value"].items():
  idx = int(idx_str)
  tc = index_to_time.get(idx)
  if tc is not None:
    records_gdp.append((tc, val))

df_gdp = pd.DataFrame(records_gdp, columns=["year_str", "gdp_meur"])
df_gdp["year"] = pd.to_datetime(df_gdp["year_str"], format="%Y").dt.year
df_gdp = df_gdp.sort_values("year").reset_index(drop=True)

df = pd.merge(df_unemp[["year", "unemployment"]],
              df_gdp[["year", "gdp_meur"]],
              on="year", how="inner")

df["gdp_growth_pct"] = df["gdp_meur"].pct_change() * 100

print(df.tail(10))

fig, ax1 = plt.subplots(figsize=(10,6))

ax1.set_xlabel("Year")
ax1.set_ylabel("Unemployment rate (%)", color="tab:red")
ax1.plot(df["year"], df["unemployment"], color="tab:red", marker="o", label="Unemployment Rate")
ax1.tick_params(axis="y", labelcolor="tab:red")

ax2 = ax1.twinx()
ax2.set_ylabel("GDP growth rate (%)", color="tab:blue")
ax2.plot(df["year"], df["gdp_growth_pct"], color="tab:blue", marker="s", linestyle="--", label="GDP Growth")
ax2.tick_params(axis="y", labelcolor="tab:blue")

plt.title("Lithuania: Unemployment vs GDP Growth (Eurostat)")
fig.tight_layout()
plt.grid(True, axis="x")
plt.show()
