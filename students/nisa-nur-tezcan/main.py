import time
import pandas as pd
import requests
import matplotlib.pyplot as plt
import folium

from beaches import beaches

# CONSTANTS & URLS
URL_WASTE = (
    "https://data.ibb.gov.tr/api/3/action/datastore_search"
    "?resource_id=6fe63b8a-ba7d-4a13-bf21-c368d7bd37ce&limit=5000"
)

URL_TOURIST = (
    "https://data.ibb.gov.tr/api/3/action/datastore_search"
    "?resource_id=e1f59ff6-0d2f-4c51-8d57-fe97dde47d79&limit=5000"
)

YEAR = 2024
FALLBACK_TEMP = [8, 8, 9, 12, 17, 21, 24, 25, 22, 18, 14, 10]
FALLBACK_WIND = [6.5, 6.3, 6.0, 5.5, 5.3, 5.0, 5.0, 5.1, 5.4, 5.8, 6.2, 6.5]

# BASIC DATA LOADERS
def load_data(url):
    """Load IBB open data as DataFrame."""
    try:
        r = requests.get(url, timeout=10).json()
        return pd.DataFrame(r["result"]["records"])
    except Exception:
        print("Data load error:", url)
        return pd.DataFrame()


print("Loading IBB datasets...")
waste_df = load_data(URL_WASTE)
tour_df = load_data(URL_TOURIST)


# CLEAN WASTE DATA
waste_df["date"] = pd.to_datetime(waste_df["tarih"], format="%d.%m.%Y", errors="coerce")
waste_df["year"] = waste_df["date"].dt.year
waste_df["month"] = waste_df["date"].dt.month
waste_df["kg"] = pd.to_numeric(waste_df["kg_cinsinden"], errors="coerce")

annual_waste = waste_df.groupby("year")["kg"].sum().reset_index()

monthly_waste = (
    waste_df.groupby("month")["kg"]
    .mean()
    .reset_index()
    .rename(columns={"kg": "avg_waste"})
)

monthly_waste["waste_level"] = pd.qcut(
    monthly_waste["avg_waste"], 3, labels=["low", "medium", "high"]
)


def get_waste_level(m):
    row = monthly_waste[monthly_waste["month"] == m]
    return row.iloc[0]["waste_level"] if not row.empty else "unknown"


# CLEAN TOURIST DATA
tour_df["date"] = pd.to_datetime(tour_df["tarih"], errors="coerce")
tour_df["year"] = tour_df["date"].dt.year
tour_df["month"] = tour_df["date"].dt.month
tour_df["count"] = pd.to_numeric(tour_df["ziyaretci_sayisi"], errors="coerce")

# Only Istanbul rows
tour_df = tour_df[tour_df["istanbul_turkiye"] == "İstanbul"]

annual_tour = tour_df.groupby("year")["count"].sum().reset_index()

monthly_tour = (
    tour_df.groupby("month")["count"]
    .mean()
    .reset_index()
)

monthly_tour["tourist_level"] = pd.qcut(
    monthly_tour["count"], 3, labels=["low", "medium", "high"]
)


def get_tourist_level(m):
    row = monthly_tour[monthly_tour["month"] == m]
    return row.iloc[0]["tourist_level"] if not row.empty else "unknown"


# SUMMARY TABLES & ANNUAL GRAPHICS 
print("\n=== Annual Waste Summary ===")
print(annual_waste)

print("\n=== Annual Tourist Summary ===")
print(annual_tour)

print("\n=== Monthly Average Waste ===")
print(monthly_waste)

print("\n=== Monthly Average Tourists ===")
print(monthly_tour)

# --- Waste (Annual Graph)
plt.figure(figsize=(10, 5))
plt.plot(annual_waste["year"], annual_waste["kg"], marker="o")
plt.title("Yearly Coastal Waste")
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()

# --- Tourists (Annual Graph)
plt.figure(figsize=(10, 5))
plt.plot(annual_tour["year"], annual_tour["count"], marker="o", color="green")
plt.title("Yearly Tourists")
plt.grid(True, alpha=0.4)
plt.xticks(annual_tour["year"])
plt.tight_layout()
plt.show()

# --- Monthly Average Waste (Monthly Bar Chart)
plt.figure(figsize=(12, 5))
plt.bar(monthly_waste["month"], monthly_waste["avg_waste"])
plt.xticks(monthly_waste["month"])
plt.title("Monthly Average Waste (kg)")
plt.xlabel("Month")
plt.ylabel("Average Waste (kg)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- Monthly Average Tourists (Monthly Bar Chart)
plt.figure(figsize=(12, 5))
plt.bar(monthly_tour["month"], monthly_tour["count"], color="orange")
plt.xticks(monthly_tour["month"])
plt.title("Monthly Average Tourists")
plt.xlabel("Month")
plt.ylabel("Average Number of Tourists")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# CLIMATE FETCHING (DONE ONCE FOR ALL BEACHES)
def fetch_climate(lat, lon):
    """Fetch climate data (12 months) for a beach."""
    try:
        url_temp = (
            "https://marine-api.open-meteo.com/v1/marine?"
            f"latitude={lat}&longitude={lon}"
            f"&start_date={YEAR}-01-01&end_date={YEAR}-12-31"
            "&hourly=sea_surface_temperature"
        )

        url_wind = (
            "https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={lat}&longitude={lon}"
            f"&start_date={YEAR}-01-01&end_date={YEAR}-12-31"
            "&hourly=wind_speed_10m"
        )

        d1 = requests.get(url_temp, timeout=10).json()
        d2 = requests.get(url_wind, timeout=10).json()

        temp = d1.get("hourly", {}).get("sea_surface_temperature", [])
        wind = d2.get("hourly", {}).get("wind_speed_10m", [])

        tdf = pd.DataFrame({"month": range(1, 13), "sea_temp": FALLBACK_TEMP})
        wdf = pd.DataFrame({"month": range(1, 13), "wind": FALLBACK_WIND})

        if temp:
            tt = pd.DataFrame({
                "m": pd.to_datetime(d1["hourly"]["time"]).month,
                "v": temp
            })
            tdf = tt.groupby("m")["v"].mean().reset_index()
            tdf.columns = ["month", "sea_temp"]

        if wind:
            ww = pd.DataFrame({
                "m": pd.to_datetime(d2["hourly"]["time"]).month,
                "v": wind
            })
            wdf = ww.groupby("m")["v"].mean().reset_index()
            wdf.columns = ["month", "wind"]

        return pd.merge(tdf, wdf, on="month")

    except Exception:
        return pd.DataFrame({
            "month": range(1, 13),
            "sea_temp": FALLBACK_TEMP,
            "wind": FALLBACK_WIND
        })


# ---- PRELOAD CLIMATE FOR ALL BEACHES ----
print("Fetching climate data for all beaches...")
CLIMATE = {}

for b in beaches:
    key = (b["lat"], b["lon"])
    CLIMATE[key] = fetch_climate(b["lat"], b["lon"])


def get_climate(lat, lon, month):
    df = CLIMATE[(lat, lon)]
    row = df[df["month"] == month]
    return float(row.iloc[0]["sea_temp"]), float(row.iloc[0]["wind"])

# TRANSPORT API
df_beaches = pd.DataFrame(beaches)

def get_transport(lat, lon):
    """Return number of public transport points within 800m."""
    query = f"""
    [out:json];
    (
      node["highway"="bus_stop"](around:800,{lat},{lon});
      node["public_transport"="platform"](around:800,{lat},{lon});
      node["amenity"="bus_station"](around:800,{lat},{lon});
      node["railway"="station"](around:800,{lat},{lon});
      node["amenity"="ferry_terminal"](around:800,{lat},{lon});
    );
    out count;
    """

    try:
        r = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            timeout=12
        ).json()

        if "elements" in r and r["elements"]:
            tg = r["elements"][0].get("tags", {})
            cnt = tg.get("total") or tg.get("count")
            return int(cnt) if cnt else 1

        return 1

    except Exception:
        return 1

# MAP BUILDER
def build_map(df, month):
    mp = folium.Map(location=[41.05, 29.02], zoom_start=12)
    top = df.head(3)["name"].tolist()

    for _, r in df.iterrows():
        temp, wind = get_climate(r["lat"], r["lon"], month)
        color = "green" if r["name"] in top else "red"

        folium.CircleMarker(
            [r["lat"], r["lon"]],
            radius=6,
            color=color,
            popup=f"{r['name']} | {temp:.1f}°C | wind {wind:.1f}",
            tooltip=r["name"]
        ).add_to(mp)

    mp.save("istanbul_beaches_map.html")
    print("Map saved: istanbul_beaches_map.html")


# RECOMMENDATION ENGINE
def recommend(month, pref=None):
    df = df_beaches.copy()
    df["wind"] = 0.0
    df["transport"] = 0
    df["score"] = 0

    w = get_waste_level(month)
    t = get_tourist_level(month)

    print(f"\n=== Recommendations for month {month} ===")
    print("Waste level:", w)
    print("Tourist level:", t)

    for i, r in df.iterrows():
        _, wind = get_climate(r["lat"], r["lon"], month)
        df.loc[i, "wind"] = wind

        tr = get_transport(r["lat"], r["lon"])
        df.loc[i, "transport"] = tr

        score = 0

        # Wind scoring
        if wind < 6:
            score += 2
        elif wind < 10:
            score += 1

        # Waste scoring
        if w == "low":
            score += 1
        elif w == "high":
            if r["zone"] in ["Black Sea", "Islands"]:
                score += 2
            else:
                score -= 1

        # Tourist scoring
        if t == "low":
            score += 1
        elif t == "high":
            score -= 1

        # Transport scoring
        score += min(tr, 5)

        # Preference scoring
        if pref and r["type"].lower() == pref:
            score += 3

        df.loc[i, "score"] = score
        time.sleep(0.15)

    # Sorting (score -> high, wind -> low, transport -> high)
    if pref:
        df["pm"] = df["type"].str.lower() == pref
        df = df.sort_values(
            ["pm", "score", "wind", "transport"],
            ascending=[False, False, True, False]
        )
    else:
        df = df.sort_values(
            ["score", "wind", "transport"],
            ascending=[False, True, False]
        )

    # Print final sorted table
    print("\n=== Beach Score Table ===")
    print(df[["name", "zone", "type", "wind", "transport", "score"]])


    # Sea temps graph
    temps = []
    names = []

    for _, r in df.iterrows():
        t, _ = get_climate(r["lat"], r["lon"], month)
        temps.append(t)
        names.append(r["name"])

    plt.figure(figsize=(12, 5))
    plt.bar(names, temps)
    plt.xticks(rotation=70)
    plt.title(f"Sea Temperatures (Month {month})")
    plt.tight_layout()
    plt.show()

    build_map(df, month)

# MAIN
if __name__ == "__main__":
    try:
        m = int(input("\nEnter month (1-12): "))
        p = input("Preferred type (urban/natural/island/touristic, empty for none): ").strip().lower()

        if p not in ["urban", "natural", "island", "touristic"]:
            p = None

        recommend(m, p)

    except Exception as exc:
        print("Error:", exc)