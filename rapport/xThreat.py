import pandas as pd
import socceraction.spadl.statsbomb as statsbomb
import requests
import socceraction.xthreat as xthreat
import socceraction.vaep.features as fs
import socceraction.spadl.config as spadl
import numpy as np
import matplotlib.pyplot as plt
import API


#id_match = API.n_dernier_match(1,["Servette"])[0]


def events(id_match):
    creds = {"user": "m.feigean@servettefc.ch", "passwd": "QzG3Kdlu"}
    username = creds["user"]
    password = creds["passwd"]
    auth = requests.auth.HTTPBasicAuth(username, password)
    URL = "https://data.statsbombservices.com/api/v5/events/%s"%id_match
    obj = requests.get(URL, auth=auth).json()
    if not isinstance(obj, list):
        print("erreur")
    eventsdf = pd.DataFrame(statsbomb._flatten_id(e) for e in obj)
    eventsdf['game_id'] = 3781222
    eventsdf['timestamp'] = pd.to_datetime(eventsdf['timestamp'], format='%H:%M:%S.%f')
    eventsdf['related_events'] = eventsdf['related_events'].apply(
        lambda d: d if isinstance(d, list) else []
    )
    eventsdf['under_pressure'] = eventsdf['under_pressure'].fillna(False).astype(bool)
    eventsdf['counterpress'] = eventsdf['counterpress'].fillna(False).astype(bool)
    eventsdf.rename(
        columns={
            'id': 'event_id',
            'period': 'period_id',
        },
        inplace=True,
    )
    return eventsdf


def xT_model(id_match) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    eventsdf = events(id_match)
    action = {}
    action[id] = statsbomb.convert_to_actions(eventsdf, team1_id)

    for match_id, df_actions in action.items():
        df_actions = spadl.add_names(df_actions)
        [gamestates] = fs.play_left_to_right([df_actions],team1_id)

    xt_model = np.array([[0.00409963, 0.00549638, 0.0066958 , 0.00781556, 0.00894181,
            0.01013774, 0.01142528, 0.01295836, 0.01491013, 0.01700021,
            0.01948768, 0.02195041, 0.02456744, 0.02647576, 0.02637368,
            0.02409153],
           [0.00499392, 0.0064268 , 0.00763493, 0.00871372, 0.01005036,
            0.01117321, 0.01256733, 0.01405955, 0.01599992, 0.0179881 ,
            0.02097624, 0.02361559, 0.02725539, 0.02941437, 0.02984144,
            0.02932228],
           [0.00582552, 0.00720136, 0.00836255, 0.00937503, 0.01062678,
            0.0117787 , 0.01321559, 0.01484979, 0.01681831, 0.01873716,
            0.02178182, 0.02477145, 0.02865249, 0.03478191, 0.03638714,
            0.03497976],
           [0.00623186, 0.00756003, 0.00862166, 0.009781  , 0.01101502,
            0.01233909, 0.01367999, 0.01539952, 0.0173118 , 0.01963822,
            0.02268695, 0.02611771, 0.03177819, 0.04126729, 0.05233114,
            0.04134918],
           [0.00674951, 0.00804892, 0.00896883, 0.01011609, 0.01120825,
            0.01260491, 0.01401887, 0.01566925, 0.01778183, 0.02005299,
            0.02347056, 0.02706223, 0.03474252, 0.06152623, 0.11113268,
            0.11995479],
           [0.00759118, 0.00821425, 0.0089521 , 0.01001239, 0.01135404,
            0.01259956, 0.01412245, 0.0156068 , 0.01784677, 0.02014624,
            0.02383237, 0.02928179, 0.04139236, 0.09393367, 0.15851409,
            0.29944388],
           [0.00755445, 0.00818576, 0.00894441, 0.01009339, 0.01133218,
            0.01255872, 0.01413128, 0.01575158, 0.01774371, 0.02088236,
            0.02363499, 0.02875867, 0.03893667, 0.07919795, 0.15497159,
            0.31294901],
           [0.00665758, 0.0079347 , 0.00876711, 0.01005392, 0.01122292,
            0.01259138, 0.0141653 , 0.01566092, 0.01809278, 0.02049196,
            0.02392497, 0.02751613, 0.03605026, 0.05947732, 0.11180981,
            0.12506967],
           [0.00601098, 0.00748104, 0.00858096, 0.00984912, 0.0110101 ,
            0.01233997, 0.01368898, 0.01549258, 0.01751075, 0.01997996,
            0.02280615, 0.02686846, 0.03240484, 0.04261566, 0.05156938,
            0.04675294],
           [0.00565315, 0.00690612, 0.00822297, 0.00934119, 0.01060322,
            0.01189037, 0.01341277, 0.01498875, 0.01708714, 0.01935744,
            0.02195451, 0.02595768, 0.02933128, 0.03310951, 0.04070389,
            0.03791916],
           [0.00501532, 0.00618154, 0.00743481, 0.0086102 , 0.00974137,
            0.01113421, 0.01261259, 0.01416428, 0.01621544, 0.01835753,
            0.02094357, 0.02399415, 0.02740805, 0.03034299, 0.03244206,
            0.02898712],
           [0.00383138, 0.00513833, 0.00599347, 0.00747179, 0.00879469,
            0.01016253, 0.01163337, 0.01300749, 0.01507945, 0.01719225,
            0.01980799, 0.02244538, 0.02496153, 0.02738504, 0.0276205 ,
            0.02392361]])

    xTModel = xthreat.ExpectedThreat(l=16, w=12)
    xTModel.xT = xt_model


    mov_actions = xthreat.get_successful_move_actions(gamestates)
    mov_actions["xT_value"] = xTModel.predict(mov_actions)

    return(mov_actions,gamestates)


