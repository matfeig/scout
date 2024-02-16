#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 14:16:53 2021

@author: matfeig
"""

from mplsoccer.pitch import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import pandas as pd
import requests
from mplsoccer.statsbomb import EVENT_SLUG, read_event, read_competition, read_match
import numpy as np


creds = {"user":"m.feigean@servettefc.ch","passwd":"QzG3Kdlu"}
username = creds["user"]
password = creds["passwd"]

id = 3781222
Servette_id = 1330
Opponent_id = 1176

auth = requests.auth.HTTPBasicAuth(username, password)

URL = "https://data.statsbombservices.com/api/v4/competitions/80/seasons/90/matches"
response = requests.get(URL, auth=auth)
df_matches = read_match(response,warn=False).set_index("match_id")

URL = "https://data.statsbombservices.com/api/v5/events/3781222"
obj = requests.get(URL, auth=auth)
events = read_event(obj,warn=False)
df_events = pd.DataFrame(events['event'])

df_events_Servette = df_events[(df_events.team_id == Servette_id)]

events_duel = df_events_Servette[(df_events_Servette.type_name == "Duel")]
events_won_duel = events_duel[(events_duel.outcome_id == 4) | (events_duel.outcome_id == 15) | (events_duel.outcome_id == 16) | (events_duel.outcome_id == 17)]
events_lost_duel = events_duel[(events_duel.outcome_id == 1) | (events_duel.outcome_id == 13) | (events_duel.outcome_id == 14)]

events_interception = df_events_Servette[(df_events_Servette.type_name == "Interception")]
events_won_interception = events_interception[(events_interception .outcome_id == 4) | (events_interception .outcome_id == 15) | (events_interception .outcome_id == 16) | (events_interception .outcome_id == 17)]
events_lost_interception = events_interception[(events_interception .outcome_id == 1) | (events_interception .outcome_id == 13) | (events_interception .outcome_id == 14)]

events_ball_recovery = df_events_Servette[(df_events_Servette.type_name == "Ball Recovery")]

events_substitution = df_events_Servette[(df_events_Servette.type_name == "Substitution")]
events_goal = df_events_Servette[(df_events_Servette.position_name) == "Goalkeeper"]

players = np.array(list(df_events_Servette["player_name"].value_counts().index))
entered_players = np.array(list(df_events_Servette["substitution_replacement_name"].value_counts().index))
goal = np.array(list(events_goal["player_name"].value_counts().index))
first_team_player = np.setdiff1d(players,entered_players)
fields_player = np.setdiff1d(first_team_player,goal)


width,height = 0.2,0.265
pitch_place = [[0.15,0],[0.3,0],[0.45,0],[0.6,0],[0.225,0.3],[0.375,0.3],[0.525,0.3],[0.225,0.6],[0.375,0.7],[0.525,0.6]]

ind_positions = {'Left Back' : 0, 'Left Center Back' : 1, 'Right Center Back' : 2, 'Right Back' : 3,
                 'Left Center Midfield' : 4, 'Center Defensive Midfield' : 5,'Right Center Midfield' : 6,
                 'Left Wing' : 7, 'Center Forward' : 8, 'Right Wing' : 9}

fig,ax0 = plt.subplots()
ax0.set_frame_on(False)
ax0.set_visible(False)
for player in fields_player :
    j = 0
    while df_events['player_name'][j] != player :
        j += 1
    i = ind_positions[df_events['position_name'][j]]
    player_won_interception = events_won_interception[(events_won_interception.player_name == player)]
    player_lost_interception = events_lost_interception[(events_lost_interception.player_name == player)]
    player_won_duel = events_won_duel[(events_won_duel.player_name == player)]
    player_lost_duel = events_lost_duel[(events_lost_duel.player_name == player)]
    player_ball_recovery = events_ball_recovery[(events_ball_recovery.player_name == player)]
    player_won_action = pd.concat([player_won_interception,player_won_duel,player_ball_recovery],axis = 0)
    player_lost_action = pd.concat([player_lost_interception,player_lost_duel],axis = 0)
    ax = fig.add_axes([pitch_place[i][0],pitch_place[i][1],width,height])
    pitch = VerticalPitch()
    pitch.draw(ax =ax)
    if len(player_won_action) > 2 :
        hull1 = pitch.convexhull(player_won_action.x, player_won_action.y)
        poly1 = pitch.polygon(hull1, ax=ax, edgecolor='cornflowerblue', facecolor='cornflowerblue', alpha=0.3)
    scatter1 = pitch.scatter(player_won_action.x, player_won_action.y, ax=ax, edgecolor='black', facecolor='cornflowerblue')
    if len(player_lost_action) > 2 :
        hull2 = pitch.convexhull(player_lost_action.x, player_lost_action.y)
        poly2 = pitch.polygon(hull2, ax=ax, edgecolor='red', facecolor='red', alpha=0.3)
    scatter2 = pitch.scatter(player_lost_action.x, player_lost_action.y, ax=ax, edgecolor='black', facecolor='red')
    #plt.title(player)
    i += 1
plt.show()
