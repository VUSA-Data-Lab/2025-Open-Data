import pandas as pd
import matplotlib.pyplot as plt
import os


file_path = r"C:\Users\Emin\source\repos\gpr\sdg_08_10__custom_15823777_linear.csv"
df = pd.read_csv(file_path)

df = df[["geo", "TIME_PERIOD", "OBS_VALUE"]]
df = df.rename(columns={"TIME_PERIOD": "year", "OBS_VALUE": "value"})

print("Cleaned dataset sample:")
print(df.head(), "\n")


countries = ["Lithuania", "Germany", "European Union - 27 countries (from 2020)"]
df_filtered = df[df["geo"].isin(countries)]

df_pivot = df_filtered.pivot(index="year", columns="geo", values="value").sort_index()

print("Pivoted dataset:")
print(df_pivot.head(), "\n")

save_path = r"C:\Users\Emin\source\repos\gpr"
os.makedirs(save_path, exist_ok=True)


plt.figure(figsize=(10, 6))
for country in countries:
    plt.plot(df_pivot.index, df_pivot[country], marker="o", label=country)

plt.title("Real GDP per capita (chain-linked volumes, euro, 2020 prices)")
plt.xlabel("Year")
plt.ylabel("EUR per capita")
plt.legend(title="Country")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(save_path, "gdp_line_all.png"))
plt.show()


growth = df_pivot.pct_change().mean() * 100
print("Average annual growth rate (%):")
print(growth, "\n")
 
plt.figure(figsize=(6, 4))
growth.plot(kind="bar", color="skyblue")
plt.title("Average Annual Growth Rate of Real GDP per Capita")
plt.ylabel("% Growth")
plt.tight_layout()
plt.savefig(os.path.join(save_path, "gdp_growth_bar.png"))
plt.show()


plt.figure(figsize=(8, 5))
plt.plot(df_pivot.index, df_pivot["Lithuania"], marker="o", label="Lithuania", linewidth=2)
plt.plot(df_pivot.index, df_pivot["European Union - 27 countries (from 2020)"],
         marker="s", label="EU27 Average", linestyle="--")
plt.title("Lithuania vs EU27: Real GDP per Capita")
plt.xlabel("Year")
plt.ylabel("EUR per capita")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(save_path, "gdp_lithuania_vs_eu.png"))
plt.show()
