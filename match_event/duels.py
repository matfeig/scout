#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 14:25:27 2021

@author: matfeig
"""

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

players = list(df_events_Servette["player_name"].value_counts().index)

events_50_50 = df_events_Servette[(df_events_Servette.type_name == "50/50")]
events_clearance = df_events_Servette[(df_events_Servette.type_name == "Clearance")]
events_duel = df_events_Servette[(df_events_Servette.type_name == "Duel")]
events_block = df_events_Servette[(df_events_Servette.type_name == "Block")]
events_dribbled_past = df_events_Servette[(df_events_Servette.type_name == "Dribbled Past")]

n = len(players)

duel_win = np.zeros(n)
duel_lost = np.zeros(n)
block = np.zeros(n)
clearance = np.zeros(n)
dribbled_past = np.zeros(n)
win_50_50 = np.zeros(n)
lost_50_50 = np.zeros(n)

def indice_player(player) :
    ind = 0
    while players[ind] != player :
        ind += 1
    return(ind)

for i in events_clearance.index :
    player = events_clearance["player_name"][i]
    ind = indice_player(player)
    if events_clearance["aerial_won"][i] == True :
        duel_win[ind] += 1
    else :
        clearance[ind] += 1
for i in events_duel.index :
    player = events_duel["player_name"][i]
    ind = indice_player(player)
    if events_duel["sub_type_name"][i] == "Aerial Lost" or events_duel["sub_type_name"][i] == "Lost" or events_duel["sub_type_name"][i] == "Lost In Play":
        duel_lost[ind] -= 1
    else :
        duel_win[ind] += 1
for i in events_block.index :
    player = events_block["player_name"][i]
    ind = indice_player(player)
    if events_block["block_offensive"][i] != True :
        block[ind] += 1
for i in events_dribbled_past.index :
    player = events_dribbled_past["player_name"][i]
    ind = indice_player(player)
    dribbled_past[ind] -= 1
for i in events_50_50.index :
    player = events_50_50["player_name"][i]
    ind = indice_player(player)
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


import matplotlib.pyplot as plt

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
plt.xlabel("Number of duels")
plt.ylabel("Players")
plt.xlim(min_x - 1,max_x + 1)
plt.title("Duels won and lost by each player")
plt.show()
plt.close()