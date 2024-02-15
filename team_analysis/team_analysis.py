#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:29:04 2021

@author: matfeig
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
df = pd.read_csv('2024-J18.csv')
df['path'] = df['Team Name'] + '.png'

##Comparer les années ###
# df2 = pd.read_csv('team_stats_2022_t1.csv')
# df2['path'] = df2['Team Name'] + '.png'
# df = data = pd.concat([df1,df2])
# df.head()
# data = pd.read_csv('sfc.csv', delimiter=';')
# data.head()

###########################################################################################
    
# Set font and background colour
plt.rcParams.update({'font.family':'Avenir'})
bgcol = '#fafafa'

# Create initial plot
fig, ax = plt.subplots(figsize=(16, 9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['NPxG'], df['NPxG.1'], c=bgcol)

# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8')
ax.spines['bottom'].set_color('#ccc8c8')

# Change ticks
plt.tick_params(axis='x', labelsize=12, color='#ccc8c8')
plt.tick_params(axis='y', labelsize=12, color='#ccc8c8')

# Plot badges
def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.03, alpha = 1)

for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row['NPxG'], row['NPxG.1']), frameon=False)
    ax.add_artist(ab)

# Add average lines
plt.hlines(df['NPxG.1'].mean(), df['NPxG'].min(), df['NPxG'].max(), color='black')
plt.vlines(df['NPxG'].mean(), df['NPxG.1'].min(), df['NPxG.1'].max(), color='black')

# Text

## Title & comment
fig.text(.15,.96,'xG Performance',size=20)
#fig.text(.15,.93,'Servette FC - medium xG & top 2 xG against', size=12)

## Avg line explanation
fig.text(.09,.14,'xG Against', size=9, color='#575654',rotation=90)
fig.text(.13,0.07,'xG For', size=9, color='#575654')

## Axes titles
#fig.text(.76,.43,'Avg. xG Against', size=9, color='black')
#fig.text(.52,.17,'Avg. xG For', size=9, color='black',rotation=90)

## Save plot
#plt.savefig('xGChart.png', dpi=1200, bbox_inches = "tight")

######################################################################################################################


# Set font and background colour
plt.rcParams.update({'font.family':'Avenir'})
bgcol = '#fafafa'

# Create initial plot
fig, ax = plt.subplots(figsize=(16, 9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['G'], df['NPxG'], c=bgcol)

# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8')
ax.spines['bottom'].set_color('#ccc8c8')

# Change ticks
plt.tick_params(axis='x', labelsize=12, color='#ccc8c8')
plt.tick_params(axis='y', labelsize=12, color='#ccc8c8')
plt.xlim(0.75, 1.8)
plt.ylim(0.75, 2.5)


# Plot badges
def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.03, alpha = 1)

for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row['NPxG'], row['G']), frameon=False)
    ax.add_artist(ab)

# Add average lines
# plt.hlines(df['G'].mean(), df['NPxG'].min(), df['NPxG'].max(), color='#c2c1c0', linestyle='-')
# plt.vlines(df['NPxG'].mean(), df['G'].min(), df['G'].max(), color='#c2c1c0', linestyle='-')
ax.scatter(df['G'], df['NPxG'], c=bgcol)

# Add y=x line
x = np.linspace(0, 3, 100)
y = x
ax.plot(x, y, color='#c2c1c0', linestyle='--')

# Text
# Plot badges
for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row['NPxG'], row['G']), frameon=False)
    ax.add_artist(ab)
    if row['Team Name'] == 'Servette':
        ax.annotate(f"NPxG: {row['NPxG']:.2f}", (row['NPxG'], row['G']), xytext=(0,-30), 
                    textcoords='offset points', ha='center', va='bottom', fontsize=10, color='black')
        ax.annotate(f"G: {row['G']}", (row['NPxG'], row['G']), xytext=(0, -35), 
                    textcoords='offset points', ha='center', va='top', fontsize=10, color='black')



## Title & comment
fig.text(.15,.96,'Performance Offensive | xG over Goals',size=20)
#fig.text(.15,.93,'Servette FC - Sur Performance légère - 1.30 Goals / 1.12 xG', size=16)

## Avg line explanation
fig.text(.1,.14,'Goals', size=10, color='black',rotation=90)
fig.text(.14,0.07,'xG', size=10, color='black')


############################################################################################

# Set font and background colour
plt.rcParams.update({'font.family':'Avenir'})
bgcol = '#fafafa'

# Create initial plot
fig, ax = plt.subplots(figsize=(16, 9))
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df['G.1'], df['NPxG.1'], c=bgcol)

# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8')
ax.spines['bottom'].set_color('#ccc8c8')

# Change ticks
plt.tick_params(axis='x', labelsize=12, color='#ccc8c8')
plt.tick_params(axis='y', labelsize=12, color='#ccc8c8')
plt.xlim(0.85, 1.65)
plt.ylim(0.55, 2.5)


# Plot badges
def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.03, alpha = 1)

for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row['NPxG.1'], row['G.1']), frameon=False)
    ax.add_artist(ab)

# Add average lines
# plt.hlines(df['G.1'].mean(), df['NPxG.1'].min(), df['NPxG.1'].max(), color='#c2c1c0', linestyle='-')
# plt.vlines(df['NPxG.1'].mean(), df['G.1'].min(), df['G.1'].max(), color='#c2c1c0', linestyle='-')
ax.scatter(df['G.1'], df['NPxG.1'], c=bgcol)

# Add y=x line
x = np.linspace(0, 3, 100)
y = x
ax.plot(x, y, color='#c2c1c0', linestyle='--')

# Text
# Plot badges
for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row['NPxG.1'], row['G.1']), frameon=False)
    ax.add_artist(ab)
    if row['Team Name'] == 'Servette':
        ax.annotate(f"NPxG.1: {row['NPxG.1']:.2f}", (row['NPxG.1'], row['G.1']), xytext=(0,-30), 
                    textcoords='offset points', ha='center', va='bottom', fontsize=10, color='black')
        ax.annotate(f"G.1: {row['G.1']}", (row['NPxG.1'], row['G.1']), xytext=(0, -35), 
                    textcoords='offset points', ha='center', va='top', fontsize=10, color='black')


## Title & comment
fig.text(.15,.96,'Performance Défensive | xG over Goals',size=20)
#fig.text(.15,.93,'Servette FC - Sur Performance légère - 1.5 Goals / 0.99 xG', size=16)

## Avg line explanation
fig.text(.08,.14,'Goals against', size=10, color='black',rotation=90)
fig.text(.14,0.07,'xG against', size=10, color='black')

################################################################################################

############################################################################################################


##### Roling Chart 




