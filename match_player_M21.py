#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:55:51 2023

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Arc
import seaborn as sns
from mplsoccer.pitch import Pitch, VerticalPitch
import tqdm
from matplotlib.animation import FuncAnimation, writers
from matplotlib.collections import LineCollection
import highlight_text
import matplotlib.font_manager
from IPython.core.display import HTML
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cmasher as cmr
from mplsoccer import VerticalPitch
from mplsoccer.utils import FontManager
from highlight_text import fig_text
from pywaffle import Waffle # PyWaffle Documentation --> https://buildmedia.readthedocs.org/media/pdf/pywaffle/latest/pywaffle.pdf
import matplotlib.pyplot as plt #Matplotlib pyplot to plot the charts
import matplotlib as mpl
from highlight_text import htext #used for highlighting the title
import matplotlib.font_manager as fm
from matplotlib import rcParams
from highlight_text import fig_text
from PIL import Image
import urllib
import os
from matplotlib.patches import FancyArrowPatch


#####################
### download data ###
#####################

df2 = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/M21/yb_sfc_1.csv")
df1 = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/event_match/23_24/M21/yb_sfc_1.csv")
#df3 = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/GPS/sfc_fcs_2.csv", sep=';')

df1.dropna(subset=['player_name'], inplace=True)


#################################################################################################################################

# Select players from Servette
servette_players = df1.loc[df1["team_name"] == "Servette FC M-21"]["player_name"].unique()

# Create a figure with subplots for each player
nrows = 3  # number of rows of subplots
ncols = 6  # number of columns of subplots
#fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 12))  # create figure object and axes

pitch = VerticalPitch(line_zorder=2,line_alpha=0.5, goal_alpha=0.3)
fig, axes = pitch.draw(nrows=nrows, ncols=ncols, figsize=(16, 12))


# Loop through the players and plot their ball receipt events
for i, player_name in enumerate(servette_players):
    # Select events for each player
    player = df1.loc[df1['player_name'] == player_name]
    playe = df2.loc[df2['player_name'] == player_name]

    # Select ball receipt events
    pos = player.loc[(player.event_type_name == "Ball Receipt*") |
                      (player.event_type_name == "Pass") |
                      (player.event_type_name == "Duel")]
    miss = player.loc[(player.event_type_name == "Miscontrol") |
                      (player.event_type_name == "Dispossessed")]

    # Plot ball receipt events
    pitch = VerticalPitch(line_zorder=2, line_color='black', linewidth=1, pitch_type='statsbomb')
    row = i // ncols  # calculate row index
    col = i % ncols  # calculate column index
    ax = axes[row, col]  # select subplot
    pitch.kdeplot(pos.location_x, pos.location_y, ax=ax, cmap='Blues', fill=True, levels=100)
    pitch.scatter(pos.location_x, pos.location_y, alpha=1, s=20, color="black", ax=ax)
    pitch.scatter(miss.location_x, miss.location_y, alpha=1, s=20, color="red", ax=ax)
    ax.set_title(player_name, fontsize=12, fontweight='bold')

# Add titles and axis labels to the figure
fig.suptitle("Ballon Touchés - Servette Players", fontsize=22, fontweight="bold")

# Adjust spacing between subplots
plt.subplots_adjust(hspace=0.5, wspace=0.3)

# Display the plot
plt.show()

###########################################################################################################################################

# Create a figure with subplots for each player
nrows = 3  # number of rows of subplots
ncols = 6  # number of columns of subplots
pitch = VerticalPitch(line_zorder=2,line_alpha=0.5, goal_alpha=0.3)
fig, axes = pitch.draw(nrows=nrows, ncols=ncols,figsize=(16, 12))

