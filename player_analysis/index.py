#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 16:07:23 2022

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

#load data
data = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/sfc_slo_2.csv")
#data = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/M21/rapper_sfc_1.csv")

data.columns = data.columns.map(lambda x: x.removeprefix("player_match_"))
data = data.replace(np.nan,0)

data.head()
describe = data.describe()

data['index'] = ((data['np_shots']*4)+(data['np_xg']*9)+(data['xa']*8)+
                 (data['op_key_passes']*4)+(data['through_balls']*6)+(data['op_passes_into_box']*6)+
                 data['touches_inside_box']*5+(data['dribbles']*4)+
                 (data['forward_passes']*1)+(data['op_f3_forward_passes']*5)+(data['successful_crosses']*3)+
                 (data['passes_inside_box']*3)+(data['obv_pass']*8)+(data['obv_shot']*8)+ (data['deep_progressions']*7)+
                 (data['obv_dribble_carry']*7)+(data['np_psxg']*9)+(data['dispossessions']*(-2))+
                 (data['successful_long_balls']*4)+(data['turnovers']*(-8))+(data['touches']*0.5))

df = data[['team_name','player_name','index']]
df['index'] = df['index'].astype(int)
df.sort_values("index",axis = 0, ascending=False, inplace=True)
X = df["player_name"]
height = df["index"]

color = list(df['team_name'])
colors = ['#870E26' if (x == 'Servette') else '#004292' for x in color ]
#colors = ['#870E26' if (x == 'Servette FC M-21') else '#004292' for x in color ]

fig = plt.figure(figsize=(16, 9), dpi = 200, facecolor = "#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")
# Add spines
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)

# Add grid and axis labels
ax.grid(True, color = "lightgrey", ls = ":")
ax.set_ylabel("Index")
ax.bar(
	X, 
    height, 
    ec = "black", 
    lw = .75, 
    color = colors, 
    zorder = 3, 
    width = 0.75)
# Annotate the ratio
for index, y in enumerate(height):
    ax.annotate(
        xy = (index, y),
        text = f"{y:}",
        xytext = (0, 7),
        textcoords = "offset points",
        size = 9,
        color = "black",
        ha = "center",
        va = "center",
        weight = "bold"
    )
# Adjust ticks
ax.tick_params(axis = "x", rotation = 90)
plt.title ('Index Offensif - SFC vs SLO ', fontsize=20,fontweight = "bold")

###############################
###### out of possession#######
###############################

data['indexDef'] = ((data['tackles']*6)+(data['interceptions']*6)-(data['dribbled_past']*(-6))+
                 (data['shots_blocked']*4)+(data['clearances']*4)+(data['successful_aerials']*8)+(((data['aerials'])-(data['successful_aerials']))*(-7))+
                 (data['aggressive_actions']*7)+(data['pressure_regains']*9)+
                 (data['pressures']*8)+(data['pressure_duration_total']*6)+
                 (data['counterpressures']*7)+(data['pressured_action_fails']*(-3))+
                 (data['counterpressured_action_fails']*(-2))+(data['pressure_duration_total']*6)+
                 (data['ball_recoveries']*8)+
                 (data['fhalf_ball_recoveries']*5)+
                 (data['obv_defensive_action']*7))


df = data[['team_name','player_name','indexDef']]
df['indexDef'] = df['indexDef'].astype(int)
df.sort_values("indexDef",axis = 0, ascending=False, inplace=True)
X = df["player_name"]
height = df["indexDef"]

color = list(df['team_name'])
colors = ['#870E26' if (x == 'Servette') else '#004292' for x in color ]
#colors = ['#870E26' if (x == 'Servette FC M-21') else '#004292' for x in color ]

fig = plt.figure(figsize=(16, 9), dpi = 200, facecolor = "#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")
# Add spines
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)

# Add grid and axis labels
ax.grid(True, color = "lightgrey", ls = ":")
ax.set_ylabel("Index")
ax.bar(
	X, 
    height, 
    ec = "black", 
    lw = .75, 
    color = colors, 
    zorder = 3, 
    width = 0.75)
