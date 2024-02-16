#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 18:12:10 2021

@author: matfeig
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 21:49:48 2021

@author: victor
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import matplotlib
from matplotlib.colors import to_rgba
import csv

#Import EPV
epv = pd.read_csv("EPV_grid.csv", header=None)
epv = np.array(epv)
n_rows, n_cols = epv.shape
print(n_rows, n_cols)
plt.imshow(epv, cmap="inferno")

df = pd.read_csv("sfc_lugbomb.csv")

#Filter Successful Passes
df = df[df["event_type_name"]=="Pass"]
df = df[df["team_name"]=="Servette"]
df = df[df["player_name"]=="Gaël Clichy"]


#Bin Data
df['x1_bin'] = pd.cut(df['location_x'], bins=n_cols, labels=False)
df['x2_bin'] = pd.cut(df['end_location_x'], bins=n_cols, labels=False)
df['y1_bin'] = pd.cut(df['location_y'], bins=n_rows, labels=False)
df['y2_bin'] = pd.cut(df['end_location_y'], bins=n_rows, labels=False)


#Return Bin Values
df['start_zone_value'] = df[['x1_bin', 'y1_bin']].apply(lambda x: epv[x[1]][x[0]], axis=1)
df['end_zone_value'] = df[['x2_bin', 'y2_bin']].apply(lambda x: epv[x[1]][x[0]], axis=1)

#Calculate Difference
df['epv'] = df['end_zone_value'] - df['start_zone_value']


##### Match Cumulative EPV ######
fig, ax = plt.subplots()
ax.plot(df["minute"],df["epv"])
ax.set_xlabel("Time")
ax.set_ylabel("EPV") 
plt.show()

df['epv_sum'] = df['epv'].cumsum()
fig, ax = plt.subplots()
ax.plot(df["minute"],df["epv_sum"])
ax.set_xlabel("Time")
ax.set_ylabel("Cumative EPV") 
plt.show()

