#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 11:23:59 2021

@author: peter
"""

import pandas as pd
import numpy as np

df = pd.read_excel("fw_kmeans_absvalues.xlsx")
del df['Unnamed: 0']
n = df.groupby("k_means").median()
n.to_excel('fw_kmeans_absvalues_median.xlsx', index=True)

### start ###
df_median = pd.read_excel("fw_kmeans_absvalues_median.xlsx")
df_all_2021 = pd.read_csv("df_2020_vf.csv")

df_all_2021 = df_all_2021[ (df_all_2021.Pos == 'FW') | (df_all_2021.Pos == 'FW,MF') | (df_all_2021.Pos == 'FW,DF')]

from scipy import stats

def getPercentile(x):
    return stats.percentileofscore(s, x,kind='rank')

s = np.random.normal(df_all_2021['Long Balls'].median(), 2*df_all_2021['Long Balls'].std(), 1000)

kpi = ['xG','Shots','Dispossessed','Turnovers','Deep Progressions','Carries','Dribbles','Successful Dribbles','Touches In Box','Successful Crosses','PintoB','Key Passes','xG Assisted','Assists','OP Assists','OP Key Passes','Aerial Wins','Passes Inside Box']
df_percentile_out = pd.DataFrame()
for k in kpi:
    percentile_kpi = []
    
    s = np.random.normal(df_all_2021[k].median(), 2*df_all_2021[k].std(), 1000)
    for index,row in df_median.iterrows():   

        percentile_kpi.append(getPercentile(row[k]))
        
    df_percentile_out[k] = percentile_kpi
    
df_percentile_out.to_excel('fw_percentile_table.xlsx')    
        