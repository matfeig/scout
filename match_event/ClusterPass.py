#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:44:06 2021

@author: matfeig
"""
#https://medium.com/analytics-vidhya/tutorial-pass-clustering-with-python-through-the-example-of-france-belgium-2018-world-cup-edc16a2f5bb8

import json
import pandas as pd
import sklearn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

with open('open-data-master/data/matches/43/3.json') as f:
  data = json.load(f)
with open('open-data-master/data/events/8655.json') as f:
  data_events = json.load(f)
  
id_team_1 = 771 
id_team_2 = 782
start_location_x_team_1 = []
end_location_x_team_1 = []
start_location_y_team_1 = []
end_location_y_team_1 = []
start_location_x_team_2 = []
end_location_x_team_2 = []
start_location_y_team_2 = []
end_location_y_team_2 = []
player_team_1 = []
player_team_2 = []
recipient_team_1 = []
recipient_team_2 = []

for event in data_events :
    if event['type']['name'] == 'Pass' and event['team']['id'] ==    id_team_1 :
        start_location_x_team_1.append(event['location'][0])
        start_location_y_team_1.append(event['location'][1])
        end_location_x_team_1.append(event['pass']['end_location'][0])
        end_location_y_team_1.append(event['pass']['end_location'][1])
        player_team_1.append(event['player']['name'])
        
        try :
            recipient_team_1.append(event['pass']['recipient']['name'])
        except :
            recipient_team_1.append('no recipient')
        
    if event['type']['name'] == 'Pass' and event['team']['id'] == id_team_2 :
        start_location_x_team_2.append(event['location'][0])
        start_location_y_team_2.append(event['location'][1])
        end_location_x_team_2.append(event['pass']['end_location'][0])
        end_location_y_team_2.append(event['pass']['end_location'][1])
        player_team_2.append(event['player']['name'])
        
        try :
            recipient_team_2.append(event['pass']['recipient']['name'])
        except :
            recipient_team_2.append('no recipient')
pass_team_1 = pd.DataFrame()
pass_team_1['start_x'] = start_location_x_team_1
pass_team_1['start_y'] = start_location_y_team_1
pass_team_1['end_x'] = end_location_x_team_1
pass_team_1['end_y'] = end_location_y_team_1
pass_team_1['player'] = player_team_1
pass_team_1['recipient'] = recipient_team_1
pass_team_2 = pd.DataFrame()
pass_team_2['start_x'] = start_location_x_team_2
pass_team_2['start_y'] = start_location_y_team_2
pass_team_2['end_x'] = end_location_x_team_2
pass_team_2['end_y'] = end_location_y_team_2
pass_team_2['player'] = player_team_2
pass_team_2['recipient'] = recipient_team_2

N_clusters = 5
X_1 = np.array(pass_team_1[['start_x', 'start_y', 'end_x', 'end_y']])
X_2 = np.array(pass_team_2[['start_x', 'start_y', 'end_x', 'end_y']])
kmeans = KMeans(n_clusters = N_clusters, random_state = 0).fit(X_1)
cluster_labels = kmeans.predict(X_1)
pass_team_1['n_cluster'] = cluster_labels
centroids_1 = pd.DataFrame(data = kmeans.cluster_centers_, columns = ['start_x', 'start_y', 'end_x', 'end_y'])
kmeans = KMeans(n_clusters = N_clusters, random_state = 0).fit(X_2)
cluster_labels = kmeans.predict(X_2)
pass_team_2['n_cluster'] = cluster_labels
centroids_2 = pd.DataFrame(data = kmeans.cluster_centers_, columns = ['start_x', 'start_y', 'end_x', 'end_y'])


from mplsoccer.pitch import Pitch
from mplsoccer.statsbomb import read_event, EVENT_SLUG
from matplotlib import rcParams
pitch = Pitch(pitch_type='statsbomb',
              pitch_color='#22312b', line_color='#c7d5cc', figsize=(10,7),
              constrained_layout=False, tight_layout=False)
fig, ax = pitch.draw()
lc1 = pitch.lines(centroids_1['start_x'], centroids_1['start_y'],
                  centroids_1['end_x'], centroids_1['end_y'],
                  lw=5, transparent=True, comet=True, label='France passes',
                  color='#ad993c', ax=ax)
lc2 = pitch.lines(centroids_2['start_x'], centroids_2['start_y'],
                  centroids_2['end_x'], centroids_2['end_y'],
                  lw=5, transparent=True, comet=True, label='Belgium passes',
                  color='#ba4f45', ax=ax)
# Plot the legend
ax.legend(facecolor='#22312b', edgecolor='None', fontsize=8, loc='upper left', handlelength=4)
# Set the title
ax.set_title(f'20 Main passes France vs Belgium, World Cup 2018 Semifinal ', fontsize=10)
# Set the figure facecolor
fig.set_facecolor('#22312b')
                  
   
for c in sorted(pass_team_1['n_cluster'].unique()) :
    
    pitch = Pitch(pitch_type='statsbomb', orientation='vertical',
              pitch_color='#22312b', line_color='#c7d5cc', figsize=(16, 11),
              constrained_layout=False, tight_layout=False)
    
    fig, ax = pitch.draw()
lc1 = pitch.lines(pass_team_1[pass_team_1['n_cluster'] == c]['start_x'], 
                      pass_team_1[pass_team_1['n_cluster'] == c]['start_y'],
                      pass_team_1[pass_team_1['n_cluster'] == c]['end_x'],
                      pass_team_1[pass_team_1['n_cluster'] == c]['end_y'],
                      lw=5, transparent=True, comet=True, label='France passes',
                      color='#ad993c', ax=ax)
# Plot the legend
ax.legend(facecolor='#22312b', edgecolor='None', fontsize=15, loc='upper left', handlelength=3)
# Set the title
ax.set_title(f'Cluster passes France vs Belgium, World Cup 2018 Semifinal ', fontsize=10)
# Set the figure facecolor
fig.set_facecolor('#22312b')
    
dic_pass_players = {}
for player in pass_team_1[pass_team_1['n_cluster'] == c]['player'].unique() :
     dic_pass_players[player] = sum(pass_team_1[pass_team_1['n_cluster'] == c]['player'] == player)
    
sort_pass_players = sorted(dic_pass_players.items(), key=lambda x: x[1], reverse=True)
sort_dic_pass_players = {}
for i in range(len(sort_pass_players)) :
    sort_dic_pass_players[sort_pass_players[i][0]] = sort_pass_players[i][1]
i=0
for p in list(sort_dic_pass_players.keys()) :
    plt.text(52, 117-i, p + ' ' + str(sort_dic_pass_players[p]), bbox=dict(facecolor='#22312b', edgecolor='None', alpha=0.5))
i+=3
                  
                  