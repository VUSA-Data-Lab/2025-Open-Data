import os
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt


class EVVisualizer:
    """
    Handles generation of plots, maps, and statistical reports.
    """

    def __init__(self, df, output_dir="output"):
        self.df = df
        self.output_dir = output_dir
        self.map_dir = os.path.join(output_dir, "maps")
        self.plot_dir = os.path.join(output_dir, "plots")

        os.makedirs(self.map_dir, exist_ok=True)
        os.makedirs(self.plot_dir, exist_ok=True)

    def generate_map(self):
        """Creates an interactive Folium map."""
        print("Generating interactive map...")
        # Center on Lithuania
        m = folium.Map(location=[55.1694, 23.8813], zoom_start=7)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in self.df.iterrows():
            color = 'red' if row['maxPowerAtSocket'] >= 50 else 'green'
            
            # Format popup text (split lines for PEP8)
            site_name = row.get('energyInfrastructureSiteName')
            power = row['maxPowerAtSocket']
            popup_text = f"Site: {site_name}<br>Power: {power} kW"

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color=color,
                fill=True,
                fill_opacity=0.7,
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(marker_cluster)

        output_path = os.path.join(self.map_dir, "lithuania_ev_map.html")
        m.save(output_path)
        print(f"Map saved to {output_path}")

    def generate_growth_chart(self):
        """Generates a charging station growth chart over time."""
        print("Generating growth analysis...")
        df_sorted = self.df.sort_values('lastUpdated')
        df_sorted['cumulative'] = range(1, len(df_sorted) + 1)

        plt.figure(figsize=(10, 6))
        plt.plot(
            df_sorted['lastUpdated'],
            df_sorted['cumulative'],
            color='blue',
            linewidth=2
        )
        plt.title('Cumulative Growth of EV Stations in Lithuania')
        plt.xlabel('Date')
        plt.ylabel('Total Stations')
        plt.grid(True)

        output_path = os.path.join(self.plot_dir, "growth_chart.png")
        plt.savefig(output_path)
        plt.close()
        print(f"Growth chart saved to {output_path}")

    def generate_power_distribution(self):
        """Generates a histogram of power capabilities."""
        plt.figure(figsize=(10, 6))
        plt.hist(
            self.df['maxPowerAtSocket'],
            bins=30,
            color='green',
            edgecolor='black'
        )
        plt.title('Distribution of Charging Power (kW)')
        plt.xlabel('Power (kW)')
        plt.ylabel('Frequency')

        output_path = os.path.join(self.plot_dir, "power_dist.png")
        plt.savefig(output_path)
        plt.close()
        print(f"Power distribution chart saved to {output_path}")