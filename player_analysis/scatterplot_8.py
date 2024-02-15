#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:30:26 2021

@author: matfeig
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.pyplot import figure

df = pd.read_csv('df.csv')
del df['Unnamed: 0']

#Name = df[['Name', 'xG', 'PSxG']]

## Changer le nom d'une column 
# df.columns = df.columns.str.replace('Non-Penalty Goals', 'Goals')


# Set font and background colour
plt.rcParams.update({'font.family':'Avenir'})
bgcol = '#fafafa'

df = df.loc[(df.primary_position == "Centre Attacking Midfielder")|(df.primary_position == "Left Attacking Midfielder")|(df.primary_position == "Right Attacking Midfielder")|
                  (df.secondary_position == "Centre Attacking Midfielder")|(df.secondary_position == "Left Attacking Midfielder")|(df.secondary_position == "Right Attacking Midfielder")|
                  (df.primary_position == "Centre Midfielder")|(df.primary_position == "Left Centre Midfielder")|(df.primary_position == "Right Centre Midfielder")|
                  (df.secondary_position == "Centre Midfielder")|(df.secondary_position == "Left Centre Midfielder")|(df.secondary_position == "Right Centre Midfielder")]
df = df.loc[(df.season_name == "2022/2023")]


##Choisir les variables 
df=df.loc[(df.player_season_minutes>=300)]


##Slect Comptetion
#df = df[(df.competion_name != "Challenge League") & (df.competion_name != "Super League")]

##Select team
# df = df[(df.team_name != "FC Porto") & (df.team_name!= "Sporting Braga")]

##Filtrer valeur xG
# df= df[df.minutes < 900]
# df1 = df[df.xG > 0.3]
# df2 = df1[df.TB >2]
# df3 = df2[df.pshot > 0.20]
# df4 = df3[df.aerwinper > 0.010]
# df5 = df4[df.perf < 0.0]
# df6 = df5[df.Age > 22]

# xG et goal
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_np_xg_90'], df['player_season_goals_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Timothé Cognat' :
    ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Alexis Antunes' :
    ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Otar Kiteishvili' :
     ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Lance Duijvestijn' :
    ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Okan Aydın' :
     ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Youssef Maziz' :
     ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Tomislav Mrkonjić' :
    ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Sandi Ogrinec' :
     ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Julien Maggiotti' :
     ax.annotate(txt, (df.player_season_np_xg_90.iat[i]+0.01, df.player_season_goals_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.xlabel("xG",fontsize = 12, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("Goals",fontsize = 12, fontweight = "bold", color = "black")
plt.title("Expected Goals vs Goals",fontsize = 20, fontweight = "bold", color = "black", pad=15)
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()


## pressing et intercpetipn 

fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_pressures_90'], df['player_season_padj_tackles_and_interceptions_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Timothé Cognat' :
    ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Alexis Antunes' :
    ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Otar Kiteishvili' :
     ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Lance Duijvestijn' :
    ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Okan Aydın' :
     ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Youssef Maziz' :
     ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Tomislav Mrkonjić' :
    ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Sandi Ogrinec' :
     ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Julien Maggiotti' :
     ax.annotate(txt, (df.player_season_pressures_90.iat[i]+0.01, df.player_season_padj_tackles_and_interceptions_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.xlabel("Pressing",fontsize = 12, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("Def & Interceptions",fontsize = 12, fontweight = "bold", color = "black")
plt.title("Pressing vs Interceptions",fontsize = 20, fontweight = "bold", color = "black", pad=15)
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()

### Progression et enace 
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_deep_progressions_90'], df['player_season_obv_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Timothé Cognat' :
    ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Alexis Antunes' :
    ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Otar Kiteishvili' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Lance Duijvestijn' :
    ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Okan Aydın' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Youssef Maziz' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Tomislav Mrkonjić' :
    ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Sandi Ogrinec' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Julien Maggiotti' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.xlabel("Deep Progressions",fontsize = 12, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("OBV",fontsize = 12, fontweight = "bold", color = "black")
plt.title("Progression vs menace",fontsize = 20, fontweight = "bold", color = "black", pad=15)
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()



