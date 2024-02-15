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

df= df.loc[(df.primary_position == "Left Back")|(df.primary_position == "Right Back")|(df.primary_position == "Right Wing Back")|
           (df.secondary_position == "Left Back")|(df.secondary_position == "Right Back")|
           (df.primary_position == "Left Wing Back")]

df = df.loc[(df.season_name == "2022/2023")]

##Choisir les variables 
df=df.loc[(df.player_season_minutes>=400)]


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

##Savefilter
# #df6.to_csv('striker_select.csv', index=False)
# fig = plt.figure()
# figure(figsize=(16, 9), dpi=80)
# ax = plt.hist(df['player_season_np_xg_90'], rwidth=0.8)
# plt.xlabel('xG', fontsize=20)
# plt.ylabel('Frequence', fontsize=20)
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# ax.get_legend().remove()
# plt.show()


# ## Selectionner les leagues
# data = df.loc[(df.competition_name == "Super League")]
# df_sorted = data.sort_values('player_season_np_xg_90', ascending=False)
# df_sorted_perf = data.sort_values('player_season_over_under_performance_90', ascending=False)


# fig = plt.figure()
# figure(figsize=(16, 9), dpi=80)
# ax = df_sorted_perf.plot.bar(x='player_name', y='player_season_over_under_performance_90',fontsize=4,rot=90)
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
# ax.get_legend().remove()
# plt.show()

