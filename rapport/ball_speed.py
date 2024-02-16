import numpy as np
import API
import matplotlib.pyplot as plt
import pandas as pd


def ball_speed(id_match,df_events) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop = True,inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    possessions1 = []
    possessions2 = []
    nb_of_pass1 = []
    nb_of_pass2 = []
    avg_ball_speed1 = []
    avg_ball_speed2 = []

    kick_off = df_events[(df_events.sub_type_name == "Kick Off")]
    i = kick_off.index[0]
    n = len(df_events)

    while i < n :
        possession_number = df_events["possession"][i]
        team = df_events["possession_team_name"][i]
        passes = 0
        distance = 0
        time = 0
        while df_events["possession"][i] == possession_number and i < n-1:
            if df_events["type_name"][i] == "Pass" :
                passes += 1
            if df_events["duration"][i] > 0 and df_events["end_x"][i] > 0 and df_events["end_y"][i] > 0:
                x0 = (105*df_events["x"][i])/120
                y0 = (68*df_events["y"][i])/80
                x1 = (105*df_events["end_x"][i])/120
                y1 = (68*df_events["end_y"][i])/80
                distance += np.sqrt((x1-x0)**2 + (y1-y0)**2)
                time += df_events["duration"][i]
            i += 1
        if passes > 0 or distance > 0 :
            if team == team1_name and (distance/time)*3.6 < 80:
                nb_of_pass1.append(passes)
                avg_ball_speed1.append((distance/time)*3.6)
                possessions1.append(len(possessions1)+1)
            elif team == team2_name and (distance/time)*3.6 < 80 :
                nb_of_pass2.append(passes)
                avg_ball_speed2.append((distance/time)*3.6)
                possessions2.append(len(possessions2)+1)
        i += 1

    with plt.ioff():

        fig, (ax1,ax2) = plt.subplots(2,1)
        plt.rcParams['axes.facecolor'] = "#C1CDCD"
        ax1.plot(possessions1,nb_of_pass1,color = "#014182")
        ax1.plot(possessions2,nb_of_pass2,color = "#f97306")
        ax2.plot(possessions1,avg_ball_speed1,color = "#014182")
        ax2.plot(possessions2,avg_ball_speed2,color = "#f97306")
        ax1.set_xlabel("Possession number")
        ax2.set_xlabel("Possession number")
        ax1.set_ylabel("Number of passes")
        ax2.set_ylabel("Average ball speed")

        return(fig)

id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = ball_speed(id_match,df_events)
plt.show()

# #boucle nombre de match 
# id_match = API.n_dernier_match(3,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = ball_speed(id,df_events)
#     plt.show()









