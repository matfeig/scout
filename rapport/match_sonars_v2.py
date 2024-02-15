from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.projections import get_projection_class
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch, VerticalPitch
import pandas as pd
import requests
from mplsoccer.statsbomb import EVENT_SLUG, read_event, read_competition, read_match
import numpy as np
import API

""""
id_match = API.n_dernier_match(1,["Servette"])[0]
"""

def nom_de_famille(name):
    ndf = name[0] + '. '
    n = len(name)
    i = 0
    while name[i] != ' ':
        i += 1
    ndf += name[i + 1:n]
    return (ndf)


def match_sonars(id_match,team,df_events) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    if team == team1_name:
        team_id = team1_id
    else:
        team_id = team2_id

    df = df_events[(df_events.team_id == team_id)]
    df.reset_index(drop=True, inplace=True)

    df['y'] = df['y'] * (-1)
    df['end_y'] = df['end_y'] * (-1)

    cmap = plt.cm.get_cmap('cividis')
    multiplier = 2 * np.pi / 24

    plt.rcParams["font.family"] = "Basier Circle"
    plt.rcParams['font.size'] = 7
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams['text.color'] = 'black'

    def get_angle(val):
        x1, y1, x2, y2 = val

        dx = x2 - x1
        dy = y2 - y1
        result = np.arctan2(dy, dx)
        return result if result >= 0 else result + 2 * np.pi

    df['length'] = np.sqrt(
        np.square(df["x"] - df["end_x"]) + np.square(df["y"] - df["end_y"]))
    df['angle'] = df[['x', 'y', 'end_x', 'end_y']].apply(get_angle, axis=1)
    df['angle_bin'] = pd.cut(df['angle'], bins=np.linspace(0, 2 * np.pi, 24), labels=False)

    pdf = df.groupby(['player_id', 'angle_bin']).agg(count=('angle_bin', 'count'),
                                                     avg_length=('length', 'mean')).reset_index()


    players_id = np.array(list(df["player_id"].value_counts().index))
    entered_players_id = np.array(list(df["substitution_replacement_id"].value_counts().index))
    first_team_players_id = np.setdiff1d(players_id,entered_players_id)

    player_loc_dict = {'1' : [15,40], '2' : [30,70],'3' : [30,55],'4' : [30,40],
                       '5' : [30,25],'6' : [30,10],'7' : [45,70],'8' : [45,10],
                       '9' : [45,55],'10' : [45,40],'11' : [45,25],'12' : [60,70],
                       '13' : [60,55],'14' : [60,40],'15' : [60,25],'16' : [60,10],
                       '17' : [75,70],'18' : [75,55],'19' : [75,40],'20' : [75,25],
                       '21' : [75,10],'22' : [105,55],'23' : [105,40],'24' : [105,25],
                       '25' : [90,40]}

    def player_position_and_name(id) :
        i = 0
        while not(df["player_id"][i] > 0):
            i += 1
        while df["player_id"][i] != id :
            i += 1
        position_id = int(df["position_id"][i])
        [x,y] = player_loc_dict[str(position_id)]
        return(df["player_name"][i],x,y)

    def plot_inset(width, ax, pdf, x, y):
        ax_sub = inset_axes(ax, width=width, height=width, loc=10,
                            bbox_to_anchor=(x, y), bbox_transform=ax.transData,
                            borderpad=0.0, axes_class=get_projection_class("polar"))

        colors = cmap(pdf['avg_length'] / pdf['avg_length'].max())
        bars = ax_sub.bar(pdf['angle_bin'] * multiplier, pdf['count'], width=0.25, bottom=0,
                          alpha=0.9, color=colors, ec='none')

        ax_sub.set_xticklabels([])
        ax_sub.set_yticks([])
        ax_sub.grid(False)
        ax_sub.spines['polar'].set_visible(False)
        ax_sub.patch.set_alpha(0)
        return ax

    with plt.ioff():

        pitch = Pitch(figsize=(24, 12))  # example plotting a sch
        fig,ax = pitch.draw(figsize=(12,9))
        plt.rcParams['axes.facecolor'] = "#C1CDCD"

        for player_id in first_team_players_id:
            (player_name,x,y) = player_position_and_name(player_id)
            player_df = pdf.query("player_id == @player_id")
            plot_inset(2, ax, player_df, x, y)
            ax.text(x - 14, y, nom_de_famille(player_name), size=8)

        # plt.tight_layout(True)

        return(fig)

id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = match_sonars(id_match,team,df_events)
plt.show()

#boucle nombre de match 
# id_match = API.n_dernier_match(3,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = match_sonars(id,team,df_events)
#     plt.show()



"""
player_nb_events = {}
player_name = {}
for player_id in first_team_players_id :
    player_loc_dict[player_id] = (0,0)
    player_nb_events[player_id] = 0
for ind in df_passes.index :
    id = df_passes["player_id"][ind]
    if id in player_loc_dict.keys() :
        (x,y) = player_loc_dict[id]
        if df_passes["x"][ind] > 0 :
            x += df_passes["x"][ind]
        if df_passes["y"][ind] > 0:
            y += df_passes["y"][ind]
        player_loc_dict[id] = (x,y)
        player_nb_events[id] += 1
        player_name[id] = df_passes['player_name'][ind]
for key in player_loc_dict.keys() :
    (x, y) = player_loc_dict[key]
    x = x/player_nb_events[key]
    y = y/player_nb_events[key]
    player_loc_dict[key] = (x,y)
"""