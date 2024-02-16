import requests
from mplsoccer.statsbomb import EVENT_SLUG, read_event, read_competition, read_match
import pandas as pd

creds = {"user":"m.feigean@servettefc.ch","passwd":"QzG3Kdlu"}
username = creds["user"]
password = creds["passwd"]

auth = requests.auth.HTTPBasicAuth(username, password)

### Competitions


URL = "https://data.statsbombservices.com/api/v4/competitions"
response = requests.get(URL, auth=auth)
df_compet = read_competition(response,warn=False)
df_compet = df_compet[(df_compet.competition_name == "Super League")]

# season id 2019/2020 : 42
# season id 2020/2021 : 90

### Matches


df_matches = pd.DataFrame()
for ind in df_compet.index :
    season_id = df_compet["season_id"][ind]
    URL = "https://data.statsbombservices.com/api/v4/competitions/80/seasons/%s/matches"%season_id
    response = requests.get(URL, auth=auth)
    df_matches_season = read_match(response, warn=False)
    df_matches = pd.concat([df_matches,df_matches_season])
df_matches = df_matches.dropna(subset=['home_score', 'away_score'])
df_matches.sort_values(by=["match_date"],ascending = False,inplace=True)
df_matches.reset_index(drop = True,inplace=True)





def teams_in_match(id_match) :
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop = True,inplace=True)
    team1_name = match_info["home_team_name"][0]
    team2_name = match_info["away_team_name"][0]
    return([team1_name,team2_name])




### Récupération des id des matches d'intérêt

def date_correcte(date) :
    chiffre = ['0','1','2','3','4','5','6','7','8','9']
    correcte = True
    if not(type(date) == str) :
        correcte = False
    else :
        n = len(date)
        if n != 10 or date[4] != '-' or date[7] != '-' :
            correcte = False
        elif not(date[0] in chiffre) or not(date[1] in chiffre) or not(date[2] in chiffre)\
            or not(date[3] in chiffre) or not(date[5] in chiffre) or not(date[6] in chiffre)\
            or not(date[8] in chiffre) or not(date[9] in chiffre) :
                correcte = False
        elif not(2000 < int(date[0:4]) < 3000) or not(0 < int(date[5:7]) < 13) or not(0 < int(date[8:10]) < 32) :
            correcte = False
    return(correcte)


def match_id(debut,fin,équipes,journées) :
    if not(date_correcte(debut)) or not(date_correcte(fin)) :
        return("Date renseignée incorrecte : doit être de la forme YYYY-MM-DD")
    debut = pd.Timestamp(debut)
    fin = pd.Timestamp(fin)
    liste_match_id = []
    i = 0
    while df_matches["match_date"][i] > fin and i < len(df_matches) :
        i += 1
    while df_matches["match_date"][i] > debut and i < len(df_matches) :
        if équipes == "all" and journées == "all" :
            liste_match_id.append(df_matches["match_id"][i])
        elif équipes == "all" and df_matches["match_week"][i] in journées :
            liste_match_id.append(df_matches["match_id"][i])
        elif (df_matches["home_team_name"][i] in équipes or df_matches["away_team_name"][i] in équipes) and journées == "all" :
            liste_match_id.append(df_matches["match_id"][i])
        elif (df_matches["home_team_name"][i] in équipes or df_matches["away_team_name"][i] in équipes) and df_matches["match_week"][i] in journées :
            liste_match_id.append(df_matches["match_id"][i])
        i += 1
    return(liste_match_id)

def index_team(liste_team,team) :
    i = 0
    while liste_team[i] != team and i < len(liste_team):
        i += 1
    return(i)

def n_dernier_match(n,équipes):
    liste_match_id = []
    nb_match_équipe = len(équipes)*[0]
    i = 0
    while nb_match_équipe != len(équipes)*[n] and i < len(df_matches) :
        if df_matches["home_team_name"][i] in équipes :
            index = index_team(équipes,df_matches["home_team_name"][i])
            nb_match_équipe[index] += 1
            liste_match_id.append(df_matches["match_id"][i])
        if df_matches["away_team_name"][i] in équipes :
            index = index_team(équipes,df_matches["away_team_name"][i])
            nb_match_équipe[index] += 1
            if not(df_matches["match_id"][i] in liste_match_id) :
                liste_match_id.append(df_matches["match_id"][i])
        i += 1
    return(liste_match_id)


### Events

def df_events(match_id) :
    URL = "https://data.statsbombservices.com/api/v5/events/%s"%match_id
    response = requests.get(URL, auth=auth)
    events = read_event(response,warn=False)
    df = pd.DataFrame(events['event'])
    return(df)

#Read a csv#
# id = n_dernier_match(2,['Servette'])
# df1 =df_events(id[0])
# df2=df_events(id[1])