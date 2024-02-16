import API
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def number_of_touch(id_match,team,angle,df_events) :

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

    team_events = df_events[(df_events.team_name == team)]

    events_ball_receipt = team_events[(df_events.type_name == 'Ball Receipt')]
    events_pass = team_events[(df_events.type_name == 'Pass')]

    angle = (angle*np.pi)/180

    events_pass_forward = events_pass[(events_pass.pass_angle <= angle)]
    events_pass_forward = events_pass_forward[(events_pass_forward.pass_angle >= (-1) * angle)]
    events_pass_backward = pd.concat([events_pass, events_pass_forward]).drop_duplicates(keep=False)

    players = np.array(list(team_events["player_name"].value_counts().index))
    entered_players = np.array(list(team_events["substitution_replacement_name"].value_counts().index))
    first_team_players = np.setdiff1d(players, entered_players)

    n = len(players)
    one_touch_forward = np.zeros(n)
    two_touch_forward = np.zeros(n)
    one_touch_backward = np.zeros(n)
    two_touch_backward = np.zeros(n)

    i = 0
    for player in players:
        player_ball_receipt = events_ball_receipt[(events_ball_receipt.player_name == player)]
        player_pass_forward = events_pass_forward[(events_pass.player_name == player)]
        player_pass_backward = events_pass_backward[(events_pass.player_name == player)]
        pass_forward_id = list(player_pass_forward.index)
        pass_backward_id = list(player_pass_backward.index)
        for ind in player_ball_receipt.index:
            for id in pass_forward_id:
                if 0 < id - ind < 10:
                    t1 = 60 * (player_ball_receipt["minute"][ind]) + player_ball_receipt["second"][ind] + 0.001 * (
                    player_ball_receipt["timestamp_millisecond"][ind])
                    t2 = 60 * (player_pass_forward["minute"][id]) + player_pass_forward["second"][id] + 0.001 * (
                    player_pass_forward["timestamp_millisecond"][id])
                    if t2 - t1 == 0:
                        one_touch_forward[i] += 1
                    elif t2 - t1 < 1.5:
                        two_touch_forward[i] += 1
            for id in pass_backward_id:
                if 0 < id - ind < 10:
                    t1 = 60 * (player_ball_receipt["minute"][ind]) + player_ball_receipt["second"][ind] + 0.001 * (
                    player_ball_receipt["timestamp_millisecond"][ind])
                    t2 = 60 * (player_pass_backward["minute"][id]) + player_pass_backward["second"][id] + 0.001 * (
                    player_pass_backward["timestamp_millisecond"][id])
                    if t2 - t1 == 0:
                        one_touch_backward[i] -= 1
                    elif t2 - t1 < 1.5:
                        two_touch_backward[i] -= 1
        m = len(player_ball_receipt)
        one_touch_forward[i] = (one_touch_forward[i] / m) * 100
        two_touch_forward[i] = (two_touch_forward[i] / m) * 100
        one_touch_backward[i] = (one_touch_backward[i] / m) * 100
        two_touch_backward[i] = (two_touch_backward[i] / m) * 100
        i += 1
        
    #two_touch_forward.sort_values("two",axis = 0, ascending=False, inplace=True)

    with plt.ioff():
        fig = plt.figure()
        fig = plt.figure(figsize=(16, 9))
        plt.style.use('fivethirtyeight')
        #plt.rcParams['axes.facecolor'] = "#C1CDCD"
        b1f = plt.barh(range(n), one_touch_forward, height=0.7, color='green', alpha=0.8)
        b2f = plt.barh(range(n), two_touch_forward, left=one_touch_forward, height=0.7, color='green', alpha=0.8,hatch = '///')
        b1b = plt.barh(range(n), one_touch_backward, height=0.7, color='red', alpha=0.8)
        b2b = plt.barh(range(n), two_touch_backward, left=one_touch_backward, height=0.7, color='red', alpha=0.8,hatch = '///')
        plt.yticks(range(n), players)
        plt.xticks(range(-30,60, 10),fontweight = "bold", fontsize=15)
        #plt.xlabel("Time intervals - every 5 minutes")
        #plt.ylabel("Number of passes in the last third of the field")
        #plt.title("Passes in the last third of the field during the match")
        plt.title("Jeu vers l'avant", fontsize=30,fontweight = "bold", pad=25)
        plt.legend([b1f, b2f,b1b,b2b], ["% une touche avant"," % pass <2s avant","% une touche arrière"," % pass <2s arrière"],fontsize = 15, loc="upper right")
        return(fig)

id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = number_of_touch(id_match,team,90,df_events)
plt.show()

# #boucle nombre de match 
# id_match = API.n_dernier_match(6,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = number_of_touch(id,team,90,df_events)
#     plt.show()
