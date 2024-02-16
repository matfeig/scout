#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 10:33:10 2022

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
from highlight_text import fig_text, ax_text
from adjustText import adjust_text
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib import cm
import scipy.stats as stats

from mplsoccer import Pitch
from PIL import Image
import urllib
import os


plt.rcParams['font.family'] = 'Karla'


df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/recrutement/player-stats_iq.csv")

df = df.loc[(df["Season"] == "2022/2023")]

df = df.loc[(df["Default Radar Template"] == "Full Back")] 

df.to_csv('df.csv')



df = (df.groupby(['Player Id', 'player_first_name', 'player_last_name'])
    [['player_season_minutes', 'player_season_total_dribbles_90', 'player_season_dribbles_90']].sum()
    .reset_index()
)
df


df_plot = df[(df['player_season_minutes'] >= df['player_season_minutes'].median()) 
             & (df['player_season_total_dribbles_90'] >= df['player_season_total_dribbles_90'].median())]
df_plot

#df_plot = df_plot.assign(per_90 = lambda x: (x.long_balls_att/x.minutes)*90)
df_plot = df_plot.assign(succ_rate = lambda x: x.player_season_dribbles_90/x.player_season_total_dribbles_90)

df_plot['zscore'] = stats.zscore(df_plot['player_season_total_dribbles_90'])*.4 + stats.zscore(df_plot['succ_rate'])*.6
df_plot['annotated'] = [True if x > df_plot['zscore'].quantile(.8) else False for x in df_plot['zscore']]

df_plot.sort_values(by='player_season_total_dribbles_90')


df_plot['zscore'] = stats.zscore(df_plot['player_season_total_dribbles_90'])*.4 + stats.zscore(df_plot['succ_rate'])*.6
df_plot['annotated'] = [True if x > df_plot['zscore'].quantile(.8) else False for x in df_plot['zscore']]

#####
##### Plot 
#####


fig = plt.figure(figsize=(16,9), dpi=100)
ax = plt.subplot()
ax.grid(visible=True, ls='--', color='lightgrey')

ax.scatter(
    df_plot['player_season_total_dribbles_90'], df_plot['succ_rate'], 
    c=df_plot['zscore'], cmap='inferno', 
    zorder=3, ec='grey', s=55, alpha=0.8)
    
texts = []
annotated_df = df_plot[df_plot['annotated']].reset_index(drop=True)
for index in range(annotated_df.shape[0]):
    texts += [
        ax.text(
            x=annotated_df['player_season_total_dribbles_90'].iloc[index], y=annotated_df['succ_rate'].iloc[index],
            s=f"{annotated_df['player_first_name'].iloc[index][0]}. {annotated_df['player_last_name'].iloc[index]}",
            path_effects=[path_effects.Stroke(linewidth=2, foreground=fig.get_facecolor()), 
            path_effects.Normal()], color='black',
            family='DM Sans', weight='bold'
        )
    ]

adjust_text(texts, only_move={'points':'y', 'text':'xy', 'objects':'xy'})

ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)

    
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(.1))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0%}'))
ax.set_xlim(0)
ax.set_ylim(0,1)

ax.set_ylabel('Réussite (%)')
ax.set_xlabel('Dribbles')

fig_text(
    x = 0.09, y = .99, 
    s = "Dribblers",
    va = "bottom", ha = "left",
    fontsize = 15, color = "black", font = "DM Sans", weight = "bold"
)

fig_text(
    x = 0.09, y = 0.93, 
    s = "Only players with above median minutes & median total long balls are shown.\n Season 2022/2023",
    va = "bottom", ha = "left",
    fontsize = 12, color = "#5A5A5A", font = "Karla"
)

# plt.savefig(
# 	"figures/11072022_long_balls.png",
# 	dpi = 600,
# 	facecolor = "#EFE9E6",
# 	bbox_inches="tight",
#     edgecolor="none",
# 	transparent = False
# )

# plt.savefig(
# 	"figures/11072022_long_balls_tr.png",
# 	dpi = 600,
# 	facecolor = "none",
# 	bbox_inches="tight",
#     edgecolor="none",
# 	transparent = True
# )





























