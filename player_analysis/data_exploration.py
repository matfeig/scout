# -*- coding: utf-8 -*-
"""
Created on Sun May 31 13:33:38 2020

@author: monte
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

### Open csv player stats statsbomb ##
df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/player_analysis/data_antunes.csv")

### Plot distribution d'une variable ###
plt.hist(df['Minutes'], rwidth=0.8)
plt.xlabel('Minutes', fontsize=20)
plt.ylabel('frequency', fontsize=20)
plt.show()


############ Plot distribution  ############
df = pd.read_excel("/Users/matfeig/Dropbox/SFC/Code/Index/indax.xlsx")
sns.countplot(x="indexx", data=df)
sns.displot(df, x="indexx", binwidth=10)
sns.displot(df, x="indexx", hue="name",kind="kde")

############ Plot Mean std  ############
mean = df.groupby('name').mean()
mean = mean.sort_values('indexx', ascending = False)
ax = sns.catplot(x="name",y="indexx", hue="MATCH DATE", data=df, kind="bar",ci=None, height=10)
ax.set_axis_labels('Joueurs SFC', 'Index Moyen')
ax.set(ylim=(170, 270))
ax.set_xticklabels(rotation=90)

############ Plot Mean std  ############
mean = df.groupby('name').mean()
mean = mean.sort_values('indexx', ascending = False)
ax = sns.catplot(x="name",y="MINS PLAYED", hue="MATCH DATE", data=df, kind="bar",ci=None, height=10)
ax.set_axis_labels('Joueurs SFC', 'Index Moyen')
ax.set(ylim=(170, 270))
ax.set_xticklabels(rotation=90)

####### Plot For a Player ######
saison = df.loc[(df['name'] == "Holcbecher Mathis Jan")]
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(saison.MATCH, saison["indexx"], width=0.8, bottom=True) 
ax.set(ylim=(220, 350))
ax.set_xticklabels(saison.date, rotation = 90) 
ax.set_ylabel("Index")
plt.show()


df1 = pd.read_csv("/Users/matfeig/Dropbox/SFC/Code/Index/player_info.csv")
fig, ax = plt.subplots(figsize=(10,5))
ax.bar(df1.Name, df1["Appearances"], width=0.8, bottom=True) 
ax.set(ylim=(0, 28))
ax.set_xticklabels(df1.Name, rotation = 90) 
ax.set_ylabel("Nombre d'apparition")
plt.show()


data = pd.read_csv('player.csv', delimiter=';')
data.head()

df_sorted = data.sort_values('Minutes', ascending=False)
df_sorted.plot.bar(x='Name', y='Minutes jouées', rot=90)
df_sorted.plot.bar(x='Name', y='InStat Index', rot=90)

data['index'] = data['InStat Index'].astype(int)



ax = sns.catplot(data=saison,kind='bar', y="indexx",hue="MATCH DATE", ci=95)
ax.set_xticklabels(rotation=90)



fig = plt.figure(figsize=(8, 5))
plt.bar(df, index, color='blue', width=0.4)
plt.yticks(rotation=45)
plt.xlabel("Names")
plt.ylabel("Age of the person")
plt.show()



############ Bilan de la league   ############



index = sns.load_dataset('indax')

sns.displot(best_index, x="INSTAT INDEX")



cognat = best_index.sort_index()
print (cognat)
print (cognat.loc["Timothe Cognat"])


short_df = df[["LAST NAME", "index"]]
print (short_df)
index_top = df[df['index'] > 270]
print (index_top)


Sasso = df["LAST NAME"] == "Sasso Vincent"
print (Sasso)

############ Suppression des NaN ############
 #= data.dropna() 
 
 
 ### Selectionner un nomber de row et column à traiter ####
 print (df.iloc[0:5,1:3])
 
 
 # Ajouter un column au dataframe
#df['x'] = dictionnary

# Pivot index by Player  year vs Match 
df_pivot = df.pivot_table("INSTAT INDEX", index='LAST NAME', columns='MATCH')
print (df_pivot)

#Subset le dataframe
df_pivot_subset = df_pivot.loc['Rouiller Steve':'Vouilloz Nicolas']
print (df_pivot_subset)

df_pivot_sub = df.loc[('Sasso Vincent', 'On average(90 mins)'):('Diallo Moussa','On average(90 mins)')]
print (df_pivot_sub)


##Supprimer un columns dans le data Frame"
del df_pivot_subset ['Total']
del df_pivot_subset ['On average(90 mins)']


##Calculer la moyenne pour chaque joueur###
mean_player = df_pivot_subset.mean(axis="columns")
print (mean_player)


##Calculer la moyenne pour chaque match###
mean_game = df_pivot_subset.mean(axis="index")
 

### Vizualisation ###

df_pivot_subset.hist()
df_pivot_subset.plot(kind='bar')
plt.show()

mean_player.hist()
mean_player.plot(kind='bar')
plt.show()

rouiller = df.groupby('LAST NAME')
print (rouiller)

fig, ax = plt.subplots()
ax.bar("Index", df["INSTAT INDEX"].mean())
plt.show()