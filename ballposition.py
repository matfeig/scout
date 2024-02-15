#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 19:46:42 2022

@author: matfeig
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import seaborn as sns
import matplotlib.patches as mpatches
from colour import Color
import matplotlib.colors as mcolors
from highlight_text import fig_text


###############################
######### Event  ###########
###############################

data= pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/event_match/sfc_gc_1.csv")

df = data[['timestamp','period','event_type_name','possession_team_name','player_name',
           'location_x', 'location_y','end_location_x','end_location_y','duration','statsbomb_xg'
           ,'obv_for_net']]
df = df.iloc[4: , :]

df = df[(df['event_type_name'] =="Ball Receipt*")]
df = df[(df['period'] ==1)]

df['rollling'] = df.rolling(25).mean()['location_x']

X = df["timestamp"]
height = df["rollling"]

color = list(df['possession_team_name'])
colors = ['#870E26' if (x == 'Servette') else '#004292' for x in color ]

fig = plt.figure(figsize=(16, 9), dpi = 200, facecolor = "#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")
# Add spines
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)

# Add grid and axis labels
ax.grid(True, color = "lightgrey", ls = ":")
ax.set_ylabel("Position du ballon")
ax.scatter(
	X,
    height, 
    #ec = "blac, 
    #lw = .75, 
    color = colors, 
    #zorder = 3, 
    #width = 0.75
    )
# Annotate the ratio
# for index, y in enumerate(height):
#     ax.annotate(
#         xy = (index, y),
#         text = f"{y:}",
#         xytext = (0, 7),
#         textcoords = "offset points",
#         size = 9,
#         color = "black",
#         ha = "center",
#         va = "center",
#         weight = "bold"
#     )
# Adjust ticks
ax.tick_params(axis = "x", rotation = 90)
plt.title ('Position du ballon', fontsize=20,fontweight = "bold")
