import pandas as pd
import matplotlib.pyplot as plt


def plot_population_trends(df: pd.DataFrame, title: str = "Population Trends") -> None:
    plt.figure(figsize=(12, 6))

    plt.plot(df["year"], df["births"], marker="o", label="Births", color="green")
    plt.plot(df["year"], df["deaths"], marker="o", label="Deaths", color="red")
    plt.plot(df["year"], df["natural_growth"], marker="o", label="Natural Growth", color="blue")

    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_bar_natural_growth(df: pd.DataFrame, title: str = "Natural Growth") -> None:
    plt.figure(figsize=(12, 6))
    plt.bar(df["year"], df["natural_growth"], color="skyblue", edgecolor="black")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Natural Growth")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.show()