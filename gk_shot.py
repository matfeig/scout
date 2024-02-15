#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 19:18:00 2023

@author: matfeig
"""
from statsbombpy import sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pyplot

user ="m.feigean@servettefc.ch"
password ="QzG3Kdlu"

#set the colours that you wish to use in the visual
color1="#d62828"
color2="#48cae4"

#set the name of the player and their club - this should be as they appear in StatsBomb IQ
player="Jeremy Frick"
team="Servette"

#set variables for league that you are analysisng
comp_id =80 #StatsBomb's competition ID
season_id=281 #StatsBomb's season ID

#get lists of matches
matches = sb.matches(competition_id = comp_id, season_id = season_id,
                     creds={"user":user, "passwd": password})

matches = matches.loc[(matches['home_team'] == team)|(matches['away_team'] == team)]
matches=matches.sort_values(by=['match_date'])
matches=matches[matches["match_status"]=="available"]
list_matches=matches.match_id.tolist()

matches=matches[["match_id","match_date"]]

#get event data for all games played by team
data = []
for n in list_matches:
    match_events = sb.events(match_id = n,
                             creds={"user": user, "passwd": password})
    data.append(match_events)
data=pd.concat(data)

#filter data to get only games in which GK featured
df_gk = data[(data["player"]==player)&(data["team"]==team)]

list_player_match=df_gk.match_id.unique().tolist()

#define functions
#get a dataframe of all the shots that the GK faced in each game
def get_stats(match_id):

    gk_match=df_gk[df_gk["match_id"]==match_id]
        
    shots_faced=['Shot Saved', 'Shot Faced', 'Goal Conceded','Shot Saved to Post', 'Shot Saved Off Target']
    
    shots_faced_df=gk_match[gk_match["goalkeeper_type"].isin(shots_faced)]
    shots_faced_df=shots_faced_df[shots_faced_df["related_events"].notnull()]

    shots_list=shots_faced_df['related_events'].apply(pd.Series).stack().unique()
    
    df_shots=data[data["id"].isin(shots_list)]
    
    psxg_stats=df_shots[["match_id","team","shot_gk_shot_stopping_xg_suppression","shot_gk_positioning_xg_suppression"]]
    
    return psxg_stats

#loop through all the games that GK played and create single dataframe of all shots faced
all_psxg_stats=[]
for m in list_player_match:
    psxg_stats = get_stats(m)
    all_psxg_stats.append(psxg_stats)
    
all_psxg_stats = pd.concat(all_psxg_stats)

#get totals for xG suppression metrics
pos_sup=round(all_psxg_stats["shot_gk_positioning_xg_suppression"].sum(),2)
if pos_sup > 0:
    pos_sup="+"+ str(pos_sup)
else:
    pass

shot_sup=round(all_psxg_stats["shot_gk_shot_stopping_xg_suppression"].sum(),2)
if shot_sup > 0:
    shot_sup="+"+ str(shot_sup)
else:
    pass

#merge dataframes to add date
all_psxg_stats=pd.merge(all_psxg_stats, matches, 
              how="left", on=["match_id"])

#sort by date
all_psxg_stats=all_psxg_stats.sort_values(by=['match_date']).reset_index(drop=True)
all_psxg_stats["team_date"]=all_psxg_stats["team"]+"\n"+all_psxg_stats["match_date"]

#define how to plot lines for match averages
def plot_lines(Y,x_metric,ax):
    for index in Y:
        difference = x_metric[index]
        if difference > 0:
            ax.plot(
                [0, difference],
                [index, index],
                lw = 7.5,
                color = color1,
                zorder = 8
            )
        else:
            ax.plot([difference, 0],
                      [index, index],
                      lw = 7.5,
                      color = color2,
                      zorder = 8
                    )

#define plot for individual shots
def plot_swarm(df,ax,var="variable"):

    df_means = df.groupby(["team_date","match_date"])[var].agg("mean").reset_index()
    df_means=df_means.sort_values(by=['match_date']).reset_index(drop=True)

    sns.stripplot(ax=ax,data=df, x=var, y="team_date"
                  ,s=10
                  ,orient="h"
                  ,color="white"
                  ,alpha=0.75
                  ,ec="black"
                  ,linewidth=2.5
                  ,zorder=7)
    
    ax.axvline(0,color="black",lw=7.5,zorder=9)
    
    x_metric=df_means[var]
    teams = list(df_means["team_date"].unique())
    Y = np.arange(len(teams))
    plot_lines(Y,x_metric,ax)
    
    limit=max(abs(data[var].min()),abs(data[var].max()))
    ax.set(xlim=(limit*-1,limit))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    avg=round(df[var].mean(),5)
    if avg > 0:
        avg="+"+ str(avg)
    else:
        pass
    ax.set_title(label=f"Avg. Over/Under: {avg}",x=0.5,y=1.02,size=18,color="black",ha='center')
    
    ax.grid()
    
#plot all data on single figure
fig = plt.figure(figsize=(22,15),constrained_layout=True)
gs = fig.add_gridspec(nrows=1,ncols=2)

ax1 = fig.add_subplot(gs[0])
plot_swarm(all_psxg_stats,ax1,"shot_gk_positioning_xg_suppression")
ax1.set_xlabel("GK Positioning",fontsize=18)
ax1.text(0, -4, s=f"Positioning: {pos_sup} goals", fontsize=22,ha='center',color="black",fontweight="bold")
ax1.set_ylabel("",fontsize=18)
ax1.set(xlim=(-0.25,0.25))

ax2 = fig.add_subplot(gs[1])
plot_swarm(all_psxg_stats,ax2,"shot_gk_shot_stopping_xg_suppression")
ax2.set_xlabel("Shot Stopping",fontsize=18)
ax2.text(0, -4, s=f"Shot Stopping: {shot_sup} goals", fontsize=22,ha='center',color="black",fontweight="bold")
ax2.set_ylabel("",fontsize=18)


fig.text(s=f"GK data analysis | {player}, {team}",
        x=0.025, y =1.1, fontsize=26,fontweight="bold")

fig.text(s=f"Goalkeeper game-by-game performance using StatsBomb's 'shot stopping xG suppression' and 'positioning xG suppression' metrics.\nCircles represent individual shots, bars reperesent game averages.\nData points to the right of the black horizontal line can be considered 'positive' actions, and vice versa.",
        x=0.025, y =1.03, fontsize=18)

plt.show()