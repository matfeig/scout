import API
import numpy as np
import pandas as pd


def indices_possessions(id_match,team,df_events) :

    df_team = df_events[(df_events.possession_team_name == team)]
    df_team.reset_index(drop = True,inplace=True)

    i = 0
    n = len(df_team)
    p_time = 0
    last_third_time = 0
    p_number = 0
    shot_number = 0
    pass_number = 0
    last_third_time = 0
    while i < n :
        p = df_team["possession"][i]
        temps_debut = 60*(df_team["minute"][i]) + df_team["second"][i] + 0.001*(df_team["timestamp_millisecond"][i])
        in_the_last_third = False
        while df_team["possession"][i] == p and i < n-1 :
            if df_team["type_name"][i] == "Shot" :
                shot_number += 1
            elif df_team["type_name"][i] == "Pass" :
                pass_number += 1
            if in_the_last_third == False and df_team["x"][i] > 80 :
                in_the_last_third = True
                temps_debut_last_third = 60*(df_team["minute"][i]) + df_team["second"][i] + 0.001*(df_team["timestamp_millisecond"][i])
            elif in_the_last_third == True and df_team["x"][i] < 80  :
                in_the_last_third = False
                temps_fin_last_third = 60 * (df_team["minute"][i]) + df_team["second"][i] + 0.001 * (df_team["timestamp_millisecond"][i])
                if df_team["duration"][i] > 0:
                    temps_fin_last_third += df_team["duration"][i]
                last_third_time += temps_fin_last_third - temps_debut_last_third
            i += 1
        if i == n-1 :
            if df_team["type_name"][i] == "Shot" :
                shot_number += 1
            elif df_team["type_name"][i] == "Pass" :
                pass_number += 1
            i += 1
        temps_fin = 60*(df_team["minute"][i-1]) + df_team["second"][i-1] + 0.001*(df_team["timestamp_millisecond"][i-1])
        if df_team["duration"][i-1] > 0 :
            temps_fin += df_team["duration"][i-1]
        p_time += temps_fin - temps_debut
        if in_the_last_third == True :
            last_third_time += temps_fin - temps_debut_last_third
        p_number += 1
    p_time = round(p_time/60,2)
    last_third_time = round(last_third_time/60,2)
    shot_by_possession = round(p_number/shot_number,2)
    pass_by_possession = round(pass_number/p_number,2)
    return(p_time,shot_by_possession,pass_by_possession,last_third_time)


def indices_def(id_match,team,df_events) :

    df_team = df_events[(df_events.team_name == team)]
    df_team.reset_index(drop = True,inplace=True)

    df_opponent_team = pd.concat([df_events, df_team]).drop_duplicates(keep=False)
    events_pass_opponent = df_opponent_team[(df_opponent_team.type_name == 'Pass')]
    events_pass_opponent = events_pass_opponent[(events_pass_opponent.end_x > 48)]

    number_opponent_pass = len(events_pass_opponent)

    events_duel = df_team[(df_team.type_name == "Duel")]
    events_duel = events_duel[(events_duel.sub_type_name == "Tackle")]

    events_interception = df_team[(df_team.type_name == "Interception")]
    events_interception_win = events_interception[(events_interception.outcome_id == 4) | (events_interception.outcome_id == 15) | (events_interception.outcome_id == 16) | (events_interception.outcome_id == 17)]

    events_foul_committed = df_team[(df_team.type_name == "Foul Committed")]

    defensive_action = pd.concat([events_duel,events_interception_win,events_foul_committed])
    defensive_action = defensive_action[(defensive_action.x < 72)]

    number_defensive_actions = len(defensive_action)

    teams_in_match = API.teams_in_match(id_match)
    if teams_in_match[0] == team :
        opponent_team = teams_in_match[1]
    else :
        opponent_team = teams_in_match[0]
    defensive_possession_time = indices_possessions(id_match,opponent_team,df_events)[0]
    challenge_intensity_index = number_defensive_actions/defensive_possession_time

    x_average = 0
    x_average_cb = 0
    n_cb = 0
    for ind in defensive_action.index :
        x_average += defensive_action["x"][ind]
        if int(defensive_action["position_id"][ind]) in [3,4,5] :
            x_average_cb += defensive_action["x"][ind]
            n_cb += 1
    x_average = x_average/number_defensive_actions
    x_average_cb = x_average_cb/n_cb

    PPDA = number_opponent_pass/number_defensive_actions

    return (PPDA,round(challenge_intensity_index,2),round(x_average,2),round(x_average_cb,2))


def indices_tirs(id_match,team,df_events) :

    df_team = df_events[(df_events.possession_team_name == team)]
    df_team.reset_index(drop=True, inplace=True)

    df_shots = df_team[(df_team.type_name == "Shot")]

    n = len(df_shots)
    passes_moy = 0
    temps_moy = 0

    for ind in df_shots.index :
        passes = 0
        p = df_shots["possession"][ind]
        temps_tir = 60*(df_shots["minute"][ind]) + df_shots["second"][ind] + 0.001*(df_shots["timestamp_millisecond"][ind])
        df_p = df_team[(df_team.possession == p)]
        df_p.reset_index(drop=True, inplace=True)
        temps_debut = 60*(df_p["minute"][0]) + df_p["second"][0] + 0.001*(df_p["timestamp_millisecond"][0])
        for i in df_p.index :
            if df_p["type_name"][i] == "Pass" and not(df_p["outcome_id"][i] > 0) :
                passes += 1
        passes_moy += passes
        temps_moy += (temps_tir - temps_debut)

    passes_moy = passes_moy/n
    temps_moy = temps_moy/n
    return(round(passes_moy,2),round(temps_moy,2))

