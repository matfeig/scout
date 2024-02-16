import API
import indices
import xThreat
import pandas as pd
import numpy as np

team_matches = pd.DataFrame(columns=['match_id','match_date','team_id','team_name','Possession time','Last third possession time','Pass by possession','Possessions/Shot','Number of passes before a shot','Possession time before a shot','PPDA','Challenge intensity index','Average heigth of defensive actions','Average heigth of defensive actions (center backs)','xG','xT'])
team_matches.to_csv('/Users/matfeig/Dropbox/SFC/code/Database/team_matches.csv')
 

def xG_values(id_match,df_events) :

    df_matches = API.df_matches
    match_info = df_matches[(df_matches.match_id == id_match)]
    match_info.reset_index(drop=True, inplace=True)

    team1_id = match_info["home_team_id"][0]
    team2_id = match_info["away_team_id"][0]

    events_shots = df_events[(df_events.type_name == "Shot")]
    events_shots_team1 = events_shots[(events_shots.team_id == team1_id)]
    events_shots_team2 = events_shots[(events_shots.team_id == team2_id)]

    xG_team1 = [0]
    xG_team2 = [0]

    for ind in events_shots_team1.index:
        xG_team1.append(events_shots_team1["shot_statsbomb_xg"][ind] + xG_team1[-1])
    for ind in events_shots_team2.index:
        xG_team2.append(events_shots_team2["shot_statsbomb_xg"][ind] + xG_team2[-1])

    return(xG_team1[-1],xG_team2[-1])



def add_last_games(teams_matches) :

    teams_matches.sort_values(by=["match_date"], ascending=False, inplace=True)
    teams_matches_id = list(teams_matches['match_id'])
    df_matches = API.df_matches
    df_matches = df_matches.iloc[:180, :]
    already_added = False
    i = 0
    n = len(df_matches)
    while not(already_added) and i < n :
        id_match = df_matches['match_id'][i]
        df_events = API.df_events(id_match)
        date = df_matches['match_date'][i]
        date = str(date)[0:180]
        if id_match in teams_matches_id :
            already_added = True
        else :
            team1,team2 = df_matches["home_team_name"][i],df_matches["away_team_name"][i]
            team1_id,team2_id = df_matches["home_team_id"][i],df_matches["away_team_id"][i]
            dic1 = {'match_id' : [id_match],'match_date' : date,'team_id' : [team1_id],'team_name' : [team1]}
            dic2 = {'match_id': [id_match], 'match_date': date, 'team_id': [team2_id],'team_name': [team2]}
            ind1_1,ind1_2,ind1_3,ind1_4 = indices.indices_possessions(id_match,team1,df_events)
            ind1_5,ind1_6 = indices.indices_tirs(id_match,team1,df_events)
            ind1_7,ind1_8,ind1_9,ind1_10 = indices.indices_def(id_match,team1,df_events)
            dic1['Possession time'],dic1['Last third possession time'] = [ind1_1],[ind1_2]
            dic1['Pass by possession'],dic1['Possessions/Shot'] = [ind1_3],[ind1_4]
            dic1['Number of passes before a shot'],dic1['Possession time before a shot'] = [ind1_5],[ind1_6]
            dic1['PPDA'],dic1['Challenge intensity index'] = [ind1_7],[ind1_8]
            dic1['Average heigth of defensive actions'],dic1['Average heigth of defensive actions (center backs)'] = [ind1_9],[ind1_10]
            ind2_1, ind2_2, ind2_3, ind2_4 = indices.indices_possessions(id_match,team2,df_events)
            ind2_5, ind2_6 = indices.indices_tirs(id_match,team2,df_events)
            ind2_7, ind2_8,ind2_9, ind2_10 = indices.indices_def(id_match,team2,df_events)
            dic2['Possession time'],dic2['Last third possession time'] = [ind2_1],[ind2_2]
            dic2['Pass by possession'],dic2['Possessions/Shot'] = [ind2_3],[ind2_4]
            dic2['Number of passes before a shot'],dic2['Possession time before a shot'] = [ind2_5],[ind2_6]
            dic2['PPDA'],dic2['Challenge intensity index'] = [ind2_7],[ind2_8]
            dic2['Average heigth of defensive actions'],dic2['Average heigth of defensive actions (center backs)'] = [ind2_9],[ind2_10]
            xG1,xG2 = xG_values(id_match,df_events)
            xT_cumul_1,xT_cumul_2,xT_diff,min = xThreat.prep_viz_xT(id_match)
            xT1,xT2 = xT_cumul_1[-1],xT_cumul_2[-1]
            dic1['xG'],dic1['xT'] = [xG1],[xT1]
            dic2['xG'], dic2['xT'] = [xG2], [xT2]
            line1 = pd.DataFrame(dic1)
            line2 = pd.DataFrame(dic2)
            teams_matches = pd.concat([teams_matches,line1,line2])
            i += 1
            print(i)
    teams_matches.reset_index(drop=True,inplace=True)
    teams_matches.sort_values(by=["match_date"], ascending=False, inplace=True)
    return(teams_matches)


teams_matches = pd.read_csv("/Users/matfeig/Dropbox/SFC/code/Database/team_matches.csv")
teams_matches = add_last_games(teams_matches)
teams_matches.to_csv("/Users/matfeig/Dropbox/SFC/code/Database/team_matches.csv",index = False)






