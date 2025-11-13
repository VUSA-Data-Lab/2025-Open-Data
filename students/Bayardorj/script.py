import warnings

import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

# -----------------------------
# Setup and Data Loading
# -----------------------------

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load the dataset
df = pd.read_csv('demo_gind__custom_7680622_linear_2_0.csv')

# Display basic information
print("Dataset shape:", df.shape)

# -----------------------------
# Data Cleaning
# -----------------------------

# Filter for Italy data only
italy_data = df[df['geo'] == 'IT'].copy()

# Select relevant columns and clean data
italy_clean = italy_data[['TIME_PERIOD', 'OBS_VALUE']].copy()
italy_clean.columns = ['year', 'population']
italy_clean['year'] = italy_clean['year'].astype(int)
italy_clean['population'] = italy_clean['population'].astype(float)

# Remove duplicates and sort by year
italy_clean = italy_clean.drop_duplicates(subset=['year']).sort_values('year')

print("\nData range:", italy_clean['year'].min(), "to", italy_clean['year'].max())

# -----------------------------
# Feature Engineering
# -----------------------------

# Calculate year-over-year changes
italy_clean['population_change'] = italy_clean['population'].diff()
italy_clean['population_pct_change'] = (
    italy_clean['population'].pct_change() * 100
)

# Calculate 5-year moving average for trend analysis
italy_clean['population_5yr_ma'] = italy_clean['population'].rolling(window=5).mean()

print("\nCleaned Italy population data:")
print(italy_clean.head(20))

# -----------------------------
# Statistics
# -----------------------------

total_change = (
    italy_clean['population'].iloc[-1] - italy_clean['population'].iloc[0]
)
pct_change_total = (
    (total_change / italy_clean['population'].iloc[0]) * 100
)

print(f"Total population change (2006–2025): {total_change:,.0f}")
print(f"Percentage change: {pct_change_total:.2f}%")

# Find the peak population year
peak_year = italy_clean.loc[italy_clean['population'].idxmax()]
print(f"\nPeak population: {peak_year['population']:,.0f} in {int(peak_year['year'])}")

# Calculate average annual decline in recent years (last 10 years)
recent_data = italy_clean[italy_clean['year'] >= 2015]
avg_annual_decline = recent_data['population_change'].mean()
print(f"Average annual decline (2015–2025): {avg_annual_decline:,.0f}")

# -----------------------------
# Visualization
# -----------------------------

fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle(
    'Italy Population Analysis: Demographic Decline Crisis',
    fontsize=16,
    fontweight='bold'
)

# Plot 1: Population Trend
axes[0, 0].plot(
    italy_clean['year'],
    italy_clean['population'],
    linewidth=2.5,
    marker='o',
    markersize=4,
    label='Actual Population'
)
axes[0, 0].plot(
    italy_clean['year'],
    italy_clean['population_5yr_ma'],
    linewidth=2,
    linestyle='--',
    alpha=0.8,
    label='5-Year Moving Average'
)
axes[0, 0].set_title('Italy Population Trend (2006–2025)', fontweight='bold')
axes[0, 0].set_xlabel('Year')
axes[0, 0].set_ylabel('Population')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].ticklabel_format(style='plain', axis='y')

# Highlight the peak year
peak_idx = italy_clean['population'].idxmax()
axes[0, 0].annotate(
    f'Peak: {italy_clean.loc[peak_idx, "population"]:,.0f}',
    xy=(
        italy_clean.loc[peak_idx, 'year'],
        italy_clean.loc[peak_idx, 'population']
    ),
    xytext=(10, 10),
    textcoords='offset points',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.1),
    arrowprops=dict(arrowstyle='->', color='red')
)