### Visualisation

def prep_viz_xT(id_match) :

    mov_actions,gamestates = xT_model(id_match)

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    n = len(mov_actions)
    xt_team1 = 19*[0]
    xt_team2 = 19*[0]
    for i in mov_actions.index :
        m = mov_actions["time_seconds"][i] / 60
        m = int(m // 5)
        if mov_actions["period_id"][i] == 2 :
            m += 9
        if mov_actions["period_id"][i] == 1 and m > 8 :
            m = 8
        if m > 18 :
            m = 18
        if mov_actions["team_id"][i] == team1_id :
            xt_team1[m] += mov_actions["xT_value"][i]
        else :
            xt_team2[m] += mov_actions["xT_value"][i]

    min = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]

    cumul_xt_1 = np.zeros(20)
    cumul_xt_2 = np.zeros(20)
    xt_diff = np.zeros(20)
    cumul_xt_1[1] = xt_team1[0]
    cumul_xt_2[1] = xt_team2[0]
    for i in range(2,20) :
        xt_diff[i - 1] = xt_team1[i - 2] - xt_team2[i - 2]
        cumul_xt_1[i] = cumul_xt_1[i-1] + xt_team1[i-1]
        cumul_xt_2[i] = cumul_xt_2[i-1] + xt_team2[i-1]
    xt_diff[19] = xt_team1[18] - xt_team2[18]

    return(cumul_xt_1,cumul_xt_2,xt_diff,min)

# xT cumulatif

def xT_cumulatif(id_match) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    cumul_xt_1, cumul_xt_2, xt_diff, min = prep_viz_xT(id_match)

    time_ind = np.arange(0, 100, 15)

    with plt.ioff():

        fig = plt.figure()
        fig = plt.figure(figsize=(16, 9))
        plt.style.use('fivethirtyeight')
        plt.fill_between(min,cumul_xt_1, facecolor='#870E26',alpha = 0.5)
        plt.fill_between(min,cumul_xt_2, facecolor='grey',alpha = 0.5)
        p1 = plt.plot(min,cumul_xt_1,label = team1_name,color = "#870E26")
        p2 = plt.plot(min,cumul_xt_2, label = team2_name,color = "grey")
        plt.ylim([0,3])
        plt.xlabel("Temps du match",fontweight = "bold", fontsize=15)
        plt.ylabel("xT Cumulé",fontweight = "bold", fontsize=15)
        plt.title("Menance Collective",fontsize=30,fontweight = "bold", pad=25)
        #ax.set_xticks(time_ind)
        #ax.legend()
        return(fig)


# xT diff

