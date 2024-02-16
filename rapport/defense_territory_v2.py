from mplsoccer.pitch import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import API
from matplotlib.colors import LinearSegmentedColormap


def nom_de_famille(name):
    ndf = name[0] + '. '
    n = len(name)
    i = 0
    while name[i] != ' ':
        i += 1
    ndf += name[i + 1:n]
    return (ndf)

def defense_territory(id_match,team,df_events) :

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

    df_events_team = df_events[(df_events.team_id == team_id)]

    events_duel = df_events_team[(df_events_team.type_name == "Duel")]
    events_duel_win = events_duel[(events_duel.outcome_id == 4) | (events_duel.outcome_id == 15) | (events_duel.outcome_id == 16) | (events_duel.outcome_id == 17)]
    events_duel_lost = events_duel[(events_duel.outcome_id) == 1 | (events_duel.outcome_id == 13) | (events_duel.outcome_id == 14)]

    events_interception = df_events_team[(df_events_team.type_name == "Interception")]
    events_interception_win = events_interception[(events_interception.outcome_id == 4) | (events_interception.outcome_id == 15) | (events_interception.outcome_id == 16) | (events_interception.outcome_id == 17)]
    events_interception_lost = events_interception[(events_interception.outcome_id == 1) | (events_interception.outcome_id == 13) | (events_interception.outcome_id == 14)]

    events_clearance = df_events_team[(df_events_team.type_name == "Clearance")]

    events_foul_committed = df_events_team[(df_events_team.type_name == "Foul Committed")]
    if 'foul_committed_offensive' in events_foul_committed :
        events_foul_committed_offensive = events_foul_committed[(events_foul_committed.foul_committed_offensive == True)]
        events_foul_committed = pd.concat([events_foul_committed, events_foul_committed_offensive]).drop_duplicates(keep=False)

    events_block = df_events_team[(df_events_team.type_name == "Block")]
    if 'block_offensive' in events_foul_committed:
        events_block_offensive = events_block[(events_block.block_offensive == True)]
        events_block = pd.concat([events_block, events_block_offensive]).drop_duplicates(keep=False)

    events_50_50 = df_events_team[(df_events_team.type_name == '50-50')]
    events_50_50_win = events_50_50[(events_50_50.outcome_id == 108) | (events_50_50.outcome_id == 147)]
    events_50_50_lost = events_50_50[(events_50_50.outcome_id == 109) | (events_50_50.outcome_id == 148)]

    events_dribbled_past = df_events_team[(df_events_team.type_name == 'Dribbled Past')]

    events_goal = df_events_team[(df_events_team.position_name) == "Goalkeeper"]


    players = np.array(list(df_events_team["player_name"].value_counts().index))
    entered_players = np.array(list(df_events_team["substitution_replacement_name"].value_counts().index))
    goal = np.array(list(events_goal["player_name"].value_counts().index))
    first_team_player = np.setdiff1d(players,entered_players)
    fields_player = np.setdiff1d(players,goal)


    width,height = 0.13,0.6
    pitch_place = [[0,0],[0.2,0],[0.4,0],[0.6,0],[0.8,0],[0,0.33],[0.2,0.33],[0.4,0.33],[0.6,0.33],[0.8,0.33],[0,0.66],[0.2,0.66],[0.4,0.66],[0.6,0.66],[0.8,0.66]]


    with plt.ioff():

        fig,ax0 = plt.subplots()
        plt.rcParams['axes.facecolor'] = "white"
        ax0.set_frame_on(False)
        ax0.set_visible(False)
        i = 0
        for player in fields_player :
            player_won_interception = events_interception_win[(events_interception_win.player_name == player)]
            player_lost_interception = events_interception_lost[(events_interception_lost.player_name == player)]
            player_won_duel = events_duel_win[(events_duel_win.player_name == player)]
            player_lost_duel = events_duel_lost[(events_duel_lost.player_name == player)]
            player_block = events_block[(events_block.player_name == player)]
            player_clearance = events_clearance[(events_clearance.player_name == player)]
            player_foul_committed = events_foul_committed[(events_foul_committed.player_name == player)]
            player_won_50_50 = events_50_50_win[(events_50_50_win.player_name == player)]
            player_lost_50_50 = events_50_50_lost[(events_duel_lost.player_name == player)]
            player_dribbled_past = events_dribbled_past[(events_dribbled_past.player_name == player)]
            player_won_action = pd.concat([player_won_interception,player_won_duel,player_clearance,player_block,player_foul_committed,player_won_50_50],axis = 0)
            player_lost_action = pd.concat([player_lost_interception,player_lost_duel,player_lost_50_50],axis = 0)
            player_action = pd.concat([player_won_action,player_lost_action,player_dribbled_past],axis = 0)       
            ax = fig.add_axes([pitch_place[i][0],pitch_place[i][1],width,height])
            pitch = VerticalPitch(line_color='#000009', line_zorder=2,linewidth=0.3)
            pitch.draw(ax =ax)
            scatter1 = pitch.scatter(player_won_action.x, player_won_action.y,marker='.', ax=ax, facecolor='cornflowerblue')
            scatter2 = pitch.scatter(player_lost_action.x, player_lost_action.y, ax=ax,marker='.', facecolor='red')
            scatter2 = pitch.scatter(player_dribbled_past.x, player_dribbled_past.y, ax=ax,marker='.',facecolor='black')
            if len(player_action) > 2 :
                hull = pitch.convexhull(player_action.x, player_action.y)
                poly = pitch.polygon(hull, ax=ax, facecolor='cornflowerblue', alpha=0.3)
            plt.title(nom_de_famille(player), size=5)
            i += 1
            #plt.legend(frameon = False,loc = 'upper right')
        return(fig)


