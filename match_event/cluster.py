#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:08:56 2021

@author: matfeig
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mplsoccer.pitch import Pitch

from sklearn.cluster import KMeans


#import data
df = pd.read_csv('sfc_vadbomb.csv')

df = df[(df['team_name']=='Servette')&(df['event_type_name']=='Pass')].reset_index()

X = np.array(df[['location_x','location_y','end_location_x','end_location_y']])
kmeans = KMeans(n_clusters = 20,random_state=100)
kmeans.fit(X)
df['cluster'] = kmeans.predict(X)

df.head()

df.cluster.value_counts()


fig, ax = plt.subplots(figsize=(10,10))
fig.set_facecolor('#38383b')
ax.patch.set_facecolor('#38383b')

pitch = Pitch(pitch_type='statsbomb',orientation='horizontal',
             pitch_color='#38383b',line_color='white',figsize=(10,10),
             constrained_layout=False,tight_layout=True,view='full')

pitch.draw(ax=ax)

for x in range(len(df['cluster'])):
    
    if df['cluster'][x] ==5:
        pitch.lines(xstart=df['location_x'][x],ystart=df['location_y'][x],xend=df['end_location_x'][x],yend=df['end_location_y'][x],
                   color='#74c69d',lw=5,zorder=2,transparent=True, comet=True,ax=ax)
        
    if df['cluster'][x] ==5:
        pitch.lines(xstart=df['location_x'][x],ystart=df['location_y'][x],xend=df['end_location_y'][x],yend=df['end_location_y'][x],
                   color='#add8e6',lw=5,zorder=2,transparent=True, comet=True,ax=ax)
                   
    if df['cluster'][x] ==10:
        pitch.lines(xstart=df['location_x'][x],ystart=df['location_y'][x],xend=df['end_location_y'][x],yend=df['end_location_y'][x],
                   color='blue',lw=5,zorder=2,comet=True,ax=ax)