import numpy as np
import API
import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer.pitch import Pitch, VerticalPitch
from matplotlib.colors import LinearSegmentedColormap


def nom_de_famille(name):
    ndf = name[0] + '.'
    n = len(name)
    i = 0
    while name[i] != ' ':
        i += 1
    ndf += name[i + 1:n]
    return (ndf)

def pass_and_ball_receipt(id_match,team,df_events) :

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

    events_pass = df_events_team[(df_events_team.type_name == "Carry")]
    events_incomplete_pass = events_pass[(events_pass.outcome_id > 0)]
    events_complete_pass = pd.concat([events_pass, events_incomplete_pass]).drop_duplicates(keep=False)
    unwanted_pass = events_complete_pass[(events_complete_pass.sub_type_name == "Corner") | (events_complete_pass.sub_type_name == "Free Kick") | (events_complete_pass.sub_type_name == "Kick Off") | (events_complete_pass.sub_type_name == "Throw-in")]
    events_complete_pass = pd.concat([events_complete_pass, unwanted_pass]).drop_duplicates(keep=False)
    events_complete_pass.reset_index(drop=True, inplace=True)
    events_ball_receipt = df_events_team[(df_events_team.type_name == "Ball Receipt")]
    events_goal = df_events_team[(df_events_team.position_name) == "Goalkeeper"]

    box_passs = events_complete_pass[(events_complete_pass["end_x"] > 102) & (events_complete_pass["end_y"] < 62) & (events_complete_pass["end_y"] > 18)]
    
    events_progressive_pass = pd.DataFrame()
    for ind in events_complete_pass.index :
        d1 = np.sqrt((120-events_complete_pass["x"][ind])**2 + (40-events_complete_pass["y"][ind]) ** 2)
        d2 = np.sqrt((120-events_complete_pass["end_x"][ind])**2 + (40-events_complete_pass["end_y"][ind]) ** 2)
        if 0 < d2/d1 < 0.75 :
            events_progressive_pass = pd.concat([events_progressive_pass,events_complete_pass.iloc[ind:(ind+1),:]])

    events_non_progressive_pass = pd.concat([events_complete_pass, events_progressive_pass]).drop_duplicates(keep=False)

  
    players = np.array(list(df_events_team["player_name"].value_counts().index))
    entered_players = np.array(list(df_events_team["substitution_replacement_name"].value_counts().index))
    goal = np.array(list(events_goal["player_name"].value_counts().index))
    first_team_player = np.setdiff1d(players,entered_players)
    fields_player = np.setdiff1d(first_team_player,goal)

    width,height = 0.2,0.45
    pitch_place = [[0,0],[0.2,0],[0.4,0],[0.6,0],[0.8,0],[0,0.5],[0.2,0.5],[0.4,0.5],[0.6,0.5],[0.8,0.5]]


    with plt.ioff():
      
        fig, ax0 = plt.subplots()
        plt.rcParams['axes.facecolor'] = "white"
        ax0.set_frame_on(False)
        ax0.set_visible(False)
        i = 0
        grey_cmap = LinearSegmentedColormap.from_list("Greys",['#FFFFFF', '#666666'], N=100)
        for player in fields_player :
            x_win = 0
            player_pass = events_complete_pass[(events_complete_pass.player_name == player)]
            player_progressive_pass = events_progressive_pass[(events_progressive_pass.player_name == player)]
            player_box_pass = box_passs[(box_passs.player_name == player)]
            player_incomplete = events_incomplete_pass[(events_incomplete_pass.player_name == player)]
            for ind in player_pass.index :
                x_win += (player_pass["end_x"][ind] - player_pass["x"][ind])*(105/120)
            for ind in player_progressive_pass.index :
                x_win += (player_progressive_pass["end_x"][ind] - player_progressive_pass["x"][ind])*(105/120)
            x_win = round(x_win,2)
            for ind in player_box_pass.index :
                x_win += (player_box_pass["end_x"][ind] - player_box_pass["x"][ind])*(105/120)
            x_win = round(x_win,2)
            player_ball_receipt = events_ball_receipt[(events_ball_receipt.player_name == player)]
            ax = fig.add_axes([pitch_place[i][0], pitch_place[i][1], width, height])
            pitch = VerticalPitch(line_color='black', line_zorder=2,linewidth=0.8)
            pitch.draw(ax=ax)
            if len(player_ball_receipt) > 2:
                kde = pitch.kdeplot(player_ball_receipt.x, player_ball_receipt.y, ax=ax,
                                    # shade using 100 levels so it looks smooth
                                    shade=True, levels=25,
                                    # shade the lowest area so it looks smooth
                                    # so even if there are no events it gets some color
                                    shade_lowest=True,
                                    cut=25,  # extended the cut so it reaches the bottom edge
                                    cmap=grey_cmap)
            pitch.arrows(player_pass.x, player_pass.y,
                         player_pass.end_x, player_pass.end_y, width=0.8,
                         headwidth=3, headlength=3, color='black', ax=ax)
            pitch.arrows(player_progressive_pass.x, player_progressive_pass.y,
                         player_progressive_pass.end_x, player_progressive_pass.end_y, width=0.9,
                         headwidth=3, headlength=3, color='gold', ax=ax)
            ### Comment for Carry ###
            pitch.arrows(player_box_pass.x, player_box_pass.y,
                         player_box_pass.end_x, player_box_pass.end_y, width=1,
                         headwidth=3, headlength=3, color='lightgreen', ax=ax)
            pitch.arrows(player_incomplete.x, player_incomplete.y,
                         player_incomplete.end_x, player_incomplete.end_y, width=0.3,
                         headwidth=5, headlength=5,headaxislength=12, color='grey', ax=ax)
            plt.title(nom_de_famille(player) + " (" + str(x_win) +" m)", size=6 )
            i += 1
        return(fig)


id_match = API.n_dernier_match(1,["Servette"])[0] 
df_events = API.df_events(id_match)
team = "Servette"

fig = pass_and_ball_receipt(id_match,team,df_events)
plt.show()


  #boucle nombre de match 
# id_match = API.n_dernier_match(3,["FC Zürich"])
# team = "FC Zürich"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = pass_and_ball_receipt(id,team,df_events)
#     plt.show()


