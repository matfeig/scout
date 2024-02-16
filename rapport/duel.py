import numpy as np
import API
import matplotlib.pyplot as plt



def indice_player(player,players):
    ind = 0
    while players[ind] != player:
        ind += 1
    return (ind)

def nom_de_famille(name):
    ndf = name[0] + '. '
    n = len(name)
    i = 0
    while name[i] != ' ':
        i += 1
    ndf += name[i + 1:n]
    return (ndf)


def duel(team,id_match,df_events) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop = True,inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    if team == team1_name :
        team_id = team1_id
    else :
        team_id = team2_id


    df_events_team = df_events[(df_events.team_id == team_id)]

    players = list(df_events_team["player_name"].value_counts().index)

    events_clearance = df_events_team[(df_events_team.type_name == "Clearance")]
    events_duel = df_events_team[(df_events_team.type_name == "Duel")]

    n = len(players)

    duel_win = np.zeros(n)
    duel_lost = np.zeros(n)
    clearance = np.zeros(n)

    for i in events_clearance.index :
        player = events_clearance["player_name"][i]
        ind = indice_player(player,players)
        if events_clearance["aerial_won"][i] == True :
            duel_win[ind] += 1
        else :
            clearance[ind] += 1
    for i in events_duel.index :
        player = events_duel["player_name"][i]
        ind = indice_player(player,players)
        if events_duel["sub_type_name"][i] == "Aerial Lost" or events_duel["sub_type_name"][i] == "Lost":
            duel_lost[ind] -= 1
        else :
            duel_win[ind] += 1

    win = duel_win + clearance
    lost = duel_lost

    max_x = max(win)
    min_x = np.min(lost)

    tri = np.argsort(win)
    players = np.array(players)[tri]
    duel_win = duel_win[tri]
    duel_lost = duel_lost[tri]
    clearance = clearance[tri]

    for i in range(len(players)) :
        players[i] = nom_de_famille(players[i])

    with plt.ioff():

        fig = plt.figure(figsize=(16,9))
        plt.rcParams['axes.facecolor'] = "white"
        w1 = plt.barh(range(n),duel_win,height = 0.6,color = "green",edgecolor = '#014182')
        w2 = plt.barh(range(n),clearance,height = 0.6,left = duel_win,color = "springgreen",edgecolor = '#014182',hatch = '...')
        l1 = plt.barh(range(n),duel_lost,height = 0.6,color = "red",edgecolor = '#f97306')
        plt.yticks(range(n),players)
        plt.legend([w1,w2,l1],["Duel win","Clearance","Duel lost"],loc = 'lower right')
        plt.xlabel("Number of duels",fontsize = 15)
        plt.ylabel("Players",fontsize = 15)
        plt.xlim(min_x - 1,max_x + 1)
        plt.title("Duels gagnés et perdus par les joueurs ",fontsize = 30,fontweight = "bold", pad=25)
        return(fig)

id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = duel(team,id_match,df_events)
plt.show()

# #boucle nombre de match 
# id_match = API.n_dernier_match(3,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = duel(team,id,df_events)
#     plt.show()



"""
def duel(team,id_match,df_events) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop = True,inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    if team == team1_name :
        team_id = team1_id
    else :
        team_id = team2_id


    df_events_team = df_events[(df_events.team_id == team_id)]

    players = list(df_events_team["player_name"].value_counts().index)

    events_50_50 = df_events_team[(df_events_team.type_name == "50/50")]
    events_clearance = df_events_team[(df_events_team.type_name == "Clearance")]
    events_duel = df_events_team[(df_events_team.type_name == "Duel")]
    events_block = df_events_team[(df_events_team.type_name == "Block")]
    events_dribbled_past = df_events_team[(df_events_team.type_name == "Dribbled Past")]

    n = len(players)

    duel_win = np.zeros(n)
    duel_lost = np.zeros(n)
    block = np.zeros(n)
    clearance = np.zeros(n)
    dribbled_past = np.zeros(n)
    win_50_50 = np.zeros(n)
    lost_50_50 = np.zeros(n)

    for i in events_clearance.index :
        player = events_clearance["player_name"][i]
        ind = indice_player(player,players)
        if events_clearance["aerial_won"][i] == True :
            duel_win[ind] += 1
        else :
            clearance[ind] += 1
    for i in events_duel.index :
        player = events_duel["player_name"][i]
        ind = indice_player(player,players)
        if events_duel["sub_type_name"][i] == "Aerial Lost" or events_duel["sub_type_name"][i] == "Lost" or events_duel["sub_type_name"][i] == "Lost In Play":
            duel_lost[ind] -= 1
        else :
            duel_win[ind] += 1
    for i in events_block.index :
        player = events_block["player_name"][i]
        ind = indice_player(player,players)
        if "block_offensice" in list(df_events.columns) :
            if events_block["block_offensive"][i] != True :
                block[ind] += 1
        else :
            block[ind] += 1
    for i in events_dribbled_past.index :
        player = events_dribbled_past["player_name"][i]
        ind = indice_player(player,players)
        dribbled_past[ind] -= 1
    for i in events_50_50.index :
        player = events_50_50["player_name"][i]
        ind = indice_player(player,players)
        if events_50_50["outcome_name"][i] == "Lost" :
            lost_50_50[ind] -= 1
        else :
            win_50_50 += 1

    win = duel_win + block + clearance + win_50_50
    lost = duel_lost + dribbled_past + lost_50_50

    max_x = max(win)
    min_x = np.min(lost)

    tri = np.argsort(win)
    players = np.array(players)[tri]
    duel_win = duel_win[tri]
    duel_lost = duel_lost[tri]
    block = block[tri]
    clearance = clearance[tri]
    dribbled_past = dribbled_past[tri]
    win_50_50 = win_50_50[tri]
    lost_50_50 = lost_50_50[tri]

    for i in range(len(players)) :
        players[i] = nom_de_famille(players[i])

    with plt.ioff():

        fig = plt.figure(figsize=(12,9))
        plt.rcParams['axes.facecolor'] = "#C1CDCD"
        w1 = plt.barh(range(n),duel_win,height = 0.6,color = "#014182",edgecolor = '#014182')
        w2 = plt.barh(range(n),block,height = 0.6,left = duel_win,color = "#C1CDCD",edgecolor = '#014182',hatch = '///')
        w3 = plt.barh(range(n),clearance,height = 0.6,left = duel_win + block,color = "#C1CDCD",edgecolor = '#014182',hatch = '...')
        w4 = plt.barh(range(n),win_50_50,height = 0.6,left = duel_win + block + clearance,color = "#C1CDCD",edgecolor = '#014182',hatch = 'ooo')
        l1 = plt.barh(range(n),duel_lost,height = 0.6,color = "#f97306",edgecolor = '#f97306')
        l2 = plt.barh(range(n),dribbled_past,height = 0.6,left = duel_lost,color = "#C1CDCD",edgecolor = '#f97306',hatch = '///')
        l3 = plt.barh(range(n),lost_50_50,height = 0.6,left = duel_lost + dribbled_past,color = "#C1CDCD",edgecolor = '#f97306',hatch = 'ooo')
        plt.yticks(range(n),players)
        plt.legend([w1,w2,w3,w4,l1,l2,l3],["Duel win","Block","Clearance","50/50 win","Duel lost","Dribbled past","50/50 lost"],loc = 'lower right')
        plt.xlabel("Number of duels",fontsize = 15)
        plt.ylabel("Players",fontsize = 15)
        plt.xlim(min_x - 1,max_x + 1)
        plt.title("Duels won and lost by each player",fontsize = 22)
        return(fig)
"""