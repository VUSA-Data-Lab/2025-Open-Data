from pathlib import Path

# Use non-GUI backend for web usage
import matplotlib
matplotlib.use("Agg")  # IMPORTANT: no Tkinter windows
import matplotlib.pyplot as plt


def generate_population_chart(ts, country_name, save_path, dark=True):
    """
    Generate and save a PNG chart of population over time.
    ts must be a dict: {"years": [...], "population": [...]}
    """

    #  NEW: Check dict instead of ts.empty 
    if not ts or not ts.get("years"):
        return

    years = ts["years"]
    population = ts["population"]

    # Colors and style
    if dark:
        plt.style.use("dark_background")
        color = "#00ffc8"
        grid = "#333"
    else:
        plt.style.use("default")
        color = "blue"
        grid = "#ccc"

    plt.figure(figsize=(10, 4))
    plt.plot(years, population, color=color, linewidth=2)
    plt.fill_between(years, population, alpha=0.15, color=color)

    plt.title(f"Population of {country_name}")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.grid(True, linestyle="--", color=grid)

    Path(save_path).parent.mkdir(exist_ok=True)
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()


def plot_country_timeseries_cli(ts, country_name, save_path=None):
    """
    Optional CLI function. ts must be dict-based.
    """

    if not ts or not ts.get("years"):
        print("No data to plot.")
        return

    if save_path:
        generate_population_chart(ts, country_name, save_path, dark=False)

    # CLI display removed to avoid Tk errors
