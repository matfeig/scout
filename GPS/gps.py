#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 08:41:09 2022

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import seaborn as sns
import matplotlib.patches as mpatches
from colour import Color
import matplotlib.colors as mcolors
from highlight_text import fig_text


###############################
######### GPS Load  ###########
###############################

data= pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/GPS/sfc_gc_1.csv")
data = data.rename(columns={'Distance (m)': 'distance'})
data = data.sort_values(by='distance',ascending=False)
data = data.reset_index()
data.drop(data[data['Name'] =='Lois Ndema'].index, inplace = True)
data.drop(data[data['Name'] =='Baba Souare'].index, inplace = True)                 
data.drop(data[data['Name'] =='Sidiki Camara'].index, inplace = True)  
data.drop(data[data['Name'] =='Steve Rouiller'].index, inplace = True)  

data1= pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/GPS/luz_sfc_1.csv")
data1 = data1.rename(columns={'Distance (m)': 'distance'})
data1 = data1.sort_values(by='distance',ascending=False)
data1 = data1.reset_index()
data1.drop(data1[data1['Name'] =='Lois Ndema'].index, inplace = True)
data1.drop(data1[data1['Name'] =='Alexandre Dias'].index, inplace = True)                 
data1.drop(data1[data1['Name'] =='Sidiki Camara'].index, inplace = True)  
data1.drop(data1[data1['Name'] =='Diogo Monteiro'].index, inplace = True)  

######               
df1 = [['Miroslav Stevanovic', 28961], 
       ['Timothe Cognat', 28967], 
       ['Yoan Severin', 29460],
       ['David Douline', 7597], 
       ['Nicolas Vouilloz', 41654], 
       ['Ronny Rodelin', 2955],
       ['Alexis Antunes', 48493], 
       ['Gael Clichy', 20302], 
       ['Patrick Pflucke', 46208],
       ['Moritz Bauer', 3622], 
       ['Theo Valls', 7314],
       ['Steve Rouiller', 28965],
       ['Moussa Diallo', 7502],
       ['Samba Lele Diba', 286843],
       ['Baba Souare', 49033], 
       ['Enzo Crivelli',3184],
       ['Kutesa Dereck', 29225], 
       ['Boubacar Fofana', 24889]]
df2 = pd.DataFrame(df1, columns=['Name', 'player_id'])
df3 = df2.merge(data, left_on='Name', right_on='Name')
########

df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/player_match/sfc_gc_1.csv")
df.columns = df.columns.map(lambda x: x.removeprefix("player_match_"))
df = df.replace(np.nan,0)
df = df[(df['team_name'] =="Servette")]

data = df3.merge(df, left_on='player_id', right_on='player_id')




data = pd.concat([data, data1])



##### Calcul #####
##################

data['ratio'] = data['distance'] / data['minutes']



### plot Distance par minute ####
#################################

data = data.sort_values(by='ratio',ascending=False)

fig = plt.figure(figsize=(16, 9), dpi = 200, facecolor = "#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")
sns.barplot(data['Name'], data['ratio'], palette="viridis_r")
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)
plt.axhline(y=data.ratio.mean(),color='Grey')
fig_text(0.83,0.55,"Moyenne", color = "Grey",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
plt.axhline(y=data.ratio.median(),color='Grey')
fig_text(0.83,0.67,"Median", color = "Grey",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
plt.yticks(fontsize=12,fontweight = "bold")
plt.xticks(fontsize=12,fontweight = "bold")
plt.xlabel("",fontsize = 20, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("Distance (m)",fontsize = 15, fontweight = "bold", color = "black")
plt.xticks(rotation = 80)
plt.title ('Distance par Joueur', fontsize=20,fontweight = "bold")



### plot Distance ####
######################

data = data.sort_values(by='distance',ascending=False)

fig = plt.figure(figsize=(16, 9), dpi = 200, facecolor = "#EFE9E6")
ax = plt.subplot(111, facecolor = "#EFE9E6")
sns.barplot(data['Name'], data['distance'], palette="viridis_r")
ax.spines["top"].set(visible = False)
ax.spines["right"].set(visible = False)
plt.axhline(y=data.distance.mean(),color='Grey')
fig_text(0.83,0.55,"Moyenne", color = "Grey",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
plt.axhline(y=data.distance.median(),color='Grey')
fig_text(0.83,0.67,"Median", color = "Grey",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
plt.yticks(fontsize=12,fontweight = "bold")
plt.xticks(fontsize=12,fontweight = "bold")
plt.xlabel("",fontsize = 20, fontweight = "bold", color = "black", labelpad=15)
plt.ylabel("Distance (m)",fontsize = 15, fontweight = "bold", color = "black")
plt.xticks(rotation = 80)
plt.title ('Distance par Joueur', fontsize=20,fontweight = "bold")