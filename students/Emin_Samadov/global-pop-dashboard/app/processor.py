def get_country_list(df):
    countries = df[["Country Name", "Country Code"]].drop_duplicates()
    countries = countries.sort_values("Country Name")

    return [
        {"name": row["Country Name"], "code": row["Country Code"]}
        for _, row in countries.iterrows()
    ]


def get_country_timeseries(df, country_code, start_year=None, end_year=None):
    sub = df[df["Country Code"] == country_code].copy()

    if start_year:
        sub = sub[sub["Year"] >= start_year]
    if end_year:
        sub = sub[sub["Year"] <= end_year]

    return sub.sort_values("Year")


def compute_stats(ts):
    if ts.empty:
        return {}

    start_row = ts.iloc[0]
    end_row = ts.iloc[-1]

    abs_growth = end_row["Population"] - start_row["Population"]
    rel_growth = (abs_growth / start_row["Population"]) * 100

    max_row = ts.loc[ts["Population"].idxmax()]

    return {
        "start_year": int(start_row["Year"]),
        "end_year": int(end_row["Year"]),
        "start_pop": float(start_row["Population"]),
        "end_pop": float(end_row["Population"]),
        "absolute_growth": float(abs_growth),
        "relative_growth_pct": float(rel_growth),
        "max_year": int(max_row["Year"]),
        "max_population": float(max_row["Population"])
    }
