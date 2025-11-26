import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_a?geo=LT&age=Y15-74&sex=T&unit=PC_ACT"
resp = requests.get(url)
data = resp.json()

time_index = data["dimension"]["time"]["category"]["index"]
index_to_time = {v: k for k, v in time_index.items()}

records = []
for idx_str, val in data["value"].items():
  idx = int(idx_str)
  tc = index_to_time.get(idx)
  if tc is not None:
    records.append((tc, val))

df = pd.DataFrame(records, columns=["time_code", "unemployment"])

df["date"] = pd.to_datetime(df["time_code"], format="%Y", errors="coerce")
df = df.dropna().sort_values("date").reset_index(drop=True)

df["year"] = df["date"].dt.year
annual_avg = df.groupby("year")["unemployment"].mean().reset_index()

print(annual_avg.tail(10))

plt.plot(annual_avg["year"], annual_avg["unemployment"], marker="o")
plt.title("Lithuania Annual Unemployment Rate (UNE_RT_A)")
plt.xlabel("Year")
plt.ylabel("Unemployment (%)")
plt.grid(True)
plt.tight_layout()
plt.show()
