fe# %%
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
from matplotlib import rcParams
from highlight_text import ax_text, fig_text
import pandas as pd

from PIL import Image
import urllib
import os

# --- Use this only if you have already downloaded fonts into your
# --- local directory.

#https://www.sonofacorner.com/the-premier-leagues-naughty-boys/

# --- Reading the data

df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/player_season/cluster/df.csv")


# -- Highlighted players.

players = [
  3184,
  2955,
  23779,
  24899,
  28961,
  29225,
  46208,
  48493,
]

#df['player_name'] = df['plauyer_name'].replace(['Danilo'],'J. Danilo')

df_main = df[~df["player_id"].isin(players)].reset_index(drop = True)
df_highlight = df[df["player_id"].isin(players)].reset_index(drop = True)

# %%

# -- Plot the chart

fig = plt.figure(figsize = (16,9), dpi = 300)
ax = plt.subplot(facecolor = "white")
ax.set_ylim([0, 2.5])
ax.set_xlim([0, 2.5])

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.scatter(
    df_main["player_season_np_xg_90"], 
    df_main["player_season_goals_90"], 
    s = 40, 
    alpha = 0.75, 
    color = "#264653",
    zorder = 3
)

ax.scatter(
    df_highlight["player_season_np_xg_90"], 
    df_highlight["player_season_goals_90"], 
    s = 40, 
    alpha = 0.95, 
    color = "#F64740",
    zorder = 3,
    ec = "#000000",
)

ax.plot(
    [df["player_season_np_xg_90"].median(), df["player_season_np_xg_90"].median()],
    [ax.get_ylim()[0], ax.get_ylim()[1]], 
    ls = "--",
    color = "grey",
    zorder = 0.5
)

ax.plot(
    [ax.get_xlim()[0], ax.get_xlim()[1]],
    [df["player_season_goals_90"].median(), df["player_season_goals_90"].median()], 
    ls = "--",
    color = "grey",
    zorder = 0.5
)

ax.grid(True, ls = ":", color = "lightgray")

for index, name in enumerate(df_highlight["player_name"]):
    X = df_highlight["player_season_np_xg_90"].iloc[index]
    Y = df_highlight["player_season_goals_90"].iloc[index]
    if name in ["Enzo Crivelli","Ronny Rodelin","Chris Vianney Bedia","Boubacar Fofana","Miroslav Stevanović","Derek Kutesa","Patrick Pflücke",
                "Alexis Antunes"]:
        y_pos = 9
    else:
        y_pos = -9
    if name in ["Scott McTominay"]:
        x_pos = 20
    else:
        x_pos = 0
    text_ = ax.annotate(
        xy = (X, Y),
        text = name.split(" ")[1],
        ha = "center",
        va = "center",
        xytext = (x_pos, y_pos),
        textcoords = "offset points",
        weight = "bold"
    )

    text_.set_path_effects(
                [path_effects.Stroke(linewidth=5, foreground="white"), 
                path_effects.Normal()]
            )

ax.set_xlabel("player_season_np_xg_90")
ax.set_ylabel("player_season_goals_90")


fig_text(
    x = 0.5, y = 0.9, 
    s = "Scoring Contribution",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 30, color = "black", font = "Karla", weight = "bold"
)

# fig_text(
#  	x = 0.87, y = .94, 
#     s = "Fouls per 90 & cards received per foul committed | Season 2021/2022\nPlayers with more than 1,000 minutes and at least 16 fouls are considered.\nViz by @sonofacorner.",
#  	va = "bottom", ha = "right",
#  	fontsize = 7, color = "#4E616C", font = "Karla"
# )

