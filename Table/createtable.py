#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:04:13 2022

@author: matfeig
"""

#https://matplotlib.org/matplotblog/posts/how-to-create-custom-tables/

import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib import pyplot as plt

# first, we'll create a new figure and axis object

fig, ax = plt.subplots(figsize=(8,6))

# set the number of rows and cols for our table

rows = 10
cols = 6

# create a coordinate system based on the number of rows/columns

# adding a bit of padding on bottom (-1), top (1), right (0.5)

ax.set_ylim(-1, rows + 1)
ax.set_xlim(0, cols + .5)

# sample data

data = [
        {'id': 'player10', 'shots': 1, 'passes': 79, 'goals': 0, 'assists': 1},
        {'id': 'player9', 'shots': 2, 'passes': 72, 'goals': 0, 'assists': 1},
        {'id': 'player8', 'shots': 3, 'passes': 47, 'goals': 0, 'assists': 0},
        {'id': 'player7', 'shots': 4, 'passes': 99, 'goals': 0, 'assists': 5},
        {'id': 'player6', 'shots': 5, 'passes': 84, 'goals': 1, 'assists': 4},
        {'id': 'player5', 'shots': 6, 'passes': 56, 'goals': 2, 'assists': 0},
        {'id': 'player4', 'shots': 7, 'passes': 67, 'goals': 0, 'assists': 3},
        {'id': 'player3', 'shots': 8, 'passes': 91, 'goals': 1, 'assists': 1},
        {'id': 'player2', 'shots': 9, 'passes': 75, 'goals': 3, 'assists': 2},
        {'id': 'player1', 'shots': 10, 'passes': 70, 'goals': 4, 'assists': 0}
]

# from the sample data, each dict in the list represents one row

# each key in the dict represents a column

for row in range(rows):
	# extract the row data from the list

    d = data[row]

    # the y (row) coordinate is based on the row index (loop)

    # the x (column) coordinate is defined based on the order I want to display the data in


    # player name column

    ax.text(x=.5, y=row, s=d['id'], va='center', ha='left')
    # shots column - this is my "main" column, hence bold text

    ax.text(x=2, y=row, s=d['shots'], va='center', ha='right', weight='bold')
    # passes column

    ax.text(x=3, y=row, s=d['passes'], va='center', ha='right')
    # goals column

    ax.text(x=4, y=row, s=d['goals'], va='center', ha='right')
    # assists column

    ax.text(x=5, y=row, s=d['assists'], va='center', ha='right')
    
    # Add column headers

# plot them at height y=9.75 to decrease the space to the

# first data row (you'll see why later)

ax.text(.5, 9.75, 'Player', weight='bold', ha='left')
ax.text(2, 9.75, 'Shots', weight='bold', ha='right')
ax.text(3, 9.75, 'Passes', weight='bold', ha='right')
ax.text(4, 9.75, 'Goals', weight='bold', ha='right')
ax.text(5, 9.75, 'Assists', weight='bold', ha='right')
ax.text(6, 9.75, 'Special\nColumn', weight='bold', ha='right', va='bottom')

for row in range(rows):
    ax.plot(
    	[0, cols + 1],
    	[row -.5, row - .5],
    	ls=':',
    	lw='.5',
    	c='grey'
    )

# add a main header divider

# remember that we plotted the header row slightly closer to the first data row

# this helps to visually separate the header row from the data rows

# each data row is 1 unit in height, thus bringing the header closer to our 

# gridline gives it a distinctive difference.

ax.plot([0, cols + 1], [9.5, 9.5], lw='.5', c='black')

# highlight the column we are sorting by

# using a rectangle patch

rect = patches.Rectangle(
	(1.5, -.5),  # bottom left starting position (x,y)

	.65,  # width

	10,  # height

	ec='none',
	fc='grey',
	alpha=.2,
	zorder=-1
)
ax.add_patch(rect)

ax.axis('off')

ax.set_title(
	'A title for our table!',
	loc='left',
	fontsize=18,
	weight='bold'
)

newaxes = []
for row in range(rows):
    # offset each new axes by a set amount depending on the row

    # this is probably the most fiddly aspect (TODO: some neater way to automate this)

    newaxes.append(
        fig.add_axes([.75, .725 - (row*.063), .12, .06])
    )
    
    # plot dummy data as a sparkline for illustration purposes

# you can plot _anything_ here, images, patches, etc.

newaxes[0].plot([0, 1, 2, 3], [1, 2, 0, 2], c='black')
newaxes[0].set_ylim(-1, 3)

# once again, the key is to hide the axis!

newaxes[0].axis('off')