#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 13:41:10 2023

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch
from highlight_text import fig_text


### download data ###
df = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/event_match/23_24/fcb_sfc_1.csv")
df['event_type_name'].value_counts()

#get team names
team1, team2 = df.team_name.unique()
#A dataframe of shots
shots = df.loc[df['event_type_name'] == 'Shot'].set_index('id')

########
########
########

#create pitch
pitch = Pitch(line_color='black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#query
mask_servette = (df.event_type_name == 'Shot') & (df.team_name == team1)
#finding rows in the df and keeping only necessary columns
df_servette = df.loc[mask_servette, ['location_x', 'location_y', 'outcome_name', "player_name", "statsbomb_xg"]]

#plot them - if shot ended with Goal - alpha 1 and add name
#for Servette
for i, row in df_servette.iterrows():
    if row["outcome_name"] == 'Goal':
    #make circle
       pitch.scatter(row.location_x, row.location_y, alpha = 1, s=500*np.sqrt(row.statsbomb_xg), color = "black", ax=ax['pitch'])
       pitch.annotate(row["player_name"], (row.location_x + 1, row.location_y - 2), ax=ax['pitch'], fontsize = 12)
    else:
       pitch.scatter(row.location_x, row.location_y, alpha = 0.2, s=500*np.sqrt(row.statsbomb_xg), color = "grey", ax=ax['pitch'])

mask_sweden = (df.event_type_name == 'Shot') & (df.team_name == team2)
df_sweden = df.loc[mask_sweden, ['location_x', 'location_y', 'outcome_name', "player_name"]]

#for Opponent
for i, row in df_sweden.iterrows():
    if row["outcome_name"] == 'Goal':
        pitch.scatter(120 - row.location_x, 80 - row.location_y, alpha = 1, s=100, color = "black", ax=ax['pitch'])
        pitch.annotate(row["player_name"], (120 - row.location_x + 1, 80 - row.location_y - 2), ax=ax['pitch'], fontsize = 12)
    else:
        pitch.scatter(120 - row.location_x, 80 - row.location_y, alpha = 0.2, s=100, color = "#870E26", ax=ax['pitch'])

fig.suptitle("FCB- SFC", fontsize = 30, fontweight = "bold", color = "black")
plt.show()


####################################
####### Servette Attaquants  #######
####################################


pitch = VerticalPitch(line_color='black', half = True)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

for i, row in df_servette.iterrows():
    if row["player_name"] == 'Dereck Germano Kutesa':
    #make circle
       pitch.scatter(row.location_x, row.location_y, alpha = 1, s=700*np.sqrt(row.statsbomb_xg), color = "black", ax=ax['pitch'])
       #pitch.annotate(row["player_name"], (row.location_x + 1, row.location_y - 2), ax=ax['pitch'], fontsize = 12)
    if row["player_name"] == 'Miroslav Stevanović':
       #make circle
       pitch.scatter(row.location_x, row.location_y, alpha = 1, s=700*np.sqrt(row.statsbomb_xg), color = "grey", ax=ax['pitch'])
       #pitch.annotate(row[" "], (row.location_x + 1, row.location_y - 2), ax=ax['pitch'], fontsize = 12)
    if row["player_name"] == 'Chris Vianney Bedia':
          #make circle
       pitch.scatter(row.location_x, row.location_y, alpha = 1, s=700*np.sqrt(row.statsbomb_xg), color = "darkblue", ax=ax['pitch'])
       #pitch.annotate(row[" "], (row.location_x + 1, row.location_y - 2), ax=ax['pitch'], fontsize = 12)
    else:
       pitch.scatter(row.location_x, row.location_y, alpha = 0.2, s=700*np.sqrt(row.statsbomb_xg), color = "#870E26", ax=ax['pitch'])

fig.suptitle("Servette Fc - Attaquants", fontsize = 30, fontweight = "bold", color = "black")
plt.show()