def xT_diff(id_match) :

    mov_actions,gamestates = xT_model(id_match)

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    cumul_xt_1, cumul_xt_2, xt_diff, min = prep_viz_xT(id_match)

    time_ind = np.arange(0, 100, 5)

    goals_team1 = gamestates[(gamestates.type_name == "shot") & (gamestates.result_name == "success") & (gamestates.team_id == team1_id)]
    goals_team2 = gamestates[(gamestates.type_name == "shot") & (gamestates.result_name == "success") & (gamestates.team_id == team2_id)]

    time_goals_1 = []
    time_goals_2 = []
    for ind in goals_team1.index :
        time = goals_team1["time_seconds"][ind]/60
        if goals_team1["period_id"][ind] == 2 :
            time += 45
        time_goals_1.append(time)
    for ind in goals_team2.index :
        time = goals_team2["time_seconds"][ind]/60
        if goals_team2["period_id"][ind] == 2 :
            time += 45
        time_goals_2.append(time)

    y0 = np.zeros(20)
    yS = np.zeros(len(time_goals_1))
    yO = np.zeros(len(time_goals_2))

    with plt.ioff(): 

        fig = plt.figure()
        fig = plt.figure(figsize=(16, 9))
        plt.style.use('fivethirtyeight')
        plt.fill_between(min,xt_diff,y0,where = (xt_diff >= y0),interpolate=True,facecolor='#870E26',alpha = 0.5)
        plt.fill_between(min,xt_diff,y0,where = (xt_diff <= y0),interpolate=True,facecolor='grey',alpha = 0.5)
        #plt.plot(min,xt_diff,color ='white' )
        plt.plot(time_goals_1,yS,'x',color = "black")
        plt.plot(time_goals_2,yO,'x',color = "black")
        plt.ylim([-0.5,0.5])
        plt.xlabel("Temps du match",fontweight = "bold", fontsize=15)
        plt.ylabel("xT difference",fontweight = "bold", fontsize=15)
        plt.title("Rappport de Force",fontsize=30,fontweight = "bold", pad=25)
        #ax.set_xticks(time_ind)
        return(fig)


# Xthreat par joueur

def nom_de_famille(name):
    ndf = name[0] + '. '
    n = len(name)
    i = 0
    while name[i] != ' ':
        i += 1
    ndf += name[i + 1:n]
    return (ndf)

def xT_joueur(id_match,team,df_events) :

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

    mov_actions,gamestates = xT_model(id_match)

    mov_actions_team = mov_actions[(mov_actions.team_id == team_id)]
    xT_joueur_pos = {}
    xT_joueur_neg = {}
    xT_joueur = {}
    for id in mov_actions_team["player_id"] :
        xT_joueur[id] = 0
        xT_joueur_pos[id] = 0
        xT_joueur_neg[id] = 0
    for ind in mov_actions_team.index :
        id = mov_actions_team["player_id"][ind]
        xT_joueur[id] += mov_actions_team["xT_value"][ind]
        if mov_actions_team["xT_value"][ind] >= 0 :
            xT_joueur_pos[id] += mov_actions_team["xT_value"][ind]
        else :
            xT_joueur_neg[id] += mov_actions_team["xT_value"][ind]

    liste_id = list(xT_joueur.keys())
    for i in range(0,len(liste_id)):
        liste_id[i] = float(liste_id[i])

    nom_joueur = {}
    for ind in df_events.index :
        if df_events["player_id"][ind] in liste_id :
            joueur_id = int(df_events["player_id"][ind])
            nom_joueur[joueur_id] = df_events["player_name"][ind]


    xT_joueur = sorted(xT_joueur.items(),key = lambda t : t[1],reverse = False)

    x_name = []
    y_xT = []
    y_xT_pos = []
    y_xT_neg = []
    for i in range(len(xT_joueur)):
        ind = xT_joueur[i][0]
        x_name.append(nom_de_famille(nom_joueur[ind]))
        y_xT.append(xT_joueur[i][1])
        y_xT_pos.append(xT_joueur_pos[ind])
        y_xT_neg.append(xT_joueur_neg[ind])

    n = len(liste_id)

    with plt.ioff():

        fig = plt.figure(figsize=(12, 9))
        plt.rcParams['axes.facecolor'] = "white"
        ax = plt.axes()
        plt.barh(range(n), y_xT_pos, height=0.6, color="#014182", alpha=0.8)
        plt.barh(range(n), y_xT_neg, height=0.6, color="#f97306", alpha=0.8)
        plt.barh(range(n), y_xT, height=0.2, color="white", alpha=0.8)
        plt.xlim([-0.4, 0.9])
        plt.xlabel("Bleu = menance sur l'adversaire & Orange = danger contre SFC", fontsize=15)
        plt.ylabel("Players", fontsize=15)
        plt.title("La menance par joueur", fontsize=20)
        plt.yticks(range(n), x_name)
        return(fig)

