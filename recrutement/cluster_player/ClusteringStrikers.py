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


df_fw = pd.read_csv("df_2020_vf.csv")

#df_fw = df_fw.loc[df_fw['Pos'].str.contains("FW", case=False)]

df_fw = df_fw[ (df_fw.Pos == 'FW') | (df_fw.Pos == 'FW,MF') | (df_fw.Pos == 'FW,DF')]

#df_fw = df_fw[df_fw['Comp']!='Super League']

df_input = df_fw[['Comp','xG','Shots','Dispossessed','Turnovers','Deep Progressions','Carries','Dribbles','Successful Dribbles','Touches In Box','Successful Crosses','PintoB','Key Passes','xG Assisted','Assists','OP Assists','OP Key Passes','Aerial Wins','Passes Inside Box']]

#Less variables here
#df_input = df_fw[['Comp','Shots','Shooting%','Dispossessed','Carries','Dribbles','Successful Dribbles','Touches In Box','PintoB','Key Passes','xG Assisted','Assists','OP Assists','OP Key Passes','Pressures']]

df_input = df_input.replace(np.nan,0)

#Try to rescale each league separately
ss = StandardScaler()

df_seriea = df_input[df_input['Comp']=='it Serie A']
df_seriea.drop(columns=['Comp'],inplace=True)
df_scaled_seriea = pd.DataFrame(ss.fit_transform(df_seriea),columns = df_seriea.columns,index=df_seriea.index)

df_pl = df_input[df_input['Comp']=='eng Premier League']
df_pl.drop(columns=['Comp'],inplace=True)
df_scaled_pl = pd.DataFrame(ss.fit_transform(df_pl),columns = df_pl.columns,index=df_pl.index)

df_bundes = df_input[df_input['Comp']=='de Bundesliga']
df_bundes.drop(columns=['Comp'],inplace=True)
df_scaled_bundes = pd.DataFrame(ss.fit_transform(df_bundes),columns = df_bundes.columns,index=df_bundes.index)

df_ligue1 = df_input[df_input['Comp']=='fr Ligue 1']
df_ligue1.drop(columns=['Comp'],inplace=True)
df_scaled_ligue1 = pd.DataFrame(ss.fit_transform(df_ligue1),columns = df_ligue1.columns,index=df_ligue1.index)

df_liga = df_input[df_input['Comp']=='es La Liga']
df_liga.drop(columns=['Comp'],inplace=True)
df_scaled_liga = pd.DataFrame(ss.fit_transform(df_liga),columns = df_liga.columns,index=df_liga.index)

df_super = df_input[df_input['Comp']=='Super League']
df_super.drop(columns=['Comp'],inplace=True)
df_scaled_super = pd.DataFrame(ss.fit_transform(df_super),columns = df_super.columns,index=df_super.index)

df_scaled = pd.concat([df_scaled_seriea,df_scaled_bundes,df_scaled_liga,df_scaled_ligue1,df_scaled_pl,df_scaled_super])

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

df_scaled['Player'] = df_fw['Player']
df_scaled['Squad'] = df_fw['Squad']

df_scaled['Comp'] = df_fw['Comp']


df_input['Player'] = df_fw['Player']
df_input['Squad'] = df_fw['Squad']

df_input['Comp'] = df_fw['Comp']


df_scaled.to_excel('fw_kmeans.xlsx')

df_input['Player'] = df_fw['Player']
df_input['Squad'] = df_fw['Squad']

df_input['Comp'] = df_fw['Comp']

df_input.to_excel('fw_kmeans_absvalues.xlsx')


######
color = ['blue','brown','purple','red','orange','green']

df_avg = df_scaled.drop(columns=['Player','Squad','Comp'])

df_mean_out = pd.DataFrame()


#Calculate avg value of each variables in the clusters
for c in df_avg.columns:
    vec = []
    cluster = []
    #f1 = plt.figure()
    #plt.title(c)
    for k in range(0,6):
        f1 = plt.figure()
        plt.title(c+' for cluster '+str(k)) 
        vec.append(df_avg[df_avg['k_means']==k][c].mean())
        cluster.append(k)
        #Plot histograms
      
        #df_avg[df_avg['k_means']==k][c].plot(kind='hist',alpha=0.3)
        plt.hist(df_avg[df_avg['k_means']==k][c],edgecolor = color[k], fill=False,histtype='step',density=True)
        #plt.savefig('Plots/HistogramsAllClusters_'+c+'.pdf')
        #plt.savefig('Plots/Clusters'+str(k)+'_'+c+'.pdf')
    df_mean_out[c] = vec

df_mean_out['Cluster'] = cluster
df_mean_out.to_excel("MidfCluster.xlsx")


