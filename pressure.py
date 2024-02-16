#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 10:33:03 2023

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mplsoccer.pitch import Pitch, VerticalPitch
from highlight_text import fig_text

df1 = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/event_match/fcw_sfc_2.csv")

df1 = df1[['timestamp', 'period','minute','second','event_type_name',
         'possession',
         'possession_team_name','player_name','team_name',
         'location_x','location_y','duration','counterpress','outcome_name',
         'type_name']]

df1 = df1.loc[(df1.team_name =='Servette')]


poss = df1.loc[(df1.event_type_name == "Pressure")]
# filter pressure events where counterpress is True
poss_counterpress = poss.loc[poss['counterpress'] == True]

# plot the pitch and the scatter plot of pressure events in black and counterpress events in red



pitch = Pitch(line_zorder=2, line_color='black',linewidth=1)
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#pitch.kdeplot(pos.location_x, pos.location_y, ax=ax['pitch'], cmap='Blues', fill=True, levels=100,)
pitch.scatter(poss.location_x, poss.location_y, alpha = 1, s=50, color = "black", ax=ax['pitch'])
pitch.scatter(poss_counterpress.location_x, poss_counterpress.location_y, alpha=1, s=50, color="red", ax=ax['pitch'])
fig_text(0.07,0.04,"Red counter press", color = "black",fontweight = "bold", fontsize = 12,backgroundcolor='white')
fig.suptitle("Pressure - SFC", fontsize = 26, fontweight = "bold", color = "black")
plt.show()
