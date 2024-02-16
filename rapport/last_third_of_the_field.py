import numpy as np
import matplotlib.pyplot as plt
import API

"""
id_match = API.n_dernier_match(1,["Servette"])[0]
"""

def passes_in_the_last_third(id_match,df_events) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]

    df_passes = df_events[(df_events.type_name == "Pass")]
    df_good_passes = df_passes[(df_passes.outcome_name != "Incomplete") & (df_passes.outcome_name != "Injury Clearance") & (df_passes.outcome_name != "Out") & (df_passes.outcome_name != "Pass Offside") & (df_passes.outcome_name != "Unknown")]
    df_carry = df_events[(df_events.type_name == "Carry")]

    minutes = ["5","10","15","20","25","30","35","40","45","50","55",
                "60","65","70","75","80","85","90",">90"]

    n = len(minutes)

    entrées_1 = np.zeros(n)
    passes_1 = np.zeros(n)
    entrées_2 = np.zeros(n)
    passes_2 = np.zeros(n)

    for i in df_good_passes.index :
        m = df_good_passes["minute"][i] // 5
        m = min(18,m)
        if df_good_passes["x"][i] <= 80 and df_good_passes["end_x"][i] >= 80 :
            if df_good_passes["team_id"][i] == team1_id :
                entrées_1[m] += 1
            else :
                entrées_2[m] -= 1
        if df_good_passes["x"][i] >= 80 and df_good_passes["x"][i] >= 80:
            if df_good_passes["team_id"][i] == team1_id:
                passes_1[m] += 1
            else:
                passes_2[m] -= 1

    for i in df_carry.index :
        m = df_carry["minute"][i] // 50
        if df_carry["x"][i] <= 80 and df_carry["x"][i] >= 80 :
            if df_carry["team_id"][i] == team1_id :
                entrées_1[m] += 1
            else :
                entrées_2[m] -= 1

    diff_entrées = entrées_1 + entrées_2
    diff_passes = passes_1 + passes_2

    with plt.ioff():

        fig = plt.figure()
        plt.style.use('fivethirtyeight')
        fig,ax = plt.subplots(figsize = (16,9))
        plt.rcParams['axes.facecolor'] = "white"
        bs = plt.bar(range(n),passes_1,width = 0.6,color = '#870E26',alpha = 0.8)
        bo = plt.bar(range(n),passes_2,width = 0.6,color = 'grey',alpha = 0.8)
        bd = plt.bar(range(n),diff_passes,width = 0.1,color = 'white',alpha = 0.8)
        plt.xticks(range(n),minutes)
        plt.xlabel("Temps du match", fontsize=20,fontweight = "bold", labelpad=15)
        plt.ylabel("Nombre d'entrée", fontsize=20,fontweight = "bold", labelpad=15)
        plt.title("Entrée dans les 30 derniers mètres",fontsize=30,fontweight = "bold", pad=25)
        plt.legend([bs,bo],[team1_name,team2_name])
        return(fig)

id_match = API.n_dernier_match(1,["Servette"])[0]
df_events = API.df_events(id_match)
team = "Servette"

fig = passes_in_the_last_third(id_match,df_events)
plt.show()

# #boucle nombre de match 
# id_match = API.n_dernier_match(3,["Servette"])
# team = "Servette"
# for id in id_match :
#     df_events = API.df_events(id)
#     fig = passes_in_the_last_third(id,df_events)
#     plt.show()


# Code plot pour les entrées dans les 30 derniers mètres

""""
plt.rcParams['axes.facecolor'] = "#4e7496"
bs = plt.bar(range(n),entrées_1,width = 0.6,color = '#014182',alpha = 0.7)
bo = plt.bar(range(n),entrées_2,width = 0.6,color = '#f97306',alpha = 0.7)
bd = plt.bar(range(n),diff_entrées,width = 0.1,color = 'white',alpha = 0.7)
plt.xticks(range(n),minutes)
plt.xlabel("Time intervals - every 5 minutes")
plt.ylabel("Number of entries in the last third of the field")
plt.title("Entries in the last thord of the field during the match")
plt.legend([bs,bo,bd],[team1_name,team2_name,"Difference"])
plt.show()
plt.close()
"""