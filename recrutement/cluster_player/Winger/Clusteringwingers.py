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


df_fw = pd.read_csv("wingers.csv")


#df_input = df_fw[['Competition',, 'Successful Dribbles', 'Dispossessed', 'Turnovers','Touches In Box', 'Post Shot xG','Shots', 'xG','xG/Shot','Aggressive Actions','Counterpressures','Pressures','Ball Recoveries','Dribble & Carry OBV','Pass OBV','Open Play xG Assisted','OP Passes Into Box','Passes Inside Box','Successful Crosses','Throughballs','Carries','Deep Progressions']]

#Without setpieces
#df_input = df_fw[['Competition', 'Successful Dribbles','Dribble & Carry OBV','Carries', 'Dispossessed', 'Turnovers','Touches In Box', 'Post Shot xG','Shots', 'xG','xG/Shot','Aggressive Actions','Counterpressures','Pressures','Ball Recoveries','Pass OBV','Open Play xG Assisted','OP Passes Into Box','Passes Inside Box','Successful Crosses','Throughballs']]
#Without defens
df_input = df_fw[['Competition', 'Successful Dribbles','Dribbles', 'Turnovers','Touches In Box', 'Post Shot xG','Shots', 'xG','Open Play xG Assisted','OP Passes Into Box','Successful Crosses','Throughballs']]


df_input = df_input.replace(np.nan,0)

#Try to rescale each league separately
ss = StandardScaler()

df_seriea = df_input[df_input['Competition']=='Primeira Liga']
df_seriea.drop(columns=['Competition'],inplace=True)
df_scaled_seriea = pd.DataFrame(ss.fit_transform(df_seriea),columns = df_seriea.columns,index=df_seriea.index)

df_pl = df_input[df_input['Competition']=='Eerste Divisie']
df_pl.drop(columns=['Competition'],inplace=True)
df_scaled_pl = pd.DataFrame(ss.fit_transform(df_pl),columns = df_pl.columns,index=df_pl.index)

df_ere = df_input[df_input['Competition']=='Eredivisie']
df_ere.drop(columns=['Competition'],inplace=True)
df_scaled_ere = pd.DataFrame(ss.fit_transform(df_ere),columns = df_ere.columns,index=df_ere.index)

df_ligue1 = df_input[df_input['Competition']=='La Liga 2']
df_ligue1.drop(columns=['Competition'],inplace=True)
df_scaled_ligue1 = pd.DataFrame(ss.fit_transform(df_ligue1),columns = df_ligue1.columns,index=df_ligue1.index)

df_liga = df_input[df_input['Competition']=='Challenge League']
df_liga.drop(columns=['Competition'],inplace=True)
df_scaled_liga = pd.DataFrame(ss.fit_transform(df_liga),columns = df_liga.columns,index=df_liga.index)

df_bundes = df_input[df_input['Competition']=='Bundesliga']
df_bundes.drop(columns=['Competition'],inplace=True)
df_scaled_bundes = pd.DataFrame(ss.fit_transform(df_bundes),columns = df_bundes.columns,index=df_bundes.index)

df_super = df_input[df_input['Competition']=='Super League']
df_super.drop(columns=['Competition'],inplace=True)
df_scaled_super = pd.DataFrame(ss.fit_transform(df_super),columns = df_super.columns,index=df_super.index)

df_lig = df_input[df_input['Competition']=='Ligue 2']
df_lig.drop(columns=['Competition'],inplace=True)
df_scaled_lig = pd.DataFrame(ss.fit_transform(df_lig),columns = df_super.columns,index=df_lig.index)


df_scaled = pd.concat([df_scaled_seriea,df_scaled_bundes,df_scaled_ere,df_scaled_liga,df_scaled_ligue1,df_scaled_pl,df_scaled_super, df_scaled_lig])

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

df_scaled['Name'] = df_fw['Name']
df_scaled['Team'] = df_fw['Team']

df_scaled['Competition'] = df_fw['Competition']


df_input['Name'] = df_fw['Name']
df_input['Team'] = df_fw['Team']

df_input['Competition'] = df_fw['Competition']


df_scaled.to_excel('wingers_kmeans.xlsx')

df_input['Name'] = df_fw['Name']
df_input['Team'] = df_fw['Team']

df_input['Competition'] = df_fw['Competition']

df_input.to_excel('wingers_kmeans_absvalues.xlsx')

######
######
#####
######
color = ['blue','brown','purple','red','orange','green']

df_avg = df_scaled.drop(columns=['Name','Team','Competition'])

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
df_mean_out.to_excel("wingerscluster.xlsx")


