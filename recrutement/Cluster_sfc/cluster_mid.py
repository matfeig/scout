#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 19:58:49 2021

@author: peter
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


df1 = pd.read_csv("austria.csv")
df2 = pd.read_csv("france.csv")
df3 = pd.read_csv("portugal.csv")
df4 = pd.read_csv("suisse.csv")
df5 = pd.read_csv("netherland.csv")

df = pd.concat([df1,df2,df3,df4,df5], ignore_index=True)
del df['Unnamed: 0']
df.drop(df.loc[df['primary_position']=='Goalkeeper'].index, inplace=True)

## Create the CSV based on all the league
df.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/df.csv')


## Selectionner les positions pour faire le cluster
df= df.loc[(df.primary_position == "Right Centre Midfielder")|(df.secondary_position == "Right Centre Midfielder")|
           (df.primary_position == "Right Defensive Midfielder")|(df.secondary_position == "Right Defensive Midfielder")|
           (df.primary_position == "Right Attacking Midfielder")|(df.secondary_position == "Right Attacking Midfielder")|
           (df.primary_position == "Centre Midfielder")|(df.secondary_position == "Centre Midfielder")|
           (df.primary_position == "Defensive Midfielder")|(df.secondary_position == "Defensive Midfielder")|
           (df.primary_position == "Attacking Midfielder")|(df.secondary_position == "Attacking Midfielder")|
           (df.primary_position == "Left Centre Midfielder")|(df.secondary_position == " Left Defensive Midfielder")|
           (df.primary_position == "Left Defensive Midfielder")|(df.secondary_position == "Left Centre Midfielder")|
           (df.primary_position == "Left Attacking Midfielder")|(df.secondary_position == "Left Attacking Midfielder")
           ]
#df.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/dfmid.csv')

##Selectiionner le nombre de minutes minameles joueur pour rentrer dans l'analyse minutes de jeu##
df=df.loc[(df.player_season_minutes>=300)]

## Choisir les variables désirées par méthode de data science 
#step wise
#Random Forest Feature Selection
#boruta

## Choisir manuellement les variables désirées 
# df_input = df[['competition_name',
#                'player_season_np_xg_90', 'player_season_xa_90',
#                'player_season_through_balls_90','player_season_op_passes_into_box_90',
#                'player_season_padj_tackles_90','player_season_padj_interceptions_90',
#                'player_season_dribbled_past_90','player_season_dispossessions_90',
#                'player_season_padj_clearances_90','player_season_aerial_wins_90',
#                'player_season_forward_pass_proportion','player_season_op_f3_passes_90',
#                'player_season_passing_ratio','player_season_op_xgchain_90',
#                'player_season_aggressive_actions_90','player_season_padj_pressures_90',
#                'player_season_pass_into_pressure_ratio','player_season_ball_recoveries_90',
#                'player_season_obv_pass_90','player_season_obv_defensive_action_90'              
#                 ]]

df_input = df[['competition_name',
               'player_season_np_xg_90', 'player_season_xa_90',   
               'player_season_padj_tackles_and_interceptions_90',
               'player_season_turnovers_90','player_season_pass_into_pressure_ratio',
               'player_season_forward_pass_proportion','player_season_op_f3_passes_90',
               'player_season_passing_ratio','player_season_op_passes_90',
               'player_season_unpressured_long_balls_90',
               'player_season_aggressive_actions_90','player_season_padj_pressures_90',
               'player_season_obv_pass_90','player_season_obv_defensive_action_90' ,
               'player_season_deep_progressions_90','player_season_carries_90',
                ]]

df_input = df_input.replace(np.nan,0)

#Try to rescale each league separately
ss = StandardScaler()

df_seriea = df_input[df_input['competition_name']=='Primeira Liga']
df_seriea.drop(columns=['competition_name'],inplace=True)
df_scaled_seriea = pd.DataFrame(ss.fit_transform(df_seriea),columns = df_seriea.columns,index=df_seriea.index)

df_pl = df_input[df_input['competition_name']=='Eerste Divisie']
df_pl.drop(columns=['competition_name'],inplace=True)
df_scaled_pl = pd.DataFrame(ss.fit_transform(df_pl),columns = df_pl.columns,index=df_pl.index)

df_bundes = df_input[df_input['competition_name']=='Bundesliga']
df_bundes.drop(columns=['competition_name'],inplace=True)
df_scaled_bundes = pd.DataFrame(ss.fit_transform(df_bundes),columns = df_bundes.columns,index=df_bundes.index)

df_ligue1 = df_input[df_input['competition_name']=='Ligue 2']
df_ligue1.drop(columns=['competition_name'],inplace=True)
df_scaled_ligue1 = pd.DataFrame(ss.fit_transform(df_ligue1),columns = df_ligue1.columns,index=df_ligue1.index)

df_super = df_input[df_input['competition_name']=='Super League']
df_super.drop(columns=['competition_name'],inplace=True)
df_scaled_super = pd.DataFrame(ss.fit_transform(df_super),columns = df_super.columns,index=df_super.index)

df_scaled = pd.concat([df_scaled_seriea,df_scaled_bundes,df_scaled_ligue1,df_scaled_pl,df_scaled_super])

distortions = []
K = range(1,20)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(df_scaled)
    distortions.append(kmeanModel.inertia_)
    
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()


### Add N_init####
kmeanModel = KMeans(n_clusters=6,n_init=100,random_state=0)
kmeanModel.fit(df_scaled)

df_scaled['k_means']=kmeanModel.predict(df_scaled)
df_input['k_means'] = df_scaled['k_means']

corr = df_scaled.corr()

df_scaled['player_name'] = df['player_name']
df_scaled['team_name'] = df['team_name']
df_scaled['competition_name'] = df['competition_name']


df_input['player_name'] = df['player_name']
df_input['team_name'] = df['team_name']
df_input['competition_name'] = df['competition_name']

df_scaled.to_excel('profil_kmeans.xlsx')

df_input['player_name'] = df['player_name']
df_input['team_name'] = df['team_name']
df_input['competition_name'] = df['competition_name']

df_input.to_excel('profil_kmeans_absvalues.xlsx')


######
color = ['blue','brown','purple','red','orange','green']

df_avg = df_scaled.drop(columns=['player_name','team_name','competition_name'])

df_mean_out = pd.DataFrame()


#Calculate avg value of each variables in the clusters
for c in df_avg.columns:
    vec = []
    cluster = []
    #f1 = plt.figure()
    #plt.title(c)
    for k in range(0,13):
        f1 = plt.figure()
        #plt.title(c+' for cluster '+str(k)) 
        vec.append(df_avg[df_avg['k_means']==k][c].mean())
        cluster.append(k)
        #Plot histograms
      
        #df_avg[df_avg['k_means']==k][c].plot(kind='hist',alpha=0.3)
        #plt.hist(df_avg[df_avg['k_means']==k][c],edgecolor = color[k], fill=False,histtype='step',density=True)
        #plt.savefig('Plots/HistogramsAllClusters_'+c+'.pdf')
        #plt.savefig('Plots/Clusters'+str(k)+'_'+c+'.pdf')
    df_mean_out[c] = vec

df_mean_out['Cluster'] = cluster
df_mean_out.to_excel("profil.xlsx")


