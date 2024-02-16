#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:44:39 2021

@author: matfeig
"""

#https://mplsoccer.readthedocs.io/en/latest/gallery/plots/plot_flow.html#sphx-glr-gallery-plots-plot-flow-py

from mplsoccer.pitch import Pitch
from mplsoccer.statsbomb import read_event, EVENT_SLUG
from matplotlib import rcParams
from scipy.stats import circmean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd

#rcParams['text.color'] = '#c7d5cc'  # set the default text color

# get event dataframe for game 7478, create a dataframe of the passes, and a boolean mask for the outcome


########                 ##########
######## From MPLsoccer  ##########
########                 ##########


# df = read_event(f'{EVENT_SLUG}/7478.json',
#                 related_event_df=False, shot_freeze_frame_df=False, tactics_lineup_df=False)['event']

# team1, team2 = df.team_name.unique()
# mask_team1 = (df.type_name == 'Pass') & (df.team_name == team1)

# df_pass = df.loc[mask_team1, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]
# mask_complete = df_pass.outcome_name.isnull()

# pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', figsize=(17, 10), line_zorder=2,
#               line_color='white', constrained_layout=True, tight_layout=False, pitch_color='lightgrey')
# bins = (6, 3)


# # Plotting using a single color and length
# fig, ax = pitch.draw()
# # plot the heatmap - darker colors = more passes originating from that square
# bs_heatmap = pitch.bin_statistic(df_pass.x, df_pass.y, statistic='count', bins=bins)
# hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Blues')
# # plot the pass flow map with a single color ('black') and length of the arrow (5)
# fm = pitch.flow(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, color='black', arrow_type='same',
#                 arrow_length=5, bins=bins, ax=ax)
# ax.set_title(f'{team1} pass flow map vs {team2}', fontsize=10, pad=-5)
# fig.set_facecolor('lightgrey')


########                 ##########
########  From my Data   ##########
########                 ##########


df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/event_match/sfc_fcs_2.csv")
df.dropna(subset=['location_x'], inplace = True)
df.reset_index(level=0, inplace = True)
df.head()

team1, team2 = df.team_name.unique()
mask_team2 = (df.event_type_name == 'Pass') & (df.team_name == team1)

df_pass = df.loc[mask_team2, ['location_x', 'location_y', 'end_location_x', 'end_location_y', 'outcome_name']]
mask_complete = df_pass.outcome_name.isnull()

pitch = Pitch(line_zorder=2, line_color='black', linewidth=1)

bins = (6, 5)


fig, ax = pitch.draw()

# plot the heatmap - darker colors = more passes originating from that square
bs_heatmap = pitch.bin_statistic(df_pass.location_x, df_pass.location_y, statistic='count', bins=bins)
hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Blues')
fm = pitch.flow(df_pass.location_x, df_pass.location_y, df_pass.end_location_x, df_pass.end_location_y, color='black', arrow_type='same',
                arrow_length=6, bins=bins, ax=ax)
fig.suptitle("Pass Flow | Servette FC - FC Sion", fontsize = 12, fontweight = "bold", color = "black")
#ax.set_title(f'{team1} pass flow map vs {team2}', fontsize=15, pad=-15)
#fig.set_facecolor('#22312b')
                  

########                 ##########
########  From medium    ##########
########                 ##########                  
                  
# https://github.com/MaximeBataille/flow_pass_france_2018/blob/main/pass_flow_france_2018.ipynb
# https://maxime-bataille.medium.com/comment-tirer-des-enseignements-dun-pass-flow-c86a123c28be



from mplsoccer.pitch import Pitch
from mplsoccer.statsbomb import read_event, EVENT_SLUG
from matplotlib import rcParams
from scipy.stats import circmean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd


def createPassMap(df, player_name) :
    
    mask = (df.type_name == 'Pass') & (df.player_name == player_name)
    df_pass = df.loc[mask, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]
    
    mask_complete = df_pass.outcome_name.isnull()
    df_pass=df_pass[mask_complete]

    pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', figsize=(10, 8), line_zorder=4,
                  line_color='#c7d5cc', constrained_layout=True, tight_layout=False, pitch_color='white')
    bins = (6, 6)

    fig, ax = pitch.draw()
    # plot the heatmap - darker colors = more passes originating from that square
    bs_heatmap = pitch.bin_statistic(df_pass.x, df_pass.y, statistic='count', bins=bins)
    hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='Blues')
    # plot the pass flow map with a single color ('black') and length of the arrow (5)
    fm = pitch.flow(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, color='black', arrow_type='same',
                    arrow_length=7, bins=bins, ax=ax)

    fig.set_facecolor('white')
    
rcParams['text.color'] = '#c7d5cc'  # set the default text color

# get event dataframe for all games for France knockout games: , create a dataframe of the passes, and a boolean mask for the outcome
df_1 = read_event(f'{EVENT_SLUG}/7580.json',
                related_event_df=False, shot_freeze_frame_df=False, tactics_lineup_df=False)['event']
df_2 = read_event(f'{EVENT_SLUG}/8649.json',
                related_event_df=False, shot_freeze_frame_df=False, tactics_lineup_df=False)['event']
df_3 = read_event(f'{EVENT_SLUG}/8658.json',
                related_event_df=False, shot_freeze_frame_df=False, tactics_lineup_df=False)['event']
df_4 = read_event(f'{EVENT_SLUG}/8655.json',
                related_event_df=False, shot_freeze_frame_df=False, tactics_lineup_df=False)['event']
df=pd.concat([df_1, df_2, df_3, df_4], axis=0)   
    

top_players=["Hugo Lloris", "Lucas Hernández Pi", "Samuel Yves Umtiti", "Raphaël Varane","Benjamin Pavard",
             "Paul Pogba", 'N\"Golo Kanté', 
             "Kylian Mbappé Lottin","Blaise Matuidi",
             "Antoine Griezmann", "Olivier Giroud"]
 
for player in top_players :
    print('*********')
    print(player)
    createPassMap(df, player)
#    if player=='N\"Golo Kanté':
#        plt.savefig('img/pass_flow_{}'.format('N Golo Kanté'))
#    else:
#        plt.savefig('img/pass_flow_{}'.format(player))
    plt.show()                 

   
pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', figsize=(10, 8), line_zorder=4,
                  line_color='#c7d5cc', constrained_layout=True, tight_layout=False, pitch_color='white')
fig, ax = pitch.draw()
plt.savefig('img/pitch')               

                  