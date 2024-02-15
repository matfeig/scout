
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
from matplotlib import rcParams
from highlight_text import ax_text, fig_text
import pandas as pd
import plotly.graph_objects as go

from PIL import Image
import urllib
import os

# --- Use this only if you have already downloaded fonts into your
# --- local directory.

#https://www.sonofacorner.com/the-premier-leagues-naughty-boys/

#%%
# --- Reading the data

df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/recrutement/df_api_stats_03-2023.csv")

df= df.loc[(df.primary_position == "Centre Forward")|(df.primary_position == "Centre Attacking Midfielder")|(df.primary_position == "Right Centre Midfielder")|
           (df.primary_position == "Left Wing")|(df.primary_position == "Right Wing")|(df.primary_position == "Left Centre Midfielder")]

df= df.loc[(df.primary_position == "Centre Forward")|(df.primary_position == "Centre Attacking Midfielder")|(df.primary_position == "Right Centre Midfielder")|
           (df.primary_position == "Left Wing")|(df.primary_position == "Right Wing")|(df.primary_position == "Left Centre Midfielder")|
           (df.primary_position == "Centre Defensive Midfielder")|(df.primary_position == "Left Defensive Midfielder")|(df.primary_position == "Left Back")|(df.primary_position == "Right Back")
           ]


# Centre Forward
# Right Wing
# Left Wing
# Centre Attacking Midfielder

# Left Defensive Midfielder
# Centre Defensive Midfielder
# Right Centre Midfielder
# Left Centre Midfielder

# Right Back
# Left Back
# Left Centre Back
# Right Centre Back

df = df.loc[(df.season_name == "2022/2023")]

##Choisir les variables 
df=df.loc[(df.player_season_minutes>=250)]

# -- Highlighted players.

players = [
  3184,
  3622,
  2955,
  7502,
  7314,
  7597,
  23325,
  16027,
  20302,
  23779,
  24899,
  28949,
  28961,
  28964,
  28965,
  28967,
  29225,
  29460,
  41654,
  40138,
  46208,
  48493,
  49033,
  50437,
  67308,
  196785,
  130192,
  219634,
  219635,
  231352,
  256059,
  286843,
  388167
  ]

#df['Name'] = df['Name'].replace(['Danilo'],'J. Danilo')

df_main = df[~df["player_id"].isin(players)].reset_index(drop = True)
df_highlight = df[df["player_id"].isin(players)].reset_index(drop = True)


#%%
# -- Plot the chart

fig = plt.figure(figsize = (16,9), dpi = 300)
ax = plt.subplot(facecolor = "white")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.scatter(
    df_main["player_season_np_xg_90"], 
    df_main["player_season_npga_90"], 
    s = 40, 
    alpha = 0.75, 
    color = "lightgrey",
    zorder = 3
)

ax.scatter(
    df_highlight["player_season_np_xg_90"], 
    df_highlight["player_season_npga_90"], 
    s = 40, 
    alpha = 0.95, 
    color = "#870E26",
    zorder = 3,
    #ec = "#000000",
)

ax.plot(
    [df["player_season_np_xg_90"].median(), df["player_season_np_xg_90"].median()],
    [ax.get_ylim()[0], ax.get_ylim()[1]], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.plot(
    [ax.get_xlim()[0], ax.get_xlim()[1]],
    [df["player_season_npga_90"].median(), df["player_season_npga_90"].median()], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.grid(True, ls = ":", color = "lightgray")

x =[0,1]
y = [0,1]
ax.plot(x, y, color='grey', linewidth=1)

for index, name in enumerate(df_highlight["player_name"]):
    X = df_highlight["player_season_np_xg_90"].iloc[index]
    Y = df_highlight["player_season_npga_90"].iloc[index]
    if name in ["Ronny Rodelin"]:
        y_pos = -20
    else:
        y_pos = -9
    if name in ["Ronny Rodelin"]:
        x_pos = 25
    else:
        x_pos = -5
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
                [path_effects.Stroke(linewidth=2, foreground="white"), 
                path_effects.Normal()]
            )

ax.set_xlabel("Expected Goals",weight = "bold")
ax.set_ylabel("Goals (NP)",weight = "bold")

fig_text(
    x = 0.36, y = 0.90, 
    s = "Expected Goals & Buts",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 20, color = "black", font = "Karla", weight = "bold"
)
fig_text(
    x = 0.8, y = 0.75, 
    s = "Sur-perf",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 12, color = "black", font = "Karla"
)

fig_text(
    x = 0.86, y = 0.67, 
    s = "Sous-perf",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 12, color = "black", font = "Karla"
)



#%%
# -- Plot the chart ###

fig = plt.figure(figsize = (16,9), dpi = 300)
ax = plt.subplot(facecolor = "white")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.scatter(
    df_main["player_season_deep_progressions_90"], 
    df_main["player_season_xa_90"], 
    s = 40, 
    alpha = 0.75, 
    color = "lightgrey",
    zorder = 3
)

ax.scatter(
    df_highlight["player_season_deep_progressions_90"], 
    df_highlight["player_season_xa_90"], 
    s = 40, 
    alpha = 0.95, 
    color = "#870E26",
    zorder = 3,
    #ec = "#000000",
)

ax.plot(
    [df["player_season_deep_progressions_90"].median(), df["player_season_deep_progressions_90"].median()],
    [ax.get_ylim()[0], ax.get_ylim()[1]], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.plot(
    [ax.get_xlim()[0], ax.get_xlim()[1]],
    [df["player_season_xa_90"].median(), df["player_season_xa_90"].median()], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.grid(True, ls = ":", color = "lightgray")


for index, name in enumerate(df_highlight["player_name"]):
    X = df_highlight["player_season_deep_progressions_90"].iloc[index]
    Y = df_highlight["player_season_xa_90"].iloc[index]
    if name in ["Ronny Rodelin"]:
        y_pos = -20
    else:
        y_pos = -9
    if name in ["Ronny Rodelin"]:
        x_pos = 25
    else:
        x_pos = -5
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
                [path_effects.Stroke(linewidth=2, foreground="white"), 
                path_effects.Normal()]
            )

ax.set_xlabel("Deep Progressions",weight = "bold")
ax.set_ylabel("Expected Assists",weight = "bold")

fig_text(
    x = 0.45, y = 0.90, 
    s = "Deep Progressions & Expected Assits",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 20, color = "black", font = "Karla", weight = "bold"
)



#%%

fig = plt.figure(figsize = (16,9), dpi = 300)
ax = plt.subplot(facecolor = "white")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.scatter(
    df_main["player_season_obv_shot_90"], 
    df_main["player_season_np_psxg_90"], 
    s = 40, 
    alpha = 0.75, 
    color = "lightgrey",
    zorder = 3
)

ax.scatter(
    df_highlight["player_season_obv_shot_90"], 
    df_highlight["player_season_np_psxg_90"], 
    s = 40, 
    alpha = 0.95, 
    color = "#870E26",
    zorder = 3,
    #ec = "#000000",
)

ax.plot(
    [df["player_season_obv_shot_90"].median(), df["player_season_obv_shot_90"].median()],
    [ax.get_ylim()[0], ax.get_ylim()[1]], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.plot(
    [ax.get_xlim()[0], ax.get_xlim()[1]],
    [df["player_season_np_psxg_90"].median(), df["player_season_np_psxg_90"].median()], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.grid(True, ls = ":", color = "lightgray")


for index, name in enumerate(df_highlight["player_name"]):
    X = df_highlight["player_season_obv_shot_90"].iloc[index]
    Y = df_highlight["player_season_np_psxg_90"].iloc[index]
    if name in ["Ronny Rodelin"]:
        y_pos = -20
    else:
        y_pos = -9
    if name in ["Ronny Rodelin"]:
        x_pos = 25
    else:
        x_pos = -5
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
                [path_effects.Stroke(linewidth=2, foreground="white"), 
                path_effects.Normal()]
            )

ax.set_xlabel("OBV shot",weight = "bold")
ax.set_ylabel("Post-Shot xG",weight = "bold")

fig_text(
    x = 0.25, y = 0.90, 
    s = "Qualité du tir",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 20, color = "black", font = "Karla", weight = "bold"
)


#%%

fig = plt.figure(figsize = (16,9), dpi = 300)
ax = plt.subplot(facecolor = "white")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.scatter(
    df_main["player_season_obv_dribble_carry_90"], 
    df_main["player_season_obv_pass_90"], 
    s = 40, 
    alpha = 0.75, 
    color = "lightgrey",
    zorder = 3
)

ax.scatter(
    df_highlight["player_season_obv_dribble_carry_90"], 
    df_highlight["player_season_obv_pass_90"], 
    s = 40, 
    alpha = 0.95, 
    color = "#870E26",
    zorder = 3,
    #ec = "#000000",
)

ax.plot(
    [df["player_season_obv_dribble_carry_90"].median(), df["player_season_obv_dribble_carry_90"].median()],
    [ax.get_ylim()[0], ax.get_ylim()[1]], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.plot(
    [ax.get_xlim()[0], ax.get_xlim()[1]],
    [df["player_season_obv_pass_90"].median(), df["player_season_obv_pass_90"].median()], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.grid(True, ls = ":", color = "lightgray")


for index, name in enumerate(df_highlight["player_name"]):
    X = df_highlight["player_season_obv_dribble_carry_90"].iloc[index]
    Y = df_highlight["player_season_obv_pass_90"].iloc[index]
    if name in ["Ronn"]:
        y_pos = -20
    else:
        y_pos = -9
    if name in ["Ronn"]:
        x_pos = 25
    else:
        x_pos = -5
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
                [path_effects.Stroke(linewidth=2, foreground="white"), 
                path_effects.Normal()]
            )

ax.set_xlabel("dribble_carry",weight = "bold")
ax.set_ylabel("Pass",weight = "bold")

fig_text(
    x = 0.2, y = 0.90, 
    s = "Menace",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 20, color = "black", font = "Karla", weight = "bold"
)

#%%
fig = plt.figure(figsize = (16,9), dpi = 300)
ax = plt.subplot(facecolor = "white")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.scatter(
    df_main["player_season_shot_touch_ratio"], 
    df_main["player_season_deep_progressions_90"], 
    s = 40, 
    alpha = 0.75, 
    color = "lightgrey",
    zorder = 3
)

ax.scatter(
    df_highlight["player_season_shot_touch_ratio"], 
    df_highlight["player_season_deep_progressions_90"], 
    s = 40, 
    alpha = 0.95, 
    color = "#870E26",
    zorder = 3,
    #ec = "#000000",
)

ax.plot(
    [df["player_season_shot_touch_ratio"].median(), df["player_season_shot_touch_ratio"].median()],
    [ax.get_ylim()[0], ax.get_ylim()[1]], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.plot(
    [ax.get_xlim()[0], ax.get_xlim()[1]],
    [df["player_season_deep_progressions_90"].median(), df["player_season_deep_progressions_90"].median()], 
    ls = "--",
    linewidth =1,
    color = "grey",
    zorder = 0.5
)

ax.grid(True, ls = ":", color = "lightgray")


for index, name in enumerate(df_highlight["player_name"]):
    X = df_highlight["player_season_shot_touch_ratio"].iloc[index]
    Y = df_highlight["player_season_deep_progressions_90"].iloc[index]
    if name in ["Ronn"]:
        y_pos = -20
    else:
        y_pos = -9
    if name in ["Ronn"]:
        x_pos = 25
    else:
        x_pos = -5
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
                [path_effects.Stroke(linewidth=2, foreground="white"), 
                path_effects.Normal()]
            )

ax.set_xlabel("Shot_touch_ratio",weight = "bold")
ax.set_ylabel("Deep_progressions_90",weight = "bold")

fig_text(
    x = 0.35, y = 0.90, 
    s = "Hauteur sur le terrain",
    #highlight_textprops=[{"color":"#F64740", "style":"italic"}],
    va = "bottom", ha = "right",
    fontsize = 20, color = "black", font = "Karla", weight = "bold"
)



#%%

#### Find Player ####

def set_text_position(name):
    if name in ['Rodelin', 'Fofana','Kutesa','Pflücke','Antunes']:
        return 'top center'
    else:
        return 'bottom center'


fig = go.Figure()
fig.add_trace(
    go.Scatter(x=df['player_season_np_xg_90'],y=df['player_season_npga_90'],mode='markers',text=df['player_name'],
               line=dict(width=2,color='lightgray'))
    )

fig.add_trace(
    go.Scatter(x=df_highlight['player_season_np_xg_90'],y=df_highlight['player_season_npga_90'],mode='markers+text',text=df_highlight['player_name'].apply(lambda x: x.split(' ')[-1]),
               line=dict(width=2,color='darkred'),textposition = list(map(set_text_position, df_highlight['player_name'].apply(lambda x: x.split(' ')[-1]))))
    )
higher_than_df = df_main[df_main["player_season_np_xg_90"]>0.6].copy()

fig.add_trace(
    go.Scatter(x=higher_than_df['player_season_np_xg_90'],y=higher_than_df['player_season_npga_90'],mode='markers+text',text=higher_than_df['player_name'],
               line=dict(width=2,color='green'),textposition = 'top center',
               
               textfont=dict(
                family="Arial",
                size=12,
                color="darkblue")
              )
    )


fig.add_trace(go.Scatter(
    x=[0, max(df.player_season_np_xg_90)],
    y=[0, max(df.player_season_npga_90)],mode='lines',line=dict(width=2,
                                        color='DarkSlateGrey'),opacity=0.5)
)

fig.add_trace(go.Scatter(x=[df['player_season_np_xg_90'].median(),df['player_season_np_xg_90'].median()],
                        y=[0,max(df.player_season_npga_90)],line=dict(color='gray', width=4,
                              dash='dash')))

fig.add_trace(go.Scatter(x=[0,max(df['player_season_np_xg_90'])],
                        y=[df['player_season_npga_90'].median(),df['player_season_npga_90'].median()],
                        line=dict(color='gray', width=4,dash='dash')))

fig.update_layout()
fig.update_layout(
    width= 1400, height=700,
    title="Plot Title",
    xaxis_title="Expected goals",
    yaxis_title="Goals (NP)",
    
)
fig.show()
fig.write_html('xgb_vs_npga.html')