for i, player_name in enumerate(servette_players):
    mask = (df1['player_name'] == player_name) & (df1['team_name'] == "Servette FC M-21")
    df_player = df1.loc[mask, :]

    passes = df_player.loc[df_player['event_type_name'] == 'Pass'].set_index('id')

    mask_bronze = (df_player.event_type_name == 'Pass')
    df_pass = df_player.loc[mask_bronze, ['location_x', 'location_y', 'end_location_x', 'end_location_y']]
    mask_bronz = (df_player.event_type_name == 'Carries')
    df_carry = df_player.loc[mask_bronz, ['location_x', 'location_y', 'end_location_x', 'end_location_y']]
    mask_bron = (df_player.event_type_name == 'Dribble')
    df_dribble = df_player.loc[mask_bron, ['location_x', 'location_y']]

    pitch = VerticalPitch(line_color='black',linewidth=1)
    ax = axes.flatten()[i]
    
    for i, row in df_pass.iterrows():
        if row["end_location_x"] >= 0 and row["end_location_x"] <= 100 and \
            row["end_location_y"] >= 0 and row["end_location_y"] <= 80:
            color = "grey"
        else:
            color = "tan"
        pitch.arrows(row["location_x"], row["location_y"],
                    row["end_location_x"], row["end_location_y"],width=1.5,
                    headwidth=3, headlength=3, color=color, ax=ax)
   
    for i, row in df_carry.iterrows():
       if row["end_location_x"] >= 0 and row["end_location_x"] <= 100 and \
           row["end_location_y"] >= 0 and row["end_location_y"] <= 80:
           color = "black"
       else:
           color = "black"
       pitch.arrows(row["location_x"], row["location_y"],
                   row["end_location_x"], row["end_location_y"],width=1.5,
                   headwidth=3, headlength=3,linestyle='--',color=color, ax=ax)        
    
    pitch.scatter(df_dribble.location_x, df_dribble.location_y, alpha = 0.9, s = 30, color = "blue", ax=ax)
    #ax.text(5, 82,f"Noir - Passes | Gris - Carry | Bleu - Dribble - {player_name}", color = "black",fontweight = "bold", fontsize = 2)
    ax.axhline(y=80, xmin=0, xmax=100, color='grey', linestyle='--')
    ax.set_title(player_name, fontsize=12, fontweight='bold')

fig.suptitle("Passes Carries Dribbles", fontsize = 22, fontweight = "bold")
plt.show()

###############################################################################################################################################


df = df1[['timestamp','event_type_name',
         'possession_team_name','player_name','team_name',
         'location_x','location_y','outcome_name',
         'type_name','obv_total_net']]

pos = df.loc[(df1.event_type_name == "Carries") |
                      (df1.event_type_name == "Pass") |
                      (df1.event_type_name == "shot")]

pos = pos.loc[(pos.team_name == "Servette FC M-21")]

# group by player_name and sum obv_total_net
total_net = pos.groupby('player_name').agg({'obv_total_net': sum})

# calculate sum of negative and positive obv_total_net values for each player
neg_total_net = pos[pos.obv_total_net < 0].groupby('player_name').agg({'obv_total_net': sum})
pos_total_net = pos[pos.obv_total_net >= 0].groupby('player_name').agg({'obv_total_net': sum})

# merge the two DataFrames
total_net = pd.merge(neg_total_net, pos_total_net, on='player_name', how='outer', suffixes=('_neg', '_pos')).fillna(0)

# sort by the value of positive obv_total_net
total_net.sort_values(by='obv_total_net_pos', ascending=False, inplace=True)

# create a barplot
fig, ax = plt.subplots(figsize=(16, 9),facecolor = "white")
total_net.plot(kind='bar', ax=ax, color=['red', 'green'],ec="black",lw=1 ,width=0.8)


# set the title and axis labels
ax.set_title('Menace Joueurs', fontsize=22,fontweight = "bold" )
ax.set_xlabel('Player', fontsize=14).set(visible= False)
ax.set_ylabel('Niveau de Menance', fontsize=12, fontweight = "bold")
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)

plt.subplots_adjust(wspace=1)

# show the plot
plt.show()
