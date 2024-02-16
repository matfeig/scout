#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:05:49 2023

@author: matfeig
"""
from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch,Pitch
from highlight_text import ax_text, fig_text
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

creds = {
"user": "m.feigean@servettefc.ch",
"passwd": "QzG3Kdlu",
}

#set the competition and season ids as variables
comp_id = 80
season_id = 281

#create cmap and set colour variables
white="white"
sbred='#e21017'
lightgrey="#d9d9d9"
darkgrey='#9A9A9A'
cmaplist = [white, darkgrey, sbred]
cmap = LinearSegmentedColormap.from_list("", cmaplist)

#get aggregate data for the season
epl_agg_df = sb.player_season_stats(competition_id=comp_id, season_id=season_id, creds=creds)

#filter for players that have played at least 1200 minutes
epl_agg_df = epl_agg_df[(epl_agg_df["player_season_minutes"] >=90)]

#create new column for obv p90 for passes and carries combined
epl_agg_df['pass_carry_obv_90'] = (epl_agg_df["player_season_obv_pass_90"]+epl_agg_df["player_season_obv_dribble_carry_90"])

#sort to put top performers first
epl_agg_df.sort_values(by='pass_carry_obv_90', ascending=False, inplace=True)

#select top 10 performers
top10_obv_df = epl_agg_df.head(10)


ax, fig = plt.subplots(figsize=[10,10])
sns.barplot(data=top10_obv_df, x="pass_carry_obv_90", y="player_name", color=sbred)
plt.xlabel(xlabel="OBV per 90",fontsize=15)
plt.ylabel(ylabel="Player",fontsize=15)
plt.title("Swiss 2022/23: OBV from Passes, Carries, and Dribbles p90 (1200+ mins Played)",fontsize=20)
sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})
sns.despine(top=True, right=True, left=False, bottom=False)
plt.autoscale()
plt.savefig('obvbar.png', dpi=300, bbox_inches = "tight")
plt.show()


#######################
########################
########################
#set name of team
team="Servette"

#set name of player
player="Timothé Cognat"

 #use comp_id and season_id variables to get matches for chosen competition
matches_df = sb.matches(competition_id=comp_id, season_id=season_id, creds = creds)

#filter for only matches featuring a given team
matches_team_df = matches_df[(matches_df["home_team"]==team) | (matches_df["away_team"]==team)]

#filter for only games that have been played
matches_team_df=matches_team_df[matches_team_df["match_status"]=="available"]

#list of relevant match ids
matches_list = matches_team_df.match_id.tolist()

#load events from specific matches (faster than pulling a whole competition season)
events = []
for i in matches_list:
    match_events = sb.events(match_id=i,creds=creds)
    events.append(match_events)
events=pd.concat(events)

#parse location of events
events[['x', 'y','z']] = events['location'].apply(pd.Series)

#filter data to get events from selected player
events=events[(events["player"]==player)]

#filter data to get only passes, dribbles, and carries
events=events[(events["type"]=="Pass")|(events["type"]=="Dribble")|(events["type"]=="Carry")]

#set up the pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
fig, ax = pitch.draw(figsize=(16, 11),constrained_layout=True, tight_layout=False)
fig.set_facecolor('white')

#plot heat map
bin_statistic = pitch.bin_statistic(events.x, events.y, statistic='sum',
values=events.obv_total_net,
bins=(6, 4),normalize=True)

heatmap = pitch.heatmap(bin_statistic, ax=ax, cmap=cmap)

#set colour bar
cbar = fig.colorbar(heatmap, ax=ax, shrink=0.7)
cbar.outline.set_edgecolor('#000000')
cbar.ax.yaxis.set_tick_params(color='#000000')
ticks = plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#000000')

#set the title
ax_title = ax.set_title(f'{player}: OBV from Passes, Carries, and Dribbles', fontsize=30)

plt.savefig('taa_obv.png', dpi=100, bbox_inches = "tight")



