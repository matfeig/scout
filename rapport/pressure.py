import numpy as np
import API
import matplotlib.pyplot as plt

""""
id_match = API.n_dernier_match(1,["Servette"])[0]
"""

def pressure(id_match,team,df_events) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop = True,inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]


    if team == team1_name:
        team_id = team1_id
    else:
        team_id = team2_id

    df_events = df_events[(df_events.team_id == team_id)]
    df_pressure = df_events[(df_events.type_name == "Pressure")]
    df_pressure.reset_index(drop = True,inplace=True)

    players_id = np.array(list(df_events["player_id"].value_counts().index))
    players = list(df_events["player_name"].value_counts().index)
    n = len(players_id)
    nb_pressure = np.zeros(n)
    pressure_time = np.zeros(n)

    def indice_player(player,players):
        ind = 0
        while players[ind] != player:
            ind += 1
        return (ind)

    for i in range(len(df_pressure)) :
        player_id = df_pressure["player_id"][i]
        ind = indice_player(player_id,players_id)
        nb_pressure[ind] += 1
        pressure_time[ind] -= df_pressure["duration"][i]

    tri = np.argsort(nb_pressure)
    players = np.array(players)[tri]
    nb_pressure = nb_pressure[tri]
    pressure_time = pressure_time[tri]

    with plt.ioff() :

        fig = plt.figure(figsize=(16,9))
        plt.style.use('fivethirtyeight')
        #plt.rcParams['axes.facecolor'] = "white"
        b1 = plt.barh(range(n),nb_pressure,height = 0.8,color = "black")
        b2 = plt.barh(range(n),pressure_time,height = 0.8,color = "silver")
        plt.axvline(10, 0, 3,linewidth=1, color = "black")
        plt.axvline(-10, 0, 3,linewidth=1, color = "black")
        plt.yticks(range(n),players)
        plt.xticks([-10,0,10])
        plt.legend([b1,b2],["Nombre de pressing","Temps de pressing"],frameon = True,loc = 'lower right')
        plt.xlabel("Temps de pressing(s)                                                                        Nombre de pressing",fontsize = 20,fontweight = "bold", labelpad=15)
        plt.ylabel("Joueurs",fontsize = 20,fontweight = "bold")
        plt.title("Pressing",fontsize = 30,fontweight = "bold", pad=25)


        return(fig)

id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = pressure(id_match,team,df_events)
plt.show()

# #boucle nombre de match 
# id_match = API.n_dernier_match(3,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = pressure(id,team,df_events)
#     plt.show()


