#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:08:59 2021

@author: matfeig
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import seaborn as sns
from mplsoccer.pitch import Pitch
from mplsoccer.statsbomb import read_event, EVENT_SLUG
from matplotlib import rcParams


pitch = Pitch(pitch_color='lightgrey', line_color='white', stripe=False, axis=False, label=False, tick=False)
fig, ax = pitch.draw()


defdata = pd.read_csv("sfc_vadbomb.csv")
defdata.head()
defdata.dropna(subset=['location_x'], inplace = True)
defdata.dropna(subset=['end_location_x'], inplace = True)

#defdata['lengthPass'] = defdata['location_x'] - defdata['location_y']

Team = defdata.loc[(defdata.team_name == "Servette")]

print (type("location_x"))
#defdata['location_x'].dtypes

### Plot
fig, ax = pitch.draw()

for index,row in Team.iterrows():
    plt.plot([row["location_x"],row["end_location_x"]],
             [row["location_y"],row["end_location_y"]], 
             color="blue")

#for i in range(len(Team)):
#    plt.plot([Team["location_x"][i],Team["end_location_x"][i]],
#             [Team["location_y"][i],Team["end_location_y"][i]], 
#             color="blue")
    
sports = defdata["event_type_name"].unique() 
print(sports)

####                              ####
#### Plot Arrow Passes or Carries ####
####                              ####

Player = Team.loc[(Team.player_name == "Gaël Ondoua")]
#Pattern = Player.loc[(Player.play_pattern_name == "Regular Play")]
Action = Player.loc[(Player.event_type_name == "Pass")]#|(Player.event_type_name == "Carries")]

fig, ax = pitch.draw()

for index,row in Action.iterrows():
 #   if location_x =! 0 or 120 
    #plt.arrow([row["location_x"],row["end_location_x"]], [row["location_y"],row["end_location_y"]]) 
    plt.plot([row["location_x"],row["end_location_x"]],
             [row["location_y"],row["end_location_y"]],
             color="blue") #linestyle='--'
    plt.plot(row["location_x"],row["location_y"],"o", color="blue")
    plt.title("Pass Map - Gaël Ondoua - SFC vs. Vaduz")
    #sns.kdeplot(Player["location_x"],Player["location_y"], shade="True", shade_lowest= False,n_levels=5, alpha= 0.5)
  
############################
############################
    
#Bar##   
fig, ax =plt.subplots()
ax.bar(Pattern["event_type_name"],Pattern.index)
plt.show()   


#######
#######
#######
#######

team1, team2 = defdata.team_name.unique()
playername = defdata.player_name.unique()
mask_team1 = (defdata.event_type_name == 'Pass') & (defdata.team_name == team1)

df_pass = defdata.loc[mask_team1, ['player_name','location_x', 'location_y', 'end_location_x', 'end_location_y', 'outcome_name']]
df_pass = defdata.loc[(defdata['player_id'] == 28967)]
mask_complete = df_pass.outcome_name.isnull()
df_pass.head()


# Setup the pitch
pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', figsize=(16, 11),
              constrained_layout=False, tight_layout=True)
fig, ax = pitch.draw()

# Plot the completed passes
lc1 = pitch.lines(df_pass[mask_complete].location_x, df_pass[mask_complete].location_y,
                  df_pass[mask_complete].end_location_x, df_pass[mask_complete].end_location_y,
                  lw=10, transparent=True, comet=True, label='Passes Réussies',
                  color='royalblue', ax=ax)

# Plot the other passes
lc2 = pitch.lines(df_pass[~mask_complete].location_x, df_pass[~mask_complete].location_y,
                  df_pass[~mask_complete].end_location_x, df_pass[~mask_complete].end_location_y,
                  lw=3, transparent=True, comet=True, label='Passes Manquées',
                  color='slategrey', ax=ax)

# Plot the legend
ax.legend(edgecolor='None', fontsize=12, loc='upper left', handlelength=1)
ax.set_title(f'{team1} vs {team2}', fontsize=15)
#fig.set_facecolor('#22312b'

## Calculate progressive Passes ####  


