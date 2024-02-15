#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 13:44:59 2021

@author: peter
"""

import numpy as np
import pandas as pd
import math
import ast

"""def GetLineup(event_file):
    servette = event_file[event_file['team_name']=='Servette']
    lineup = servette[servette['event_type_name']=='Starting XI']['formation_player_name']
    #lu = ast.literal_eval(lineup)['lineup']
    lu = []
    for row in lineup.iterrows():
        lu.append(row.formation_player_name[0])
        
    subs = servette.substitution_replacement.dropna().unique().tolist()
    all_players = lineup+subs
    all_players = [x.split(' ')[-1] for x in all_players]
    all_players = [x.replace('ć','c') for x in all_players] #to fix Stevanovic name
    
    return lineup,all_players"""

def GetLineup(event_file):
    servette = event_file[event_file['team_name']=='Servette']
    lineup = servette[servette['event_type_name']=='Starting XI']
    lu = lineup.formation_player_name.dropna().unique().tolist()
    
    subs = servette[servette['event_type_name']=='Substitution']
    sub_list = subs.substituted_player_name.dropna().unique().tolist()
    all_players = lu+sub_list
    return lu,all_players
    
def AddLineup(df_event_gps,lineup):
    #Adding the lineup
    lineup = [x.split(' ')[-1] for x in lineup]
    lineup = [x.replace('ć','c') for x in lineup]
    #setting the starting XI as lineup for all match, subs will bechanged later
    df_event_gps['lineup'] = [lineup]*len(df_event_gps)
    
    #Getting the index of the substitution from Servette
    sub_index = dict()#entering player
    out_index = dict()#exiting player
    
    for index,row in df_event_gps.iterrows():
        if len(row['event_type_name'])==0:
            continue
        if 'Substitution' in row.event_type_name and 'Servette' in row.team_name:
            print(index)
            sub_index[index] = row.substituted_player_name[0].split(' ')[-1]
            out_index[index] = row.player_name[0].split(' ')[-1]
    
    for key in sub_index.keys():
        print(lineup)
        new_lineup = [sub_index[key] if out_index[key]==x else x for x in lineup]
        #Changing the lineup based on new player and index in the DF
        df_event_gps.at[df_event_gps.index>=key,'lineup'] = pd.Series([new_lineup]*len(df_event_gps))
        lineup = new_lineup
    return df_event_gps

def CleanUpList(df_event_gps):
    for c in df_event_gps.columns:
        if df_event_gps.dtypes[c]==np.object and c!='timestamp':
            print(c)
            df_event_gps[c] = [ [] if x is np.NaN else x for x in df_event_gps[c] ]    
    return df_event_gps

def CheckPlayer(pl,row,col):
    if pl in row['lineup']:
        return row[col]
    else:
        return np.NaN
    
def SetNanBench(df_event_gps,all_players):
    for pl in all_players:
        pl_surname = pl.split(' ')[-1]
        print(pl_surname)
        col = ['X_'+pl_surname,'Y_'+pl_surname,'Direction_'+pl_surname,'Speed_'+pl_surname]
        for c in col:
            try:
                df_event_gps[c] = df_event_gps.apply(lambda row: CheckPlayer(pl_surname,row,c), axis=1)
            except KeyError:
                continue

    return df_event_gps

def GetStretchIndex(df_event_gps):
    
    #Selecting columns with 'X_*' to calculate x_centroid
    mask = df_event_gps.columns.str.contains('X_*')
    df_X = df_event_gps.loc[:,mask]
    df_event_gps['Centroid_X'] = df_X.mean(axis=1,skipna=True)
    df_X['Centroid'] = df_X.mean(axis=1,skipna=True)
    
    #Calculating the Stretch Index of every single player, defined as x-position of the player - the x-centroid position
    mask = df_X.columns.str.contains('X_*')
    for c in df_X.loc[:,mask].columns:
        print(c.split('_')[1])
        df_event_gps['SIx_'+c.split('_')[1]] = df_X[c] - df_X['Centroid']
        
    #Selecting columns with 'Y_*' to calculate x_centroid
    mask = df_event_gps.columns.str.contains('Y_*')
    df_Y = df_event_gps.loc[:,mask]
    df_event_gps['Centroid_Y'] = df_Y.mean(axis=1,skipna=True)
    df_Y['Centroid'] = df_Y.mean(axis=1,skipna=True)
    
    #Calculating the Stretch Index of every single player, defined as y-position of the player - the y-centroid position
    mask = df_Y.columns.str.contains('Y_*')
    for c in df_Y.loc[:,mask].columns:
        print(c.split('_')[1])
        df_event_gps['SIy_'+c.split('_')[1]] = df_Y[c] - df_Y['Centroid']
    
    SI = []
    SI_x = []
    SI_y = []
    #calculate StretchIndex
    for index,row in df_event_gps.iterrows():
        lu = row.lineup
        numerator = 0
        num_x = 0
        num_y = 0
        num_pl = 0
        for l in lu:
            if l=='Frick': #Ignoring Frick,no GPS Data
                continue
            if np.isnan(row['X_'+l]) or np.isnan(row['Y_'+l]):#skipping player if its GPS data is NaN
                #print("Skipping "+l)
                continue
            numerator += math.sqrt( math.pow((row['X_'+l] - row.Centroid_X),2) +  math.pow((row['Y_'+l] - row.Centroid_Y),2))
            num_x += math.fabs((row['X_'+l] - row.Centroid_X))
            num_y += math.fabs((row['Y_'+l] - row.Centroid_X))
            num_pl+=1
        #Checking to have at least 1 player position, otherwise division by zero and the universe will collapse
        if num_pl!=0:
            SI.append(numerator/num_pl)
            SI_x.append(num_x/num_pl)
            SI_y.append(num_y/num_pl)
        else:
            SI.append(np.NaN)
            SI_x.append(np.NaN)
            SI_y.append(np.NaN)
    
    df_event_gps['StretchIndex'] = SI
    df_event_gps['StretchIndex_x'] = SI_x
    df_event_gps['StretchIndex_y'] = SI_y
    
    return df_event_gps