import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
from io import StringIO

def load_data():
    try:
        url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/tps00150/1.0/*.*.*.*.*?c[freq]=A&c[unit]=YR&c[sex]=T&c[indic_he]=HLY_0&c[geo]=EU27_2020,BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,HU,MT,NL,AT,PL,PT,RO,SI,SK,FI,SE,IS,NO,CH,UK,AL,EA19,EA20,LI,ME,MK,RS,TR&c[TIME_PERIOD]=2019,2020,2021,2022,2023&compress=false&format=csvdata&formatVersion=2.0&lang=en&labels=name"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = StringIO(response.text)
        df = pd.read_csv(data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to download the file from {url}. Error: {e}")
        return None
    except pd.errors.ParserError:
        print("Error: Failed to parse the CSV file. Please check the file format.")
        return None

def clean_data(df):
    if df is None:
        return None
    df = df[['geo', 'Geopolitical entity (reporting)', 'TIME_PERIOD', 'OBS_VALUE', 'OBS_FLAG']]
    df = df[df['OBS_VALUE'].notnull()]
    df['OBS_VALUE'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')
    
    # Store EU average before removing it
    eu_data = df[df['geo'] == 'EU27_2020'].copy()
    
    df = df[df['geo'] != 'EU27_2020']
    df['OBS_FLAG'] = df['OBS_FLAG'].fillna('normal')
    df['Data_Reliability'] = df['OBS_FLAG'].apply(
        lambda x: 'Break in series' if 'b' in str(x) else
                 'Provisional' if 'p' in str(x) else
                 'Estimated' if 'e' in str(x) else 'Normal'
    )
    return df, eu_data

def create_visualizations(df_clean, eu_data):
    if df_clean is None:
        return

    # Visualization 1: Trends over time
    plt.figure(figsize=(10, 6))
    for country in df_clean['geo'].unique():
        country_data = df_clean[df_clean['geo'] == country]
        plt.plot(country_data['TIME_PERIOD'], country_data['OBS_VALUE'], label=country)
    plt.title('Healthy Life Years at Birth by Country (2019-2023)')
    plt.xlabel('Year')
    plt.ylabel('Healthy Life Years')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # Visualization 2: 2023 Comparison with EU Average (Enhanced)
    df_2023 = df_clean[df_clean['TIME_PERIOD'] == 2023].sort_values('OBS_VALUE', ascending=False)
    eu_2023_value = eu_data[eu_data['TIME_PERIOD'] == 2023]['OBS_VALUE'].values
    
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x='OBS_VALUE', y='Geopolitical entity (reporting)', hue='Data_Reliability', data=df_2023)
    
    # Add EU average vertical line
    if len(eu_2023_value) > 0:
        plt.axvline(x=eu_2023_value[0], color='red', linestyle='--', linewidth=2, label=f'EU Average: {eu_2023_value[0]:.1f}')
        plt.legend(loc='lower right')
    
    plt.title('Healthy Life Years at Birth in 2023 (with EU Average)')
    plt.xlabel('Healthy Life Years')
    plt.ylabel('Country')
    plt.tight_layout()
    plt.show()

    # Visualization 3: Box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='TIME_PERIOD', y='OBS_VALUE', data=df_clean)
    plt.title('Distribution of Healthy Life Years (2019-2023)')
    plt.xlabel('Year')
    plt.ylabel('Healthy Life Years')
    plt.tight_layout()
    plt.show()

    # NEW Visualization 4: 2D Comparison - 2019 vs 2023
    df_pivot = df_clean.pivot(index='geo', columns='TIME_PERIOD', values='OBS_VALUE').reset_index()
    
    # Filter to only countries with both 2019 and 2023 data
    df_comparison = df_pivot[df_pivot[2019].notnull() & df_pivot[2023].notnull()].copy()
    
    # Get country names for labels
    country_names = df_clean[['geo', 'Geopolitical entity (reporting)']].drop_duplicates()
    df_comparison = df_comparison.merge(country_names, on='geo', how='left')
    
    plt.figure(figsize=(12, 10))
    
    # Scatter plot
    plt.scatter(df_comparison[2019], df_comparison[2023], s=100, alpha=0.6, edgecolors='black')
    
    # Add diagonal line (y=x) to show where values are equal
    min_val = min(df_comparison[2019].min(), df_comparison[2023].min())
    max_val = max(df_comparison[2019].max(), df_comparison[2023].max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.5, linewidth=2, label='No Change Line')
    
    # Add country labels
    for idx, row in df_comparison.iterrows():
        plt.annotate(row['geo'], 
                    (row[2019], row[2023]),
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontsize=8,
                    alpha=0.7)
    
    # Add EU average reference if available
    eu_2019_value = eu_data[eu_data['TIME_PERIOD'] == 2019]['OBS_VALUE'].values
    eu_2023_value = eu_data[eu_data['TIME_PERIOD'] == 2023]['OBS_VALUE'].values
    
    if len(eu_2019_value) > 0 and len(eu_2023_value) > 0:
        plt.axvline(x=eu_2019_value[0], color='blue', linestyle=':', alpha=0.5, label=f'EU Avg 2019: {eu_2019_value[0]:.1f}')
        plt.axhline(y=eu_2023_value[0], color='green', linestyle=':', alpha=0.5, label=f'EU Avg 2023: {eu_2023_value[0]:.1f}')
        plt.scatter(eu_2019_value[0], eu_2023_value[0], s=200, c='red', marker='*', 
                   edgecolors='black', linewidths=2, label='EU Average', zorder=5)
    
    plt.xlabel('Healthy Life Years in 2019')
    plt.ylabel('Healthy Life Years in 2023')
    plt.title('2D Comparison: HLY 2019 vs 2023\n(Points above red line = improvement, below = decline)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Problem Definition")
    print("""
    Problem: Disparities in healthy life years (HLY) at birth across European countries highlight inequalities in
    healthcare systems, socio-economic conditions, and lifestyle factors. Addressing these disparities can inform
    health policy to improve overall population health and reduce inequalities.

    Objective: Analyze HLY trends from 2019 to 2023 to identify countries with significant improvements or declines,
    highlight outliers, and explore potential socio-economic or policy-driven factors.
    """)

    print("\nData Source and Cleaning")
    print("""
    Dataset: Eurostat TPS00150 - Healthy life years at birth by sex.
    - Source: Publicly available Eurostat data.
    - Schema: Columns include `geo` (country), `TIME_PERIOD` (year), `OBS_VALUE` (HLY), `OBS_FLAG` (data status).
    Cleaning Steps:
    1. Select relevant columns: `geo`, `Geopolitical entity (reporting)`, `TIME_PERIOD`, `OBS_VALUE`, `OBS_FLAG`.
    2. Remove rows with missing `OBS_VALUE`.
    3. Convert `OBS_VALUE` to numeric.
    4. Store EU27_2020 aggregate for reference before excluding from country analysis.
    5. Handle flags for data reliability.
    """)

    df = load_data()
    result = clean_data(df)
    
    if result is not None:
        df_clean, eu_data = result
        
        print("\nDescriptive Statistics")
        stats = df_clean.groupby('geo')['OBS_VALUE'].agg(['mean', 'median', 'std']).reset_index()
        print(stats)

        print("\nAnalytical Methods")
        print("""
        1. Descriptive Statistics: Calculate mean, median, and standard deviation of HLY by country and year.
        2. Trend Analysis: Analyze HLY trends over time for each country using line plots.
        3. Comparative Analysis: Compare HLY across countries for 2023 to identify top and bottom performers.
        4. 2D Comparison: Visualize 2019 vs 2023 values to identify improvement patterns.
        5. Outlier Detection: Identify countries with significant changes (>5 years) in HLY from 2019 to 2023.
        6. Visualization: Use line charts, bar charts, box plots, and scatter plots to visualize trends and distributions.
        """)

        create_visualizations(df_clean, eu_data)

        print("\nOutlier Detection: Significant HLY Changes (2019-2023)")
        df_pivot = df_clean.pivot(index='geo', columns='TIME_PERIOD', values='OBS_VALUE').reset_index()
        df_pivot['Change_2019_2023'] = df_pivot[2023] - df_pivot[2019]
        outliers = df_pivot[df_pivot['Change_2019_2023'].abs() > 5][['geo', 'Change_2019_2023']]
        print(outliers)