id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = defense_territory(id_match,team,df_events)
plt.show()

#boucle nombre de match
# id_match = API.n_dernier_match(2,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = defense_territory(id,team,df_events)
#     plt.show()


"""
df_events = API.df_events(id_match)
fig = defense_territory(id_match,"Servette",df_events)
plt.show()

cmap = plt.get_cmap("Oranges")
flamingo_cmap = LinearSegmentedColormap.from_list("Flamingo - 100 colors",['#e3aca7', '#c03a1d'], N=100)
flamingo_cmap.colorbar_extend
len(cmap._segmentdata)
"""

"""
df_events = API.df_events(id_match)
df_matches = API.df_matches
match_info = df_matches[(df_matches.match_id == id_match)]
match_info.reset_index(drop=True, inplace=True)

team1_id = match_info["home_team_id"][0]
team2_id = match_info["away_team_id"][0]
team1_name = match_info["home_team_name"][0]
team2_name = match_info["away_team_name"][0]

team = "Servette"

if team == team1_name:
    team_id = team1_id
else:
    team_id = team2_id

df_events_team = df_events[(df_events.team_id == team_id)]
df_pressure = df_events_team[(df_events_team.type_name == "Pressure")]

player = "Timothé Cognat"

df_pressure_player = df_pressure[(df_pressure.player_name == player)]

df_pressure_player = df_pressure.loc[df_pressure.player_name == player,['x', 'y']]

from matplotlib.colors import LinearSegmentedColormap

flamingo_cmap = LinearSegmentedColormap.from_list("Flamingo - 100 colors",
                                                  ['#e3aca7', '#c03a1d'], N=100)

pitch = VerticalPitch(line_color='#000009', line_zorder=2)
fig, ax = pitch.draw(figsize=(4.4, 6.4))
kde = pitch.kdeplot(df_pressure_player.x, df_pressure_player.y, ax=ax,
                    # shade using 100 levels so it looks smooth
                    shade=True, levels=100,
                    # shade the lowest area so it looks smooth
                    # so even if there are no events it gets some color
                    shade_lowest=True,
                    cut=4,  # extended the cut so it reaches the bottom edge
                    cmap=flamingo_cmap)
"""
