#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 09:14:23 2021

@author: matfeig
"""

from scipy.spatial import ConvexHull
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import seaborn as sns

from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_color='lightgrey', line_color='white', stripe=False, axis=False, label=False, tick=False)
fig, ax = pitch.draw()


defdata = pd.read_csv("zur_stgbomb.csv")
defdata.head()
#defdata.dropna(subset=['location_x'], inplace = True)


player8108 = defdata.loc[(defdata['player_id'] == 8108)]
player8108.head()



##### For One player #######@
defpoints = player8108[['location_x', 'location_y']].values
defpoints
#Create a convex hull object and assign it to the variable hull
hull = ConvexHull(player8108[['location_x','location_y']])
#Display hull
hull
#Plot the X & Y location with dots
plt.plot(player8108.location_x,player8108.location_y, 'o')
#Loop through each of the hull's simplices
for simplex in hull.simplices:
    #Draw a black line between each
    plt.plot(defpoints[simplex, 0], defpoints[simplex, 1], 'k-')
    
    
    
#######Plot the X & Y location with dots
fig, ax = pitch.draw()
plt.plot(player8108.location_x,player8108.location_y, 'o')
#Loop through each of the hull's simplices
for simplex in hull.simplices:
    #Draw a black line between each
    plt.plot(defpoints[simplex, 0], defpoints[simplex, 1], 'k-')    
#Fill the area within the lines that we have drawn
plt.fill(defpoints[hull.vertices,0], defpoints[hull.vertices,1], 'k', alpha=0.5)
#plt.legend(player8108) 



###### All the players ######
Team = defdata.loc[(defdata.team_name == "St. Gallen")]
Team.head()
players = Team["player_id"].unique()
players = players[~np.isnan(players)]
print (players)

#For each player in our players variable
for player_id in players:
    
    fig, ax = pitch.draw() 
    #ax.legend(player_id)
    df = Team[(Team.player_id == player_id)]
    
    #Create an array of the x/y coordinate groups
    points = df[['location_x', 'location_y']].values

    #If there are enough points for a hull, create it. If there's an error, forget about it
    try:
        hull = ConvexHull(df[['location_x','location_y']])
        
    except:
        pass
    
    #If we created the hull, draw the lines and fill with 5% transparent red. If there's an error, forget about it
    try:     
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
            plt.fill(points[hull.vertices,0], points[hull.vertices,1], 'blue', alpha=0.05)                       
    except:
        pass 
#Once all of the individual hulls have been created, plot them together
plt.show()
















