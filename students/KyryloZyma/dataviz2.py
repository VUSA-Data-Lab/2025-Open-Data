import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
# import webbrowser

# matplotlib randomly decided to not build for GUI using pywebbrowser lib,
# so I had to change a rendering backend
import matplotlib
matplotlib.use("Qt5Agg")

import plotly.express as px


df = pd.read_csv("data2.csv")
df_mun = pd.read_csv("municipality_population.csv")

df["dateTime"] = pd.to_datetime(df["dateTime"])
df["registrationDate"] = pd.to_datetime(df["registrationDate"])
df["lastEditTime"] = pd.to_datetime(df["lastEditTime"])
df["category"] = df["category"].str.strip(' "')
df["category1"] = df["category1"].str.strip(' "')
df["category2"] = df["category2"].str.strip(' "')

MAX_DATE = "1950-01-01"
df.drop(df.query(f"dateTime < @MAX_DATE").index, inplace=True)
# print(df['municipality'].str.split(n=1).str[0])


# PREP
df["municipality"] = df["municipality"].str.split(n=1).str[0].str.capitalize()
df_mun["municipality"] = (
    df_mun["municipality"].str.split(n=1).str[0].str.capitalize()
)
df_mun = (
    df_mun.groupby("municipality")["population"].agg(["sum"]).reset_index()
)
df_mun = df_mun.rename(columns={"sum": "population"})
df_plot1 = (
    df.groupby("municipality")["numberOfParticipants"]
    .agg(["sum", "count"])
    .reset_index()
)

# excluding outer join on keys
# print(pd.concat([df_plot1['municipality'],
    # df_mun['municipality']],
    # ignore_index=True).drop_duplicates(keep=False))

# Checking if municipality has data on collisions and has data on population at the same time
CK_DF = df_plot1.merge(df_mun, how="inner", on="municipality")
common_keys = CK_DF["municipality"]
# print(common_keys)



# GLOBAL STATS
# Incidents per municipality
df = df.loc[df["municipality"].isin(common_keys)].reset_index(drop=True)
df_mun = df_mun.loc[df_mun["municipality"].isin(common_keys)].reset_index(
    drop=True
)
df_plot1 = df_plot1.loc[
    df_plot1["municipality"].isin(common_keys)
].reset_index(drop=True)

ax = df_plot1.plot(
    x="municipality",
    y=["sum", "count"],
    kind="bar",
    style=".-",
    rot=90,
    width=1,
)
ax.set_ylabel("Total number of incidents starting from 2010")
# population
ax = df_mun.plot(
    ax=ax,
    secondary_y=True,
    x="municipality",
    y=["population"],
    # kind="scatter",
    kind="line",
    # style=".-",
    style="r.",
    rot=90,
)
ax.set_ylabel("Population at the state of 2025")
plt.show()
plt.close()

# Incident type
sun1_df = df.loc[df["category"].str.len() > 0]
fig = px.sunburst(
    sun1_df,
    path=["category", "category1", "category2"],
    title="Reported incident category distribution:",
)
fig.show()
# fig.write_image("fig1.png")



# USER_INPUT
print("\n\n\n\n\n")
print(df_mun)
municipality_number = int(input("Choose a municipality to analyze from the list above:"))
user_municipality = common_keys.to_list()[municipality_number]
print(user_municipality)



# REQUESTED STATS
# Incidents per municipality
df_plot2 = df.loc[df["municipality"] == user_municipality]
df_2 = (
    df_plot2.set_index("dateTime")["numberOfParticipants"]
    # .resample("D")
    .resample("W")
    .agg(["sum", "count"])
)
# df_=df_1.merge(df_2,suffixes=('_D','_M'))

tmp_df = df_2.rolling(4, center=True).mean()
ax = tmp_df.plot(
    # x='dateTime'
    y=["sum", "count"],
    grid=True,
    kind="area",
    stacked=False,
    # ,rot=90
    title="Incidents per week at "
    + user_municipality
    + " municipality, data smoothed out across 4-week period",
)
ax.set_xlabel("Week #")
ax.set_ylabel("Incidents")
# df_= df_.reset_index()
# df_.rolling(30, center=True).mean(numeric_only=True).plot(
    # x="dateTime",
    # y=["sum", "count"],
    # kind="line",
    # style=".-", rot=90
# )

plt.show()
plt.close()
# print(df_plot2)



# Incident type
sun2_df = df_plot2.loc[df_plot2["category"].str.len() > 0]
fig = px.sunburst(
    sun2_df,
    path=["category", "category1", "category2"],
    title="Reported incident category distribution at "
    + user_municipality
    + " municipality:",
)
fig.show()

# exit()
#
# Incidents per year
# # plot sum(numberOfParticipants) and count() over municipality
# # reindex and count occurences per "D"(1 day) period
# df_ = df.set_index('dateTime')['registrationCode'].resample('D').count()
# df_.plot(alpha=.5)
# # df_.rolling(30, center=True).mean().plot(ax=ax, grid=True, ylabel="Incidents")
# df_.rolling(30, center=True).mean().plot(grid=True, ylabel="Incidents")
# # plt.set_ylabel("Incidents")
# plt.show(); plt.close()
