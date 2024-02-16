#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 08:44:03 2022

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
data = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/fcw_sfc_2.csv")
#data = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/M21/luzern_sfc_1.csv")

data.columns = data.columns.map(lambda x: x.removeprefix("player_match_"))
data = data.replace(np.nan,0)

###############################
######### KPI match ###########
###############################

df_sfc = data.loc[(data.team_name == "Servette")]
#df_sfc = data.loc[(data.team_name == "Servette FC M-21")]
df_sfc = df_sfc[['team_name','player_name','op_passes_into_box','obv','obv_dribble_carry', 'obv_shot', 'obv_defensive_action','deep_progressions']]

df_sfc['obv_shot'].sum()
df_sfc['op_passes_into_box'].sum()
df_sfc['deep_progressions'].sum()
df_sfc['obv_dribble_carry'].sum()
df_sfc['obv'].sum()
df_sfc['obv_defensive_action'].sum()


