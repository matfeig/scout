#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:58:11 2021
@author: matfeig
"""
#https://fcpython.com/visualisation/football-heatmaps-seaborn
#https://fcpython.com/blog/creating-personal-football-heatmaps

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import seaborn as sns
from mplsoccer.pitch import Pitch
import tqdm
from matplotlib.animation import FuncAnimation, writers
from matplotlib.collections import LineCollection
import pandas as pd
import PIL
from urllib.request import urlopen
from urllib.request import Request, urlopen
import requests
from mplsoccer.statsbomb import EVENT_SLUG, read_event



pitch = Pitch(positional=True, shade_middle=True, positional_color='#eadddd', shade_color='#f2f2f2')
fig, ax = pitch.draw()

#matplotlib inline
data = pd.read_csv("sfc_fcs_2.csv")
# df2 = pd.read_csv("sfc_ls.csv")
# df3 = pd.read_csv("fcz_sfc.csv")

# data = pd.concat([df1, df2, df3], ignore_index=True)


data.dropna(subset=['location_x'], inplace = True)
data.head()

sns.countplot(x="event_type_name",data=data)
plt.xticks(rotation= 90)

#Nopmbre de passe par joueurs


#### Niveau #####
fig, ax = plt.subplots()
fig.set_size_inches(7, 5)
sns.kdeplot(data["location_x"],data["location_y"])
plt.show()



#### Heat Map & Niveau ######
fig, ax = plt.subplots()
fig.set_size_inches(14,4)
########Plot one - include shade
plt.subplot(121)
sns.kdeplot(data["location_x"],data["location_y"], shade="True")
#########Plot two - no shade, lines only
plt.subplot(122)
sns.kdeplot(data["location_x"],data["location_y"])
plt.show()



### Heat Map Autres###
fig, ax = plt.subplots()
fig.set_size_inches(14,4)
#########Plot One - distinct areas with few lines
plt.subplot(121)
sns.kdeplot(data["location_x"],data["location_y"], shade="True", n_levels=5)
#########Plot Two - fade lines with more of them
plt.subplot(122)
sns.kdeplot(data["location_x"],data["location_y"], shade="True", n_levels=40)

plt.show()



#####Display Pitch ######
Team = data.loc[(data.team_name == "Servette")]
Type = Team.loc[(Team.play_pattern_name == "Regular Play")]
Action = Type.loc[(Type.event_type_name == "Pass")|(Type.event_type_name == "Carries")]
#Action = Type.loc[(Type.event_type_name == "Carries")]

fig, ax = pitch.draw()
sns.kdeplot(Action["location_x"],Action["location_y"], shade="True",n_levels=5, alpha= 0.5)
plt.show()


#####Display a single player ######
player = data.loc[(data['player_id'] == 23779)]
player = player.loc[(player.event_type_name == "Ball Receipt*")|(player.event_type_name == "Ball Recovery")|(player.event_type_name == "Interception")]
defpoints = player[['location_x', 'location_y']].values
defpoints
fig, ax = pitch.draw()
sns.kdeplot(player["location_x"],player["location_y"], shade="True",n_levels=5, alpha= 0.3)
sns.scatterplot(player["location_x"],player["location_y"],size=1, edgecolor='black', facecolor='black', legend='')
plt.title("Bedia- Ball receipt")
plt.show()



### ALL player in a tema ###
Team = data.loc[(data.team_name == "Servette")]
Team.head()
players = Team["player_id"].unique()
players = players[~np.isnan(players)]
print (players)

#For each player in our players variable
for player_id in players:
    fig, ax = pitch.draw() 
    ax.legend(players[players['player_id'==player_id]]['player_name'].iloc[0])
    #Create a new dataframe for the player
    df = Team[(Team.player_id == player_id)]
    #Create an array of the x/y coordinate groups
    #points = df[['location_x', 'location_y']].values
    sns.kdeplot(df["location_x"],df["location_y"], shade="True", shade_lowest= False,n_levels=5, alpha= 0.5)
#Once all of the individual hulls have been created, plot them together
plt.show()
















