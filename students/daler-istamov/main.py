from modules.loader import load
from modules.computer import compute
from modules.processor import process
from modules.visualizer import plot_population_trends, plot_bar_natural_growth


def main():
    births_raw = load("data/births.csv")
    deaths_raw = load("data/deaths.csv")

    births_processed = process(births_raw, "births")
    deaths_processed = process(deaths_raw, "deaths")

    computed = compute(births_processed, deaths_processed)

    print(computed)

    plot_population_trends(computed, "Uzbekistan: Population Trends 2010-2024")
    plot_bar_natural_growth(computed, "Uzbekistan: Natural Growth 2010-2024")


if __name__ == "__main__":
    main()