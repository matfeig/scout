#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 11:26:03 2021

@author: matfeig
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:27:43 2020

@author: matfeig
"""
import pandas as pd
import matplotlib.pyplot as plt
#import plotly.graph_objects as go
import matplotlib.patches as patches
import numpy as np
from mplsoccer.pitch import Pitch


def getShotDF(df,team):
    list_df = []
    list_poss = [] #storing the possessions number to avoid to take the same shots multiple times
    for index, row in df.iterrows():
        if(row['possession'] in list_poss):
            continue
        if(row['event_type_name']=='Shot' and row['team_name']==team):
            possession = row['possession']
            tmp_df = df.loc[(df['possession']==possession) & (df['freeze_frame_player_id']==0) & (df['team_name']==team) & (df['outcome_name']!='Incomplete')]
            list_poss.append(possession)
            list_df.append(tmp_df)
            print(list_poss)
    return list_df

def plotPassages(list_df_shots,shirt_color,nr_color):  
    list_subdf = []
    i=0
    for tmp_df in list_df_shots:
            ### Plotting ###
            df_shot = tmp_df
            df_shot['carry_length'] = np.sqrt(np.power((df['location_x']-df['end_location_x']),2) + np.power((df['location_y']-df['end_location_y']),2))
            
            df_shot = df_shot.reset_index(drop=True)
            l = df_shot[(df_shot['type_name']=='Recovery')].index.tolist()
            if(len(l)>0):
                df_shot = df_shot[df_shot.index>=l[-1]]
            list_subdf.append(df_shot)
            l = df_shot[(df_shot['event_type_name']=='Ball Recovery')].index.tolist()
            if(len(l)>0):

                df_shot = df_shot[df_shot.index>=l[-1]]
            df_shot = df_shot[(df_shot['event_type_name']=="Pass") | ((df_shot['event_type_name']=="Carries") & (df_shot['carry_length']>3)) | (df_shot['event_type_name']=="Shot")]
#    
#            fig=plt.figure()
#            ax1=fig.add_subplot(1,1,1)
#            draw_pitch(ax1)
#            
            pitch = Pitch(pitch_type='statsbomb', figsize=(8, 4))  # example plotting a sch
            fig, ax1 = pitch.draw()
            
            ax1.scatter(df_shot['location_x'],df_shot['location_y'],c=shirt_color,s=120,zorder=3)
           # ax1.set_facecolor('xkcd:green') 
    
            df_shot = df_shot.reset_index(drop=True)

            for index, row in df_shot.iterrows():

                if(row['event_type_name']=="Pass"):
                    if((row['end_location_x']==df_shot['location_x'].iloc[index+1]) & (row['end_location_y']==df_shot['location_y'].iloc[index+1])):
                        ax1.arrow(row['location_x'],row['location_y'],row['end_location_x']-row['location_x'],row['end_location_y']-row['location_y'],width=0.1,color="black",head_width=0.8)
                    else:
                        ax1.arrow(row['location_x'],row['location_y'],df_shot['location_x'].iloc[index+1]-row['location_x'],df_shot['location_y'].iloc[index+1]-row['location_y'],width=0.1,color="black",head_width=0.8)
                if(row['event_type_name']=="Carries"):
                    if((row['end_location_x']==df_shot['location_x'].iloc[index+1]) & (row['end_location_y']==df_shot['location_y'].iloc[index+1])):
                        ax1.arrow(row['location_x'],row['location_y'],row['end_location_x']-row['location_x'],row['end_location_y']-row['location_y'],width=0.1,color="black",head_width=0.8,linestyle=":")
                    else:
                        ax1.arrow(row['location_x'],row['location_y'],df_shot['location_x'].iloc[index+1]-row['location_x'],df_shot['location_y'].iloc[index+1]-row['location_y'],width=0.1,color="black",head_width=0.8,linestyle=":")
                if(row['event_type_name']=="Shot"):
                    ax1.arrow(row['location_x'],row['location_y'],row['end_location_x']-row['location_x'],row['end_location_y']-row['location_y'],width=0.1,color="red",head_width=0.8,linestyle=":")
                text = str(int(jersey_num[row['player_name']][0]))
                if(int(jersey_num[row['player_name']][0])>9):
                    ax1.annotate(text, (row['location_x']-1.8, row['location_y']+1.0),zorder=4,fontsize=8.5,color=nr_color,weight='bold')
                else:
                    ax1.annotate(text, (row['location_x']-1., row['location_y']+1.0),zorder=4,fontsize=8.5,color=nr_color,weight='bold')
    
            ax1.set_xlim(-1,121)   
            ax1.set_ylim(81,-1)  
            #fig.savefig("Team_Shot_"+str(i)+'.pdf')
            i+=1
        
path = '/Users/matfeig/Dropbox/SFC/Database/Dataevent/'

df = pd.read_csv(path+'stg_zur_bomb.csv')
df['freeze_frame_player_id'] = df['freeze_frame_player_id'].replace(np.nan,0)
df['formation_jersey_number'] = df['formation_jersey_number'].replace(np.nan,0)
#df['location_x'] = df['location_x'] *
#df['location_y'] = df['location_y'] * 68./80.
#df['end_location_x'] = df['end_location_x'] * 105./120.
#df['end_location_y'] = df['end_location_y'] * 68./80.
df['type_name'] = df['type_name'].replace(np.nan,"")


list_df_shots = getShotDF(df,'St. Gallen')

jersey_num = df[df['formation_jersey_number']!=0][['formation_player_name','formation_jersey_number']]
jersey_num = jersey_num.set_index('formation_player_name').T.to_dict('list')
### players from the bench need to be added by hand...stupid Statsbomb
##Zurich
jersey_num['Alessio Besio'] = '27'
jersey_num['Basil Stillhart'] = '11' 
jersey_num['Boris Babic'] = '11'
jersey_num['Kwadwo Duah'] = '19' 
plotPassages(list_df_shots,"darkred","white")