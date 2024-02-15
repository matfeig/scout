#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch
from highlight_text import fig_text
from matplotlib.colors import TwoSlopeNorm


### download data ###
df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/event_match/fcz_sfc_3.csv")



df['event_type_name'].value_counts()


df = df[['timestamp', 'period','minute','second','event_type_name',
         'possession',
         'possession_team_name','player_name','team_name',
         'location_x','location_y','duration','outcome_name',
         'type_name']]

df.sort_values(['period','timestamp'],
               inplace=True,
               ignore_index=True)

df['change_in_possession'] = df['possession'].diff()

df['change_in_possession'].value_counts()


# Filter rows where we had a switch in possession
possession_switch = df[df['change_in_possession'] == 1].reset_index(drop=True)

possession_switch['delta_time'] = pd.to_datetime(possession_switch['timestamp']).diff()

possession_switch['delta_seconds'] = [x.total_seconds() for x in possession_switch['delta_time']]
possession_switch.head()

possession_switch[possession_switch['possession_team_name'] == 'Servette'
                  ]['delta_seconds'].hist()


pitch = Pitch( line_zorder=2, line_color='black')

arg_touch = possession_switch[possession_switch['possession_team_name'] != 'Servette'
                              ]

arg_hist = pitch.bin_statistic(arg_touch.location_x, 
                               arg_touch.location_y, statistic='count', 
                               bins=(3, 3), normalize=False)

pol_touch = possession_switch[(possession_switch['possession_team_name'] != 'Servette') &
                              (possession_switch['delta_seconds'] <= 8)
                              ]

pol_hist = pitch.bin_statistic(pol_touch.location_x, 
                               pol_touch.location_y, statistic='count', 
                               bins=(3,3), normalize=False)


arg_ratio  = pol_hist["statistic"]/arg_hist["statistic"]

divnorm = TwoSlopeNorm(vmin=0, vcenter=0.25, vmax=0.5)

arg_hist["statistic"] = arg_ratio

fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)

pcm  = pitch.heatmap(arg_hist, cmap='bwr_r', edgecolor='grey', ax=ax['pitch'], norm = divnorm,
                     )

#legend to our plot
ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
cbar = plt.colorbar(pcm, cax=ax_cbar)
 
labels = pitch.label_heatmap(arg_hist, color='black', fontweight = "bold",fontsize=24,
                             ax=ax['pitch'], ha='center', va='center',
                             str_format='{:.0%}')
fig.suptitle("Ball recovery within 5 seconds | Servette FC", fontsize = 26,
             fontweight = "bold", color = "black")
plt.show()