# Plot 2: Annual Population Change
axes[0, 1].bar(
    italy_clean['year'],
    italy_clean['population_change'],
    color=[
        'red' if x < 0 else 'green'
        for x in italy_clean['population_change']
    ],
    alpha=0.7
)
axes[0, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
axes[0, 1].set_title('Annual Population Change', fontweight='bold')
axes[0, 1].set_xlabel('Year')
axes[0, 1].set_ylabel('Change in Population')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Percentage Change
axes[1, 0].plot(
    italy_clean['year'],
    italy_clean['population_pct_change'],
    linewidth=2,
    marker='s',
    markersize=4,
    color='orange'
)
axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
axes[1, 0].fill_between(
    italy_clean['year'],
    italy_clean['population_pct_change'],
    where=(italy_clean['population_pct_change'] < 0),
    color='red',
    alpha=0.3
)
axes[1, 0].set_title('Annual Percentage Change', fontweight='bold')
axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('Percentage Change (%)')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Cumulative Change from Peak
peak_pop = italy_clean['population'].max()
italy_clean['change_from_peak'] = italy_clean['population'] - peak_pop
axes[1, 1].fill_between(
    italy_clean['year'],
    italy_clean['change_from_peak'],
    color='red',
    alpha=0.6
)
axes[1, 1].plot(
    italy_clean['year'],
    italy_clean['change_from_peak'],
    linewidth=2,
    color='darkred'
)
axes[1, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
axes[1, 1].set_title('Cumulative Population Loss from Peak', fontweight='bold')
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Population Loss')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -----------------------------
# Projection
# -----------------------------

# Use last 10 years for projection
recent_years = italy_clean[italy_clean['year'] >= 2015].copy()
X = recent_years[['year']]
y = recent_years['population']

model = LinearRegression()
model.fit(X, y)

# Project next 10 years
future_years = np.array(range(2026, 2036)).reshape(-1, 1)
future_population = model.predict(future_years)

# Create projection dataframe
projection_df = pd.DataFrame({
    'year': range(2026, 2036),
    'population': future_population
})

# Combine actual and projected data
combined_data = pd.concat(
    [italy_clean[['year', 'population']], projection_df],
    ignore_index=True
)
combined_data['type'] = (
    ['Actual'] * len(italy_clean) + ['Projected'] * len(projection_df)
)

# Plot projection
plt.figure(figsize=(12, 6))

# Plot actual and projected data
actual_data = combined_data[combined_data['type'] == 'Actual']
projected_data = combined_data[combined_data['type'] == 'Projected']

plt.plot(
    actual_data['year'],
    actual_data['population'],
    linewidth=2.5,
    marker='o',
    label='Actual',
    color='blue'
)
plt.plot(
    projected_data['year'],
    projected_data['population'],
    linewidth=2.5,
    linestyle='--',
    marker='s',
    label='Projected',
    color='red'
)

plt.title(
    'Italy Population Trend with 10-Year Projection',
    fontsize=14,
    fontweight='bold'
)
plt.xlabel('Year')
plt.ylabel('Population')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Add annotations
current_pop = italy_clean['population'].iloc[-1]
projected_2035 = projection_df['population'].iloc[-1]
total_decline = projected_2035 - current_pop

plt.annotate(
    f'Projected 2035: {projected_2035:,.0f}\n'
    f'Additional decline: {total_decline:,.0f}',
    xy=(2035, projected_2035),
    xytext=(2028, projected_2035 + 500_000),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='red', alpha=0.1),
    arrowprops=dict(arrowstyle='->', color='red')
)

plt.tight_layout()
plt.show()

print(f"Projected population in 2035: {projected_2035:,.0f}")
print(f"Additional decline from 2025 to 2035: {total_decline:,.0f}")

# -----------------------------
# Summary Statistics
# -----------------------------

summary_stats = {
    'Metric': [
        'Starting Population (2006)',
        'Peak Population',
        'Current Population (2025)',
        'Total Change (2006–2025)',
        'Percentage Change',
        'Peak Year',
        'Years of Decline',
        'Average Annual Decline (2015–2025)',
        'Projected 2035 Population',
        'Additional Projected Decline'
    ],
    'Value': [
        f"{italy_clean['population'].iloc[0]:,.0f}",
        f"{peak_year['population']:,.0f}",
        f"{italy_clean['population'].iloc[-1]:,.0f}",
        f"{total_change:,.0f}",
        f"{pct_change_total:.2f}%",
        f"{int(peak_year['year'])}",
        f"{2025 - int(peak_year['year'])} years",
        f"{avg_annual_decline:,.0f}",
        f"{projected_2035:,.0f}",
        f"{total_decline:,.0f}"
    ]
}

summary_df = pd.DataFrame(summary_stats)

print("\nITALY POPULATION CRISIS – KEY FINDINGS")
print("=" * 50)
print(summary_df.to_string(index=False))

