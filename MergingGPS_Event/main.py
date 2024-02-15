#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 14:48:54 2021

@author: peter
"""

import GetGPS as GPS
import datetime
import pandas as pd
import numpy as np
import PrepareData as Prep
import math
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def distance(row):
    return math.sqrt( math.pow(row['end_location_x'] - row['location_x'],2) + math.pow(row['end_location_y'] - row['location_y'],2) )

"""def speed(row,ax):
    if row['deltaT']>0:
        return row['delta'+ax]/row['deltaT']
    else:
        return 0"""

date = '2021-11-07'
home_team = "Servette"
year = 2021
month = 11
day = 7
#ev_filename = 'Zurich_Servette_21092021.csv'
ev_filename = 'FCZ_SFC.csv'

#We need to add 2 hours!!
BeginMatch = datetime.datetime(year=year,month=month,day=day,hour=14+2,minute=15,second=38)
EndFirstHalf = datetime.datetime(year=year,month=month,day=day,hour=15+2,minute=1,second=10) #46'05''
BeginSecondHalf  = datetime.datetime(year=year,month=month,day=day,hour=15+2,minute=17,second=8)
EndMatch = datetime.datetime(year=year,month=month,day=day,hour=16+2,minute=2,second=57)#49'    
    
time_list = [BeginMatch,EndFirstHalf,BeginSecondHalf,EndMatch]

GPS.Download(date)
GPS.JSONtoCSV(date)

event_file = pd.read_csv(ev_filename)
#Storing lineups of Servette and substitutions
lineup,all_players = Prep.GetLineup(event_file)
all_players = [item.split(' ')[-1] for item in all_players]
#Converting matchTimestamp from event file to compare it with timestamp from GPS file
event_file['matchTimestamp'] = pd.to_datetime(event_file['timestamp'])

"""event_file['deltaT'] = (event_file['matchTimestamp'] -  event_file['matchTimestamp'].shift(1))/ pd.Timedelta(seconds=1)
event_file['deltaX'] = event_file['end_location_x'] - event_file['location_x']
event_file['deltaY'] = event_file['end_location_y'] - event_file['location_y']
event_file['deltaD'] = event_file.apply(distance,axis=1)
event_file['speedball_x'] = event_file.apply(lambda k: speed(k, 'X'), axis=1)
event_file['speedball_y'] = event_file.apply(lambda k: speed(k, 'Y'), axis=1)
event_file['speedball'] = event_file.apply(lambda k: speed(k, 'D'), axis=1)"""

#Improve to store 5 GPS point per second and approximated event data
dict_df = GPS.CSVtoXY(date,time_list,home_team) #returns list of df 

#Keep GPS data of only the players who played the match
dict_gps_players = {k: dict_df[k] for k in all_players if k in dict_df}

tot_df = GPS.MergeAllPlayers(dict_gps_players) #Add mean position for NaN GPS data

event_file['substituted_player_name'] = event_file['substituted_player_name'].replace(np.NaN,"")
event_file['player_name'] = event_file['player_name'].replace(np.NaN,"")
#Merge GPS and event data files
df_event_gps = GPS.MergeEvtGps(event_file,tot_df,time_list)
df_event_gps = Prep.CleanUpList(df_event_gps) #setting empty list instead of nan in empty rows from event file, needed to allow to loop on the column

#TO BE FIXED
df_event_gps = Prep.AddLineup(df_event_gps,lineup) #add lineup column, it will be used to clean data later on

#Set to nan X,Y of players who are not on the field
df_event_gps = Prep.SetNanBench(df_event_gps,all_players)



#Need to add centroid of the team, stretch index, compactness
df_event_gps = Prep.GetStretchIndex(df_event_gps)

import matplotlib.pyplot as plt

from scipy.spatial import ConvexHull

surf_area = []
for index,row in df_event_gps.iterrows():

        lu = row.lineup
        coord = []
        for l in lu:
            if l=='Frick' or math.isnan(row['X_'+l]) or  math.isnan(row['Y_'+l]): #Ignoring Frick,no GPS Data
                continue
            coord.append(np.array([row['X_'+l],row['Y_'+l]]))
        if len(coord)>9:
            coord = np.stack( coord, axis=0 )
            surf_area.append(ConvexHull(coord).volume)
            #print(ConvexHull(coord).volume)
            #hull = ConvexHull(coord)
            #plt.plot(coord[:,0], coord[:,1], 'o')
            #for simplex in hull.simplices:
            #    plt.plot(coord[simplex, 0], coord[simplex, 1], 'k-')
        else:
            surf_area.append(np.nan)

df_event_gps['SurfaceArea'] = surf_area

            
############

df_event_gps.to_excel('FCZ_Servette.xlsx')
df_event_gps.to_csv('FCZ_Servette.csv')
t = df_event_gps.dtypes


## Selection du type de donnée : ici choix de la - mi temps  1 = 1 iere mi temps 
df = df_event_gps[df_event_gps.apply(lambda x: x['period']==1, axis=1)]


### Distribution de la surface area 
df['SurfaceArea'].plot.hist()

########


from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_type= 'uefa', pitch_color='None', line_color='black')
#fig, ax = pitch.draw()


fig, ax = pitch.draw()
sc = pitch.scatter(df.Y_Kyei, df.X_Kyei,
                   # size varies between 100 and 1000 (points squared)
                   #s=(df_shots_barca.shot_statsbomb_xg * 900) + 100,
                   c='black',  # color for scatter in hex format
                   edgecolors='None',  # give the markers a charcoal border
                   # for other markers types see: https://matplotlib.org/api/markers_api.html
                   marker='.',
                   ax=ax)
sns.kdeplot(df["Y_Kyei"],df["X_Kyei"], cmap='Blues', shade=True, shade_lowest=False)
ax.set_xlim(0,105)
ax.set_ylim(0,68)
ax.set_ylim(ax.get_ylim() [::-1])

fig, ax = pitch.draw()
sc = pitch.scatter(df.Y_Cichy, df.X_Clichy,
                   # size varies between 100 and 1000 (points squared)
                   #s=(df_shots_barca.shot_statsbomb_xg * 900) + 100,
                   c='black',  # color for scatter in hex format
                   edgecolors='None',  # give the markers a charcoal border
                   # for other markers types see: https://matplotlib.org/api/markers_api.html
                   marker='.',
                   ax=ax)
#sns.kdeplot(df["Y_Sasso"],df["X_Kyei"], cmap='Blues', shade=True, shade_lowest=False)
ax.set_xlim(0,105)
ax.set_ylim(0,68)
#ax.set_ylim(ax.get_ylim() [::-1]) (Reverse for the second period)



