#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 18:25:54 2023

@author: matfeig
"""
from statsbombpy import sb
import pandas as pd
import numpy as np
from mplsoccer import VerticalPitch
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans


# set up credentials for StatsBomb API access
email="m.feigean@servettefc.ch" #replace between the quotation marks with the email address that you use to login to StatsBomb IQ
password="QzG3Kdlu" #replace between the quotation marks with the password that you use to login to StatsBomb IQ 

#team you want to focus on
focus_team = "Servette"

comp_id=80 #StatsBomb's competition id
season_id=281 #StatsBomb's season id

#set colours and fonts
textc='#1d1d1d'
linec=textc
font="Inter"
bgcolor="white"
color1='#00CBD0'
color2='#ED8A16'
color3='#AB2EBF'
color4='#E7C418'
color5='#5DD413'
color6='#E60FB0'
color7='#2A76DF'
color8='#DF3B3B'

#pitch variables 
pitch = VerticalPitch(pitch_type='statsbomb',
              pitch_color=bgcolor, line_color=linec,line_zorder=3)


# get matches for focus_team
matches = sb.matches(competition_id=comp_id, season_id=season_id,
                               creds={"user":email, "passwd":password})
team_matches = matches[(matches["home_team"] == focus_team) | (matches["away_team"] == focus_team)]
team_matches = team_matches[team_matches["match_status"] == "available"]
list_matches = list(team_matches["match_id"])

# pull events for those matches
data = []
for n in list_matches:
    match_events = sb.events(match_id = n,include_360_metrics=True,creds={"user":email, "passwd":password})
    data.append(match_events)
data=pd.concat(data)

match_events = pd.DataFrame(data)

#parse out start and end locations
match_events[['x', 'y', 'z']] = match_events['location'].apply(pd.Series)
match_events[['pass_end_x', 'pass_end_y']] = match_events['pass_end_location'].apply(pd.Series)

#filter to passes into final 3rd from focus team 
df=match_events[match_events["team"]==focus_team]
df=df[df["type"]=="Pass"]
df=df[df['pass_type'].isnull()]
df=df[df["pass_end_x"]>40]
df=df[df["x"]<=40]

# Prepare data for clustering
cluster_data = df[['x', 'y', 'pass_end_x', 'pass_end_y']]
n_clusters = 8

# Apply KMeans clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(cluster_data)
df['pass_pass_cluster_id'] = kmeans.labels_




#group passes by cluster id and sort by volume
rank=df.groupby(['pass_pass_cluster_id']).size().reset_index()
rank.rename(columns={rank.columns[1]: "total_passes_in_cluster" }, inplace = True)
rank=rank.sort_values(by='total_passes_in_cluster', ascending=False)

#get list of 6 most common cluster ids
list_clusters=rank["pass_pass_cluster_id"].tolist()
list_clusters=list_clusters[:8] #last 6
df=df[df.pass_pass_cluster_id.isin(list_clusters)]

fig, axs = pitch.grid(nrows=2, ncols=4, figheight=16,
                      grid_width=0.85,
                      endnote_height=0.03, endnote_space=0,
                      axis=False,
                      title_space=0.02, title_height=0.06, grid_height=0.85)

#loop through 6 most common clusters and plot on pitch
for i, ax in enumerate(axs['pitch'].flat[:len(list_clusters)]):
    
    #filter df to get only passes in cluster i
    df_cluster = df[(df['pass_pass_cluster_id']==list_clusters[i])]
    
    #set colours for clusters
    if i == 0:
        color=color1
    elif i ==1:
        color=color2
    elif i ==2:
        color=color3
    elif i ==3:
        color=color4    
    elif i ==4:
        color=color5
    elif i ==5:
        color=color6
    elif i ==6:
        color=color7
    elif i ==7:
        color=color8
    
    #take random sample of 50 clusters
    if len(df_cluster)>=50:
         df_cluster=df_cluster.sample(n = 50)
    else:
         pass
    #plot passes on pitch
    pitch.arrows(df_cluster.x, df_cluster.y,
             df_cluster.pass_end_x, df_cluster.pass_end_y, width=2,
             headwidth=5, headlength=5, color=color, ax=ax,alpha=0.95)

#plot legend
custom_lines = [Line2D([0], [0], color=color1, lw=4),
                Line2D([0], [0], color=color2, lw=4),
                Line2D([0], [0], color=color3, lw=4),
                Line2D([0], [0], color=color4, lw=4),
                Line2D([0], [0], color=color5, lw=4),
                Line2D([0], [0], color=color6, lw=4),
                Line2D([0], [0], color=color7, lw=4),
                Line2D([0], [0], color=color8, lw=4)]

labels = ["Most common","2nd most common","3rd most common","4th common","5th most common","6th most common","7th most common","8th most common"]

fig.legend(custom_lines, labels, fontsize=20, loc='lower center',
           bbox_to_anchor=[0.5, -0.025],ncol=3)

#set titles
fig.text(s=f"{focus_team} - Pattern de passes pour atteindre le dernier tier? ", #ha='center'
         x=0.075, y =0.975, fontsize=32,color="black",fontweight='semibold')

league=matches.iloc[0]["competition"]
season=matches.iloc[0]["season"]
fig.text(s=f"{league}, {season}, completed passes only.", #ha='center'
         x=0.075, y =0.925, fontsize=22,color="black")


######################

















