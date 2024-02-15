# %%
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams
from highlight_text import fig_text
import pandas as pd

from PIL import Image
import urllib
import os


# --- Use this only if you have already downloaded fonts into your


# --- Read and transform the data

df1 = pd.read_csv('/Users/matfeig/Dropbox/SFC/Database/event_match/sfc_fcs_2.csv', index_col = 0)

df2 = df1[df1.event_type_name=='Shot']
df = df2[["team_id","player_id","player_name","minute", "statsbomb_xg","outcome_name","team_name","match_id"]]

df = df.rename(columns = {"team_id": "teamId", "player_id": "playerId","player_name": "PlayerName", "minute": "min","statsbomb_xg": "xG","outcome_name": "eventType","team_name": "teamName"}) 

color = list(df['teamName'])
colors = ['#870E26' if (x == 'Servette') else 'grey' for x in color ]
df['teamColor']= colors

venu = list(df['teamName'])
venue = ['H' if (x == 'Servette') else 'A' for x in venu ]
df['venue']= venue

df['min'] = df['min'].astype(int)
df['xG'] = df['xG'].astype(float)


df = df.drop_duplicates(keep='first')

df = df.replace({
    'eventType': {
        'Saved': 'AttemptSaved'
    }
})

df = df.replace({
    'eventType': {
        'Off T': 'Miss'
    }
})

df = df.replace({
    'eventType': {
        'Wayward': 'Post'
    }
})

df = df.replace({
    'eventType': {
        'Blocked': 'Miss'
    }
})
# ----------------------------------------------------------------
# Function to plot the xG match axes

def plot_axes_xg_by_match(ax, fig, match_id, data=df):
    '''
    This function plots the xG lollipop chart for a given match
    id.
    '''
    df = data.copy()
    match_df = df[df['match_id'] == match_id].reset_index(drop=True)
    match_df.sort_values(by='min', ascending=True).reset_index(drop=True)

    home_conditional = (match_df['venue'] == 'H')
    away_conditional = (match_df['venue'] == 'A')

    # -- Clean up the axes
    ax.set_ylim(-.80,0.85)
    ax.set_xlim(-7,97)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks([])
    ax.xaxis.set_ticks(
        [x for x in range(-2,45,10)] + [x for x in range(52,102,10)],
        labels=[x for x in range(0,91,10)]
    )
    ax.tick_params(labelsize=12)

    plt.rcParams['hatch.linewidth'] = 1.45

    home_color = match_df[home_conditional]['teamColor'].iloc[0]
    for index, shot in enumerate(match_df[home_conditional]['xG']):
        minute = match_df[home_conditional]['min'].iloc[index]
        if minute < 46:
            offset_x = -2
        else:
            offset_x = 2
        ax.plot([minute + offset_x, minute + offset_x], [0, shot], color=home_color)
        if match_df[home_conditional]['eventType'].iloc[index] != 'Goal':
            hatch = ''
        else:
            hatch = '/////////////'
        ax.scatter([minute + offset_x], [shot + .025], marker='o', s=80, hatch=hatch, 
                color="white", zorder=20, lw=1.15, ec=home_color)

    away_color = match_df[away_conditional]['teamColor'].iloc[0]
    for index, shot in enumerate(match_df[away_conditional]['xG']):
        minute = match_df[away_conditional]['min'].iloc[index]
        if minute < 46:
            offset_x = -2
        else:
            offset_x = 2
        ax.plot([minute + offset_x, minute + offset_x], [0, -1*shot], color=away_color)
        if match_df[away_conditional]['eventType'].iloc[index] != 'Goal':
            hatch = ''
        else:
            hatch = '/////////////'
        ax.scatter([minute + offset_x], [-1*shot - .025], marker='o', s=80, hatch=hatch, 
                color="white", zorder=20, lw=1.15, ec=away_color)

    # --- Make it pretty ---
    ax.plot([-5,95], [0,0], color='black', lw=2)
    ax.plot([45,45], [-1.05,1.05], color='white', lw=1, zorder=2)
    ax.fill_between(
        x=[-5,95], y1=[0], y2=[1.05],
        color=home_color, alpha=0.1, zorder=1,
        hatch="......."
    )
    ax.fill_between(
        x=[-5,95], y1=[0], y2=[-1.05],
        color=away_color, alpha=0.1, zorder=1,
        hatch="......."
    )

    # --- Add the logos and legend ---
    home_team_id = match_df[home_conditional]['teamId'].iloc[0]
    away_team_id = match_df[away_conditional]['teamId'].iloc[0]
    home_team_name = match_df[home_conditional]['teamName'].iloc[0]
    away_team_name = match_df[away_conditional]['teamName'].iloc[0]



    # --- Compute goals and xG
    home_xG = match_df[home_conditional]['xG'].sum()
    away_xG = match_df[away_conditional]['xG'].sum()
    home_goals = (match_df[home_conditional]['eventType'] == 'Goal').sum()
    away_goals = (match_df[away_conditional]['eventType'] == 'Goal').sum()

    ax.annotate(
        xy=(0.03, 0.95),
        text=f'{home_team_name} ({home_xG:.1f}) vs. {away_team_name} ({away_xG:.1f}): {home_goals} - {away_goals}',
        xycoords='axes fraction',
        weight='bold',
        size=10
    )

    return ax


# --- The Final Visual

layout_ = '''
    AA
'''

height_ratios = [1]

f = plt.figure(figsize=(16,9))
axs = f.subplot_mosaic(layout_, gridspec_kw={ 'height_ratios':height_ratios,'hspace': 0.25 })
#axs = f.plot()

counter = 0
df = df.sort_values(by='match_id').reset_index(drop=True)
matches = list(df['match_id'].unique())
for k, ax in axs.items():
    match_id = matches[counter]
    plot_axes_xg_by_match(ax, f, match_id=match_id, data=df)
    counter += 1


fig_text(
    x = 0.5, y = .89, 
    s = "Tirs au cours du Match",
    #highlight_textprops=[{"style":"italic"}],
    va = "bottom", ha = "center",
    fontsize = 16, color = "black", weight = "bold"
)
# fig_text(
# 	x = 0.12, y = .92, 
#     s = " xG lollipop timeline | Each circle is a shot | <Dashed circles represent goals> | Viz by @sonofacorner.",
#     highlight_textprops=[{"weight": "bold", "color": "black"}],
# 	va = "bottom", ha = "left",
# 	fontsize = 12, color = "#4E616C", font = "Karla"
# )

# plt.savefig(
# 	"figures/08082022_ligue1_round1.png",
# 	dpi = 600,
# 	facecolor = "#EFE9E6",
# 	bbox_inches="tight",
#     edgecolor="none",
# 	transparent = False
# )

# plt.savefig(
# 	"figures/08082022_ligue1_round1_tr.png",
# 	dpi = 600,
# 	facecolor = "none",
# 	bbox_inches="tight",
#     edgecolor="none",
# 	transparent = True
#)






