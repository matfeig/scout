#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:55:03 2023

@author: matfeig
"""
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch
import pandas as pd
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from highlight_text import fig_text
import pandas as pd
from mplsoccer import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

### download data ###
df = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/event_match/23_24/sfc_yb_1.csv")

team1, team2 = df.team_name.unique()
receipt = df.loc[(df["event_type_name"] == "Ball Receipt*") | (df["event_type_name"] == "Pass") ].set_index("id")


######## To rievieww #####

pitch = Pitch(line_zorder=2, line_color='black')

arg_touch = df.loc[(df["event_type_name"].isin(["Pass", "Ball Receipt*" ])) & (df.team_name == "Servette")]
pol_touch = df.loc[(df["event_type_name"].isin(["Pass", "Ball Receipt*"])) & (df.team_name == team2)]

arg_hist = pitch.bin_statistic(arg_touch.location_x, arg_touch.location_y, statistic='count', bins=(6, 5), normalize=False)
pol_hist = pitch.bin_statistic(pol_touch.location_x, pol_touch.location_y, statistic='count', bins=(6, 5), normalize=False)
pol_hist["statistic"] = np.flip(pol_hist["statistic"])


arg_ratio  = arg_hist["statistic"]/(arg_hist["statistic"]+pol_hist["statistic"])
pol_ratio = pol_hist["statistic"]/(arg_hist["statistic"]+pol_hist["statistic"])

divnorm = TwoSlopeNorm(vmin=0, vcenter=0.5, vmax=1)

arg_hist["statistic"] = arg_ratio

fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pcm  = pitch.heatmap(arg_hist, cmap='bwr_r', edgecolor='grey', ax=ax['pitch'], norm = divnorm)
#legend to our plot
ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
cbar = plt.colorbar(pcm, cax=ax_cbar)
fig_text(0.07,0.04,">55% pour SFC = bleu - 45% à 55% = blanc - <45% pour SFC = rouge ", color = "#870E26",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
fig.suptitle("Ratio ballons touchés | Controler le Territoire", fontsize = 30, fontweight = "bold", color = "black")
plt.show()
#####
#####
#####

### Making a diagram of most involved players ####
#keep only surnames
receipt["player_name"] = receipt["player_name"].apply(lambda x: str(x).split()[-1])
#count passes by player and normalize them
pass_count = receipt.groupby(["player_name"]).location_x.count().sort_values()
#make a histogram
pass_count = pass_count.plot.bar(pass_count)
#make legend
#ax.set_xlabel("")
#ax.set_ylabel("Number of ball receipt")