def xT_joueurs(id_match,team,df_events) :
    
    move_action_list = []
    game_states_list = []

    for i in id_match :
        df_matches = API.df_matches
        match_info = df_matches[(df_matches.match_id == i)]
        match_info.reset_index(drop=True, inplace=True)
    
        team1_id = match_info["home_team_id"][0]
        team2_id = match_info["away_team_id"][0]
        team1_name = match_info["home_team_name"][0]
        team2_name = match_info["away_team_name"][0]
    
        if team == team1_name:
            team_id = team1_id
        else:
            team_id = team2_id
    
        mov_actions,gamestates = xT_model(i)
        move_action_list.append(mov_actions)
        game_states_list.append(gamestates)

    mov_actions=pd.concat(move_action_list)
    game_states=pd.concat(game_states_list)
    mov_actions.reset_index(inplace=True, drop=True)
    game_states.reset_index(inplace=True, drop=True)

    mov_actions_team = mov_actions[(mov_actions.team_id == team_id)]
    xT_joueur_pos = {}
    xT_joueur_neg = {}
    xT_joueur = {}
    for id in mov_actions_team["player_id"] :
        xT_joueur[id] = 0
        xT_joueur_pos[id] = 0
        xT_joueur_neg[id] = 0
    for ind in mov_actions_team.index :
        id = mov_actions_team["player_id"][ind]
        print(id)
        print(ind)
        print(xT_joueur)
        xT_joueur[id] += mov_actions_team["xT_value"][ind]
        if mov_actions_team["xT_value"][ind] >= 0 :
            xT_joueur_pos[id] += mov_actions_team["xT_value"][ind]
        else :
            xT_joueur_neg[id] += mov_actions_team["xT_value"][ind]

    liste_id = list(xT_joueur.keys())
    for i in range(0,len(liste_id)):
        liste_id[i] = float(liste_id[i])

    nom_joueur = {}
    for ind in df_events.index :
        if df_events["player_id"][ind] in liste_id :
            joueur_id = int(df_events["player_id"][ind])
            nom_joueur[joueur_id] = df_events["player_name"][ind]


    xT_joueur = sorted(xT_joueur.items(),key = lambda t : t[1],reverse = False)

    x_name = []
    y_xT = []
    y_xT_pos = []
    y_xT_neg = []
    for i in range(len(xT_joueur)):
        ind = xT_joueur[i][0]
        x_name.append(nom_de_famille(nom_joueur[ind]))
        y_xT.append(xT_joueur[i][1])
        y_xT_pos.append(xT_joueur_pos[ind])
        y_xT_neg.append(xT_joueur_neg[ind])

    n = len(liste_id)

    with plt.ioff():

        fig = plt.figure(figsize=(12, 9))
        plt.rcParams['axes.facecolor'] = "white"
        ax = plt.axes()
        plt.barh(range(n), y_xT_pos, height=0.6, color="#014182", alpha=0.8)
        plt.barh(range(n), y_xT_neg, height=0.6, color="#f97306", alpha=0.8)
        plt.barh(range(n), y_xT, height=0.2, color="white", alpha=0.8)
        #plt.xlim([-2, 2])
        plt.xlabel("Bleu = menance sur l'adversaire & Orange = danger contre SFC", fontsize=15)
        plt.ylabel("Players", fontsize=15)
        plt.title("La menance par joueur", fontsize=20)
        plt.yticks(range(n), x_name)
        return(fig)


##Calculate the average number of progressive passes 
## Calculate the avezrage distance of progressive passes 


id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

# fig = xT_joueur(id_match,team,df_events)
# plt.show()

fig = xT_diff(id_match)
plt.show()

fig = xT_cumulatif(id_match)
plt.show()


# # #boucle nombre de match 
# id_match = API.n_dernier_match(3,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = xT_joueur(id,team,df_events)
#     plt.show()


#Concat x matches 
# id_match = API.n_dernier_match(21,["Servette"])
# team = "Servette"
# df_events_list = []
# for id in id_match :
#     df_events = API.df_events(id)
#     df_events_list.append(df_events)

# df_events= pd.concat(df_events_list)
# df_events.reset_index(inplace=True, drop=True)
# fig = xT_joueurs(id_match, 'Servette', df_events)
# plt.show()



