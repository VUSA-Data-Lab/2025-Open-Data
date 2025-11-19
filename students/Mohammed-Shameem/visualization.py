# visualization.py
import matplotlib.pyplot as plt
import pandas as pd


class NeoVisualizer:
    """
    Contains methods for visualizing asteroid data.
    """

    @staticmethod
    def plot_diameter_distribution(df: pd.DataFrame, save=False):
        plt.figure(figsize=(10, 6))
        plt.hist(df["diameter_max_m"], bins=20)
        plt.title("Asteroid Maximum Diameter Distribution")
        plt.xlabel("Diameter (meters)")
        plt.ylabel("Count")
        plt.grid(True)

        if save:
            plt.savefig("diameter_distribution.png")

        plt.show()

    @staticmethod
    def plot_hazardous_pie(df: pd.DataFrame, save=False):
        counts = df["is_hazardous"].value_counts()

        plt.figure(figsize=(6, 6))
        plt.pie(counts, labels=["Non-Hazardous", "Hazardous"], autopct="%1.1f%%")
        plt.title("Hazardous vs Non-Hazardous Asteroids")

        if save:
            plt.savefig("hazardous_pie.png")

        plt.show()

    @staticmethod
    def plot_velocity(df: pd.DataFrame, save=False):
        plt.figure(figsize=(10, 6))
        plt.scatter(df["diameter_max_m"], df["velocity_km_s"])
        plt.title("Velocity vs Diameter")
        plt.xlabel("Diameter (meters)")
        plt.ylabel("Velocity (km/s)")
        plt.grid(True)

        if save:
            plt.savefig("velocity_vs_diameter.png")

        plt.show()
