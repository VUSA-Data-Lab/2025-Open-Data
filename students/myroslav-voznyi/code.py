
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 60)
print("Testing COVID-19 Vaccination Analysis")
print("=" * 60)
print()

print("Step 1: Loading data...")
url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"

try:
    df = pd.read_csv(url)
    print(f"✓ Data loaded successfully!")
    print(f"  - Rows: {len(df)}")
    print(f"  - Columns: {len(df.columns)}")
    print()
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit()


print("Step 2: Cleaning data...")
df['date'] = pd.to_datetime(df['date'])
df = df.dropna(subset=['location'])
print(f"✓ Data cleaned!")
print()

print("Step 3: Getting latest data...")
latest = df.sort_values('date').groupby('location').tail(1).reset_index(drop=True)
print(f"✓ Latest data extracted for {len(latest)} locations")
print()

print("=" * 60)
print("TOP 10 COUNTRIES BY TOTAL VACCINATIONS")
print("=" * 60)
top10 = latest.nlargest(10, 'total_vaccinations')[['location', 'total_vaccinations']]
print(top10.to_string(index=False))
print()

print("Creating visualization...")
plt.figure(figsize=(12, 6))
top10_plot = latest.nlargest(10, 'total_vaccinations')
plt.barh(top10_plot['location'], top10_plot['total_vaccinations'], color='steelblue')
plt.xlabel('Total Vaccinations', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.title('Top 10 Countries by Total Vaccinations', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print()
print("=" * 60)
print("✓ Test completed successfully!")
print("=" * 60)