# Deep progres et goal
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_padj_tackles_and_interceptions_90'], df['player_season_obv_defensive_action_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Gaël Clichy' :
    ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Moustapha Seck' :
    ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Abdallah N"Dour' :
     ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.1, df.player_season_obv_defensive_action_90.iat[i]+.1), size = 10,backgroundcolor="w")
   if txt == 'Mateus Quaresma Correia' :
    ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Kylian Kaïboué' :
     ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Jonas Antonius Auer' :
     ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Maximiliano Moreira Romero' :
     ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Christian Neiva Afonso' :
     ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Amir Absalem' :
     ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Boy Kemper' :
     ax.annotate(txt, (df.player_season_padj_tackles_and_interceptions_90.iat[i]+0.01, df.player_season_obv_defensive_action_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Moussa Diallo' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.xlabel("player_season_padj_tackles_and_interceptions_90",fontsize = 12, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("player_season_obv_defensive_action_90",fontsize = 12, fontweight = "bold", color = "black")
plt.title("Actions Defensives ",fontsize = 20, fontweight = "bold", color = "black", pad=15)
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()


# Deep progres et goal
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_turnovers_90'], df['player_season_change_in_passing_ratio'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Gaël Clichy' :
    ax.annotate(txt, (df.player_season_turnovers_90.iat[i]-0.15, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Moustapha Seck' :
    ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Abdallah N"Dour' :
     ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.1, df.player_season_change_in_passing_ratio.iat[i]+.1), size = 10,backgroundcolor="w")
   if txt == 'Mateus Quaresma Correia' :
    ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Kylian Kaïboué' :
     ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Jonas Antonius Auer' :
     ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Maximiliano Moreira Romero' :
     ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Christian Neiva Afonso' :
     ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Amir Absalem' :
     ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Boy Kemper' :
     ax.annotate(txt, (df.player_season_turnovers_90.iat[i]+0.01, df.player_season_change_in_passing_ratio.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Moussa Diallo' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]-0.2, df.player_season_obv_pass_90.iat[i]-.2), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.xlabel("player_season_turnovers_90",fontsize = 12, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("player_season_change_in_passing_ratio",fontsize = 12, fontweight = "bold", color = "black")
plt.title("Qualité Technique  ",fontsize = 20, fontweight = "bold", color = "black", pad=15)
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()

# Deep progres et goal
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_deep_progressions_90'], df['player_season_obv_pass_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Gaël Clichy' :
    ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]-0.15, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Moustapha Seck' :
    ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Abdallah N"Dour' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.1, df.player_season_obv_pass_90.iat[i]+.1), size = 10,backgroundcolor="w")
   if txt == 'Mateus Quaresma Correia' :
    ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Kylian Kaïboué' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Jonas Antonius Auer' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Maximiliano Moreira Romero' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Christian Neiva Afonso' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Amir Absalem' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Boy Kemper' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Moussa Diallo' :
     ax.annotate(txt, (df.player_season_deep_progressions_90.iat[i]+0.01, df.player_season_obv_pass_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.xlabel("player_season_deep_progressions_90",fontsize = 12, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("player_season_obv_pass_90",fontsize = 12, fontweight = "bold", color = "black")
plt.title("Jeu Offensif  ",fontsize = 20, fontweight = "bold", color = "black", pad=15)
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()

















## Qualité de tir vs occasion 
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_np_xg_per_shot'], df['player_season_np_psxg_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Patrick Pflücke' :
    ax.annotate(txt, (df.player_season_np_xg_per_shot.iat[i]+0.01, df.player_season_np_psxg_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Boubacar Fofana' :
    ax.annotate(txt, (df.player_season_np_xg_per_shot.iat[i]+0.01, df.player_season_np_psxg_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Ronny Rodelin' :
     ax.annotate(txt, (df.player_season_np_xg_per_shot.iat[i]+0.01, df.player_season_np_psxg_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Miroslav Stevanović' :
    ax.annotate(txt, (df.player_season_np_xg_per_shot.iat[i]+0.01, df.player_season_np_psxg_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Derek Kutesa' :
     ax.annotate(txt, (df.player_season_np_xg_per_shot.iat[i]+0.01, df.player_season_np_psxg_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.xlabel("xG par Tir",fontsize = 12, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("Qualité du tir",fontsize = 12, fontweight = "bold", color = "black")
#plt.title("Expected Goals vs Goals",fontsize = 20, fontweight = "bold", color = "black", pad=15)
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()


## menace ##
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_obv_pass_90'], df['player_season_obv_dribble_carry_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Patrick Pflücke' :
    ax.annotate(txt, (df.player_season_obv_pass_90.iat[i]+0.01, df.player_season_obv_dribble_carry_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Boubacar Fofana' :
    ax.annotate(txt, (df.player_season_obv_pass_90.iat[i]+0.01, df.player_season_obv_dribble_carry_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Ronny Rodelin' :
     ax.annotate(txt, (df.player_season_obv_pass_90.iat[i]+0.01, df.player_season_obv_dribble_carry_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Miroslav Stevanović' :
    ax.annotate(txt, (df.player_season_obv_pass_90.iat[i]+0.01, df.player_season_obv_dribble_carry_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Derek Kutesa' :
     ax.annotate(txt, (df.player_season_obv_pass_90.iat[i]+0.01, df.player_season_obv_dribble_carry_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()



## Technique ##
fig, ax = plt.subplots(figsize=(16,9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['player_season_dispossessions_90'], df['player_season_total_dribbles_90'], c="Grey")
# Annotate each data point
#if df['Team'] == Servette 
for i, txt in enumerate(df.player_name):
   if txt == 'Patrick Pflücke' :
    ax.annotate(txt, (df.player_season_dispossessions_90.iat[i]+0.01, df.player_season_total_dribbles_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Boubacar Fofana' :
    ax.annotate(txt, (df.player_season_dispossessions_90.iat[i]+0.01, df.player_season_total_dribbles_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Ronny Rodelin' :
     ax.annotate(txt, (df.player_season_dispossessions_90.iat[i]+0.01, df.player_season_total_dribbles_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Miroslav Stevanović' :
    ax.annotate(txt, (df.player_season_dispossessions_90.iat[i]+0.01, df.player_season_total_dribbles_90.iat[i]+.0), size = 10,backgroundcolor="w")
   if txt == 'Derek Kutesa' :
     ax.annotate(txt, (df.player_season_dispossessions_90.iat[i]+0.01, df.player_season_total_dribbles_90.iat[i]+.0), size = 10,backgroundcolor="w")
# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
# Change ticks
plt.tick_params(axis='x', labelsize=8, color='black')
plt.tick_params(axis='y', labelsize=8, color='black')
plt.show()







###
#df.rename(columns={'Primary Position': 'Pos'}, inplace=True)
#df_sorted= df[ (df.Pos == 'Centre Forward') | (df.Pos == 'Left Centre Forward') | (df.Pos == 'Right Centre Forward') | 
             # (df.Pos == 'Central Attacking Midfielder') | (df.Pos == 'Right Wing') | (df.Pos == 'Left Wing')]

df_sorted = df.sort_values('xG & xGassited', ascending=False)
df_sorted.columns = df_sorted.columns.str.replace('Scoring Contribution', 'Scoring')
df_sorted.columns = df_sorted.columns.str.replace('xG & xGassited', 'xGA')
df_sorted.drop(df_sorted[df_sorted.xGA < 0.50].index, inplace=True)

df_sorted.plot.bar(x='Name', y='xGA',color="black", rot=50)

fig, ax = plt.subplots(figsize=(50,10))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.bar(df_sorted, df_sorted['xGA'])

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
plt.tick_params(axis='x', labelsize=5, color='black')
plt.tick_params(axis='y', labelsize=5, color='black')

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(df_sorted.Name, df_sorted["xGA"], width=0.8) 
ax.set_xticklabels(df_sorted.Name, rotation = 90, fontsize= 5)
ax.set_ylabel("xG & xG Assisted /90")
plt.show()


