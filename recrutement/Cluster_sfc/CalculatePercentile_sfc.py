#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 11:23:59 2021

@author: peter
"""

import pandas as pd
import numpy as np

df = pd.read_excel("profil_kmeans_absvalues.xlsx")
del df['Unnamed: 0']
n = df.groupby("k_means").median()
n.to_excel('profil_kmeans_absvalues_median.xlsx', index=True)

### start ###
df_median = pd.read_excel("profil_kmeans_absvalues_median.xlsx")
df_all_2021 = pd.read_csv("df.csv")

df_all_2021 = df_all_2021[(df_all_2021.primary_position == "Centre Forward")|(df_all_2021.primary_position == "Left Centre Forward")|(df_all_2021.primary_position == "Right Centre Forward")|
           (df_all_2021.secondary_position == "Centre Forward")|(df_all_2021.secondary_position == "Left Centre Forward")|(df_all_2021.secondary_position == "Right Centre Forward")|
           (df_all_2021.primary_position == "Left Wing")|(df_all_2021.primary_position == "Right Wing")|(df_all_2021.primary_position == "Centre Attacking Midf_all_2021ielder")|
           (df_all_2021.primary_position == "Left Attacking Midf_all_2021ielder")|(df_all_2021.primary_position == "Right Attacking Midf_all_2021ielder")]

from scipy import stats

def getPercentile(x):
    return stats.percentileofscore(s, x,kind='rank')

s = np.random.normal(df_all_2021['player_season_long_balls_90'].median(), 2*df_all_2021['player_season_long_balls_90'].std(), 1000)

kpi = ['player_season_np_xg_90','player_season_np_psxg_90','player_season_np_shots_90',
               'player_season_dribbles_90','player_season_obv_dribble_carry_90','player_season_carries_90',
               'player_season_dispossessions_90','player_season_turnovers_90', 
               'player_season_xa_90','player_season_op_passes_into_box_90','player_season_obv_pass_90',
               'player_season_touches_inside_box_90',
               'player_season_aerial_wins_90',                         
               'player_season_deep_completions_90','player_season_deep_progressions_90'
                ]
df_percentile_out = pd.DataFrame()
for k in kpi:
    percentile_kpi = []
    
    s = np.random.normal(df_all_2021[k].median(), 2*df_all_2021[k].std(), 1000)
    for index,row in df_median.iterrows():   

        percentile_kpi.append(getPercentile(row[k]))
        
    df_percentile_out[k] = percentile_kpi
    
df_percentile_out.to_excel('profil_percentile_table.xlsx')    
        