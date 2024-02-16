#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:30:56 2023

@author: matfeig
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mplsoccer.pitch import Pitch, VerticalPitch
from highlight_text import fig_text

df1 = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/event_match/fcb_sfc_3.csv")

df1 = df1[['timestamp', 'period','minute','second','event_type_name',
         'possession',
         'possession_team_name','player_name','team_name',
         'location_x','location_y','duration','outcome_name',
         'type_name']]

df1 = df1.loc[(df1.team_name =='Servette')]


pos = df1.loc[(df1.outcome_name == "Incomplete")]
pos = pos.loc[(pos.event_type_name == "Pass")]
miss = df1.loc[(df1.event_type_name == "Miscontrol")|(df1.event_type_name == "Dispossessed")|(df1.event_type_name == "Turnover")]


pitch = Pitch(line_zorder=2, line_color='black',linewidth=1)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#pitch.kdeplot(pos.location_x, pos.location_y, ax=ax['pitch'], cmap='Blues', fill=True, levels=100,)
pitch.scatter(pos.location_x, pos.location_y, alpha = 1, s=50, color = "black", ax=ax['pitch'])
pitch.scatter(miss.location_x, miss.location_y, alpha = 1, s=50, color = "red", ax=ax['pitch'])
fig_text(0.07,0.04,"Rouge - Control manqué et ballon perdu dans les pieds | Black - Pass or ball receipt Incomplete", color = "black",fontweight = "bold", fontsize = 12,backgroundcolor='white')
fig.suptitle("Ballons Perdus - SFC", fontsize = 26, fontweight = "bold", color = "black")
plt.show()














##pour chaque player 

# names = df1['player_name'].unique()
# for name in names:
#      player = df1.loc[df1['player_name'] == name]


#      pos = df1.loc[(df1.outcome_name == "Incomplete")]
#      pos = pos.loc[(pos.event_type_name == "Pass")]
#      miss = df1.loc[(df1.event_type_name == "Miscontrol")|(df1.event_type_name == "Dispossessed")]

#      pitch = VerticalPitch(line_zorder=2, line_color='black', linewidth=1)
#      fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
#      pitch.kdeplot(pos.location_x, pos.location_y, ax=ax['pitch'], cmap='Blues', fill=True, levels=100,)
#      pitch.scatter(pos.location_x, pos.location_y, alpha = 1, s=50, color = "black", ax=ax['pitch'])
#      pitch.scatter(miss.location_x, miss.location_y, alpha = 1, s=50, color = "red", ax=ax['pitch'])
#      fig_text(0.07,0.04,f"Rouge - Ballon perdu - {name}", color = "black",fontweight = "bold", fontsize = 12,backgroundcolor='white')
#      fig.suptitle("Ballons Perdus ", fontsize = 26, fontweight = "bold", color = "black")
#      #fig.savefig(f'/Users/matfeig/Desktop/{name}.png')
#      plt.show()
