#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 11:14:47 2022

@author: matfeig
"""
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

##https://matplotlib.org/matplotblog/posts/how-to-create-custom-tables/


from PIL import Image
import urllib
import os


df = pd.read_csv('/Users/matfeig/Dropbox/SFC/Database/minutes.csv', sep=';')
del df['Unnamed: 0']

df_example_1 = df[['Player', 'Pos', 'MP', 'Starts', 'Subs', 'unSub']]
print(tabulate(df_example_1.head(), tablefmt='pipe', headers='keys'))

df_example_2 = df[['Player', 'Pos', 'Min', 'MP', 'Starts', 'Subs','Compl', 'unSub']]
print(tabulate(df_example_2.head(), tablefmt='pipe', headers='keys'))

df_example_2['InSquad'] = df_example_2['MP'] + df_example_2['unSub']
df_example_2 = df_example_2.sort_values(by='Min', ascending=True).reset_index(drop=True)
df_example_2 = df_example_2[~df_example_2['Pos'].isna()]

df_example_2['Starts_InSquad'] = [f'{x}/{y}' for x,y in zip(df_example_2['Starts'], df_example_2['InSquad'])]
df_example_2.head()

######
###### Plot
######


fig = plt.figure(figsize=(7,10), dpi=300)
ax = plt.subplot()

ncols = 5
nrows = df_example_2.shape[0]

ax.set_xlim(0, ncols + 1)
ax.set_ylim(0, nrows + 1)

positions = [0.25, 2.5, 3.5, 4.5, 5.5]
columns = ['Player', 'Pos', 'Min', 'MP', 'Starts_InSquad']

# Add table's main text
for i in range(nrows):
    for j, column in enumerate(columns):
        if j == 0:
            ha = 'left'
        else:
            ha = 'center'
        if column == 'Min':
            text_label = f'{df_example_2[column].iloc[i]:,.0f}'
            weight = 'bold'
        else:
            text_label = f'{df_example_2[column].iloc[i]}'
            weight = 'normal'
        ax.annotate(
            xy=(positions[j], i + .5),
            text=text_label,
            ha=ha,
            va='center',
            weight=weight
        )

# Add column names
column_names = ['Player', 'Position', 'Minutes', 'Matches\nPlayed', 'Starts /\nIn Squad']
for index, c in enumerate(column_names):
        if index == 0:
            ha = 'left'
        else:
            ha = 'center'
        ax.annotate(
            xy=(positions[index], nrows + .25),
            text=column_names[index],
            ha=ha,
            va='bottom',
            weight='bold'
        )

# Add dividing lines
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows, nrows], lw=1.5, color='black', marker='', zorder=4)
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5, color='black', marker='', zorder=4)
for x in range(1, nrows):
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=1.15, color='gray', ls=':', zorder=3 , marker='')

ax.set_axis_off()
# plt.savefig(
#     'figures/pretty_example.png',
#     dpi=300,
#     transparent=True,
#     bbox_inches='tight')