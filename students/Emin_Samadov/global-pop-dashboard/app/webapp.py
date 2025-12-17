from flask import Blueprint, render_template, request
from .data_loader import load_clean_data
from .visualizer import generate_population_chart
from pathlib import Path

webapp = Blueprint("webapp", __name__)

EXPORT_DIR = Path("static/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

@webapp.route("/")
def index():
    df = load_clean_data()

    countries = df[["Country Name", "Country Code"]].drop_duplicates()
    countries = countries.sort_values("Country Name")

    return render_template(
        "index.html",
        countries=[
            {"name": r["Country Name"], "code": r["Country Code"]}
            for _, r in countries.iterrows()
        ],
        default_code="LTU"
    )


@webapp.route("/api/country-data")
def api_country_data():
    code = request.args.get("code", "LTU")
    start = request.args.get("start")
    end = request.args.get("end")

    df = load_clean_data()

    country_data = df[df["Country Code"] == code].copy()
    country_name = country_data["Country Name"].iloc[0]

    if start:
        country_data = country_data[country_data["Year"] >= int(start)]
    if end:
        country_data = country_data[country_data["Year"] <= int(end)]

    years = country_data["Year"].tolist()
    population = country_data["Population"].tolist()

    #  Year-to-year table 
    yearly_table = []
    for i in range(1, len(years)):
        change = population[i] - population[i - 1]
        pct = (change / population[i - 1]) * 100 if population[i - 1] > 0 else 0

        yearly_table.append({
            "year": years[i],
            "population": population[i],
            "change": change,
            "pct": pct
        })

    #  World population share 
    world = df[df["Country Code"] == "WLD"].set_index("Year")["Population"]

    world_share = []
    for y, p in zip(years, population):
        if y in world.index:
            share = (p / world[y]) * 100
        else:
            share = None
        world_share.append(share)

    # Save chart
    save_path = EXPORT_DIR / f"{code}_{start or 'all'}_{end or 'all'}.png"
    generate_population_chart(
        {"years": years, "population": population},
        country_name,
        str(save_path)
    )

    stats = {
        "start_year": years[0],
        "end_year": years[-1],
        "start_pop": population[0],
        "end_pop": population[-1],
        "absolute_growth": population[-1] - population[0],
        "relative_growth_pct": ((population[-1] - population[0]) / population[0]) * 100,
        "max_population": max(population),
        "max_year": years[population.index(max(population))]
    }

    return {
        "country_code": code,
        "country_name": country_name,
        "years": years,
        "population": population,
        "chart_url": f"/static/exports/{save_path.name}",
        "stats": stats,
        "yearly_table": yearly_table,
        "world_share": world_share,
    }
