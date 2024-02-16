import matplotlib.pyplot as plt
import API
import numpy as np
from highlight_text import fig_text


def xg(id_match,df_events):

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    events_shots = df_events[(df_events.type_name == "Shot")]
    events_shots_team1 = events_shots[(events_shots.team_id == team1_id)]
    events_shots_team2= events_shots[(events_shots.team_id == team2_id)]

    min_team1 = [0]
    min_team2 = [0]
    xG_team1 = [0]
    xG_team2 = [0]

    for ind in events_shots_team1.index :
        min = events_shots_team1["minute"][ind]
        sec = (events_shots_team1["second"][ind]*100/60) * 10**(-2)
        min_team1.append(min + sec)
        xG_team1.append(events_shots_team1["shot_statsbomb_xg"][ind] + xG_team1[-1])
    for ind in events_shots_team2.index :
        min = events_shots_team2["minute"][ind]
        sec = (events_shots_team2["second"][ind]*100/60) * 10**(-2)
        min_team2.append(min + sec)
        xG_team2.append(events_shots_team2["shot_statsbomb_xg"][ind] + xG_team2[-1])

    n = len(df_events)
    stop_time = df_events["minute"][n-1] + (df_events["second"][n-1]*100/60)*10**(-2)
    min_team1.append(stop_time)
    min_team2.append(stop_time)

    with plt.ioff():

        fig = plt.figure()
        plt.style.use('fivethirtyeight')
        fig,ax = plt.subplots(figsize = (16,9))
        plt.rcParams['axes.facecolor'] = "white"
        plt.stairs(xG_team1,min_team1,baseline = None,fill=False,linewidth=5,label = team1_name,color = '#870E26')
        plt.stairs(xG_team2,min_team2,baseline = None, fill=False,linewidth=5,label = team2_name,color = 'grey')
        #plt.axvline(45, 0, 1,linewidth=2, color = "k")
        plt.axhline(y=1.19, xmin=0.05, xmax=50, linewidth=2, color = '#870E26', ls='--')
        fig_text(0.13,0.45,"xG SFC", color = "#870E26",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
        plt.axhline(y=1.07, xmin=0.05, xmax=60, linewidth=2, color = 'Grey', ls='--')
        fig_text(0.13,0.35,"xG adv", color = "Grey",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
        plt.ylim(-0.02,max(xG_team2[-1],xG_team1[-1]) + 0.5)
        plt.yticks([0,0.7,1.4,2.1,2.8])
        plt.xticks([0,15,30,45,60,75,90])
        fig_text(0.13,0.80, s="Mi-temps 1\n", fontsize = 12, fontweight = "bold", color = "black")
        fig_text(0.51,0.80, s="Mi-temps 2\n", fontsize = 12 , fontweight = "bold", color = "black")
        plt.text(min_team1[-1] + 1,xG_team1[-1],str(round(xG_team1[-1],2)),color = '#870E26')
        plt.text(min_team2[-1] + 1,xG_team2[-1],str(round(xG_team2[-1],2)),color = 'grey')
        plt.xlabel("Minute de Jeu",fontsize = 20, fontweight = "bold", color = "black", labelpad=15)
        plt.ylabel("Valeur de xG",fontsize = 20, fontweight = "bold", color = "black")
        plt.title("Expected Goals",fontsize = 30, fontweight = "bold", color = "black", pad=30)
        plt.legend(frameon = True,loc = 'upper right')
        return(fig)

id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = xg(id_match,df_events)
plt.show()

# #boucle nombre de match 
# id_match = API.n_dernier_match(3,["Servette"])
# team = "Servette" 
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = xg(id,df_events)
#     plt.show()