# Annotate the ratio
for index, y in enumerate(height):
    ax.annotate(
        xy = (index, y),
        text = f"{y:}",
        xytext = (0, 7),
        textcoords = "offset points",
        size = 9,
        color = "black",
        ha = "center",
        va = "center",
        weight = "bold"
    )
# Adjust ticks
ax.tick_params(axis = "x", rotation = 90)
plt.title ('Index Défensif - SFC  vs SLO', fontsize=20,fontweight = "bold")

###############################
######        Total     #######
###############################

data['Index_G']= data['index']+data['indexDef']

df = data[['team_name','player_name','Index_G']]
df['Index_G'] = df['Index_G'].astype(int)
df.sort_values("Index_G",axis = 0, ascending=False, inplace=True)
X = df["player_name"]
height = df["Index_G"]

color = list(df['team_name'])
colors = ['#870E26' if (x == 'Servette') else '#004292' for x in color ]

fig = plt.figure(figsize=(16, 9), dpi = 200, facecolor = "#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")
# Add spines
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)
# Add grid and axis labels
ax.grid(True, color = "lightgrey", ls = ":")
ax.set_ylabel("Index_G")
ax.bar(
	X, 
    height, 
    ec = "black", 
    lw = .75, 
    color = colors, 
    zorder = 3, 
    width = 0.75)
# Annotate the ratio
for index, y in enumerate(height):
    ax.annotate(
        xy = (index, y),
        text = f"{y:}",
        xytext = (0, 7),
        textcoords = "offset points",
        size = 9,
        color = "black",
        ha = "center",
        va = "center",
        weight = "bold"
    )
# Adjust ticks
ax.tick_params(axis = "x", rotation = 90)
plt.title ('Index Total - SFC vs FCZ', fontsize=20,fontweight = "bold")

###############################
#### Adjusted Possession  #####
###############################



###############################
######     Per 90   #########
###############################


minutes.rename(columns = {'Name':'Player'}, inplace = True)
data1 = pd.merge(data, minutes)
data1 = pd.merge(data, minutes, left_on='Player', right_on='Player')

data1['Index_ind']= data1['index']/data1['Minutes']*100

df = data1[['teamName','Player','Index_ind']]
df['Index_ind'] = df['Index_ind'].astype(int)
df.sort_values("Index_ind",axis = 0, ascending=False, inplace=True)
X = df["Player"]
height = df["Index_ind"]

color = list(df['teamName'])
colors = ['#870E26' if (x == 'Servette') else '#004292' for x in color ]

fig = plt.figure(figsize=(16, 9), dpi = 200, facecolor = "#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")
# Add spines
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)
# Add grid and axis labels
ax.grid(True, color = "lightgrey", ls = ":")
ax.set_ylabel("Index_ind")
ax.bar(
 	X, 
    height, 
    ec = "black", 
    lw = .75, 
    color = colors, 
    zorder = 3, 
    width = 0.75)
# Annotate the ratio
for index, y in enumerate(height):
    ax.annotate(
        xy = (index, y),
        text = f"{y:}",
        xytext = (0, 7),
        textcoords = "offset points",
        size = 9,
        color = "black",
        ha = "center",
        va = "center",
        weight = "bold"
    )
# Adjust ticks
ax.tick_params(axis = "x", rotation = 90)
plt.title ('Index Indiv - SFC vs St. Gall', fontsize=20,fontweight = "bold")


###############################
######### KPI match ###########
###############################

df_sfc = data.loc[(data.team_name == "Servette")]
df_sfc = df_sfc[['team_name','player_name','op_passes_into_box','obv','obv_dribble_carry', 'obv_shot', 'obv_defensive_action',
                 'deep_progressions']]
df_sfc['op_passes_into_box'].sum()
df_sfc['obv'].sum()
df_sfc['obv_dribble_carry'].sum()
df_sfc['obv_shot'].sum()
df_sfc['obv_defensive_action'].sum()
df_sfc['deep_progressions'].sum()




