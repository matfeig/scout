#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 15:47:57 2022

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as figure

df1 = pd.read_csv("tourx.csv")
df1.rename(columns={'Team Name':'Team'}, inplace=True)
df1.rename(columns={'NPxG.1':'NPxGc'}, inplace=True)
df1.rename(columns={'G.1':'Gc'}, inplace=True)


fig = plt.figure()
plt.figure(figsize=(12, 12))
ax = plt.axes()
ax.patch.set_facecolor('white')
ax.plot(df1['NPxG'],df1['G'], 'o', color='grey')
ax.set(xlim=(0.2, 3),ylim=(0.2, 3))
plt.title("Goals et Expected Goals par équipe - Tour 3") #title
plt.xlabel('xG ')
plt.ylabel('Goals')


for i in range(df1.shape[0]):
 plt.text(x=df1.NPxG[i]+0.02,y=df1.G[i]+0.02,s=df1.Team[i], 
          fontdict=dict(color='black',size=8))
 
plt.show()
 