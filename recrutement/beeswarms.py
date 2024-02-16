#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 14:17:30 2021

@author: matfeig
"""

#https://github.com/ciaran-grant/fbref_data/blob/master/FBRef%20-%20%20Progressive%20Passes.ipynb
#https://github.com/mckayjohns/Viz-Templates

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

import highlight_text
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# the famous import font code to use Andale Mono
import matplotlib.font_manager
from IPython.core.display import HTML

def make_html(fontname):
    return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])


data = pd.read_csv("df.csv")

## Selectionner les positions pour faire le beeswarms
data= data.loc[(data.primary_position == "Centre Forward")|(data.primary_position == "Left Centre Forward")|(data.primary_position == "Right Centre Forward")|
           (data.secondary_position == "Centre Forward")|(data.secondary_position == "Left Centre Forward")|(data.secondary_position == "Right Centre Forward")|
           (data.primary_position == "Left Wing")|(data.primary_position == "Right Wing")|(data.primary_position == "Centre Attacking Midataielder")|
           (data.primary_position == "Left Attacking Midataielder")|(data.primary_position == "Right Attacking Midataielder")]

## Selectionner les leagues
#data = data.loc[(data.competition_name == "Bundesliga")|(data.primary_position == "Super League")]

##Selectiionner le nombre de minutes minameles joueur pour rentrer dans l'analyse minutes de jeu##
data=data.loc[(data.player_season_minutes>=300)]

#set default colors
text_color = 'black'
background = 'white'

#%%

##### Plot pour un single player #####
####                             ####
# fig, ax = plt.subplots(figsize=(10,5))
# fig.set_facecolor(background)
# ax.patch.set_facecolor(background)

# data = data.sort_values(by='player_name',ascending=False)

# #set up our base layer
# mpl.rcParams['xtick.color'] = text_color
# mpl.rcParams['ytick.color'] = text_color

# ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
# spines = ['top','bottom','left','right']
# for x in spines:
#     if x in spines:
#         ax.spines[x].set_visible(False)
# sns.swarmplot(x='player_season_np_xg_90',data=data,color='grey',zorder=1)

# #plot 
# plt.scatter(x=0.6,y=0,c='red',edgecolor='white',s=150,zorder=2)
# plt.text(s='player_name',x=0.6,y=-.04,c=text_color)

# plt.title('xG Super League 2020/21',c=text_color,fontsize=14)
# plt.xlabel('xG per 90',c=text_color)

#%%
### Important ###
print(data.head())
data.player_name.unique()
data = data.reset_index()

####
####
#### Occasions de buts #######
####
####

metrics = ['player_season_np_xg_90','player_season_np_psxg_90','player_season_np_shots_90','player_season_dribbles_90','player_season_obv_dribble_carry_90','player_season_carries_90']

fig,axes = plt.subplots(3,2,figsize=(10,9))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['player_name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['player_name'])):
         if data['player_name'][x] == 'Patrick Pflüke':
             ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
         if data['player_name'][x] == 'Boubacar Fofana':
             ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
         if data['player_name'][x] == 'Ronny Rodelin':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)  
         if data['player_name'][x] == 'Miroslav Stevanović':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
         if data['player_name'][x] == 'Derek Kutesa':
             ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)                                
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquants Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=45, y=.88, #highlight_weights = ['bold'],
                fontsize=15,
                fontfamily = '',
                color = text_color,
                #highlight_colors = ['#6CABDD'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='',color=text_color)
#plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)


####
####
#### Contributions offensive Attaquant  #######
####
####

metrics = ['Deep Progressions','xGChain','OP F3 Passes','OP Passes Into Box','F3 Pass Forward%','Carry Length']

fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['Name'])):
        if data['Name'][x] == 'Alex Schalk':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Boubacar Fofana':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        if data['Name'][x] == 'Grejohn Kyei':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        if data['Name'][x] == 'Koro Koné':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        if data['Name'][x] == 'Miroslav Stevanović':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        if data['Name'][x] == 'Kastriot Imeri':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
        if data['Name'][x] == 'Alexis Antunes':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['#6CABDD'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)


####
####
#### Contributions Défensive Attaquant  #######
####
####

metrics = ['Aggressive Actions','Defensive Regains','PAdj Pressures','Counterpressures','Counterpressures F2','Interceptions']

fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['Name'])):
        if data['Name'][x] == 'Alex Schalk':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Boubacar Fofana':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        if data['Name'][x] == 'Grejohn Kyei':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        if data['Name'][x] == 'Koro Koné':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        if data['Name'][x] == 'Miroslav Stevanović':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        if data['Name'][x] == 'Kastriot Imeri':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
        if data['Name'][x] == 'Alexis Antunes':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['#6CABDD'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)


####
#### Occasions de buts Milieu de terrain #######
####
####

metrics = ['All Goals','xG','Shots','Assists','Key Passes','Scoring Contribution']

fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['Name'])):
        if data['Name'][x] == 'Timothé Cognat':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Théo Valls':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        if data['Name'][x] == 'Kastriot Imeri':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        if data['Name'][x] == 'Alexis Antunes':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        if data['Name'][x] == 'Gaël Ondoua':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        if data['Name'][x] == 'Boris Cespedes':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
#        if data['Name'][x] == 'Alexis Antunes':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['#6CABDD'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)



####
####
#### Contributions offensive Milieu  #######
####
####

metrics = ['Deep Progressions','xGChain','OP F3 Passes','OP Passes Into Box','F3 Pass Forward%','Carry Length']

fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['Name'])):
        if data['Name'][x] == 'Timothé Cognat':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Théo Valls':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        if data['Name'][x] == 'Kastriot Imeri':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        if data['Name'][x] == 'Alexis Antunes':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        if data['Name'][x] == 'Gaël Ondoua':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        if data['Name'][x] == 'Boris Cespedes':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
#        if data['Name'][x] == 'Alexis Antunes':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['#6CABDD'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)


####
####
#### Contributions Défensive Milieu  #######
####
####

metrics = ['Aggressive Actions','Defensive Regains','PAdj Pressures','Counterpressures','Counterpressures F2','Interceptions']

fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['Name'])):
        if data['Name'][x] == 'Timothé Cognat':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Théo Valls':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        if data['Name'][x] == 'Kastriot Imeri':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        if data['Name'][x] == 'Alexis Antunes':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        if data['Name'][x] == 'Gaël Ondoua':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        if data['Name'][x] == 'Boris Cespedes':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
#        if data['Name'][x] == 'Alexis Antunes':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['#6CABDD'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)


####
####
#### Contributions offensive Défenseeur  #######
####
####

metrics = ['Deep Progressions','xGChain','OP F3 Passes','OP Passes Into Box','F3 Pass Forward%','Carry Length']

fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['Name'])):
        if data['Name'][x] == 'Anthony Sauthier':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Gaël Clichy':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        if data['Name'][x] == 'Steve Rouiller':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        if data['Name'][x] == 'Moussa Diallo':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        if data['Name'][x] == 'Yoan Severin':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        if data['Name'][x] == 'Vincent Sasso':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
        if data['Name'][x] == 'Arial Mendy':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['#6CABDD'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)


####
####
#### Contributions Défensive Defenseur  #######
####
####

#metrics = ['Aggressive Actions','Defensive Regains','PAdj Pressures','Counterpressures','Counterpressures F2','Interceptions']
#metrics = ['PAdj Clearances','Aerial Win%','Average DA X','PAdj Tack&Int','Interceptions','Dribbled Past']
metrics = ['Deep Progressions','xGChain','OP F3 Passes','OP Passes Into Box','F3 Pass Forward%','Carry Length']


fig,axes = plt.subplots(3,2,figsize=(16,9))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
#mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.2,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#870E26')
    ax.set_xlabel(f'{metrics[met_counter]}',c='black')
    
    for x in range(len(data['Name'])):
        # if data['Name'][x] == 'Anthony Sauthier':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Gaël Clichy':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=120,c='Blue',zorder=2)
        # if data['Name'][x] == 'Steve Rouiller':
        #    ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        # if data['Name'][x] == 'Moussa Diallo':
        #    ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        # if data['Name'][x] == 'Yoan Severin':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        # if data['Name'][x] == 'Vincent Sasso':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
        # if data['Name'][x] == 'Arial Mendy':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['black'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color='black')
# plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)


####
####
#### Spécifique Defenseur  #######
####
####

metrics = ['PAdj Clearances','Aerial Win%','Average DA X','PAdj Tack&Int','Dribbles Stopped%','Dribbled Past']

fig,axes = plt.subplots(3,2,figsize=(14,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='white')
    
    for x in range(len(data['Name'])):
        # if data['Name'][x] == 'Anthony Sauthier':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Gaël Clichy':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        # if data['Name'][x] == 'Steve Rouiller':
        #    ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        # if data['Name'][x] == 'Moussa Diallo':
        #    ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        # if data['Name'][x] == 'Yoan Severin':
            # ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        # if data['Name'][x] == 'Vincent Sasso':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
        # if data['Name'][x] == 'Arial Mendy':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['black'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)

###
####
###
##


#metrics = ['Aggressive Actions','Defensive Regains','PAdj Pressures','Counterpressures','Counterpressures F2','Interceptions']

## Spé def centraux
#metrics = ['PAdj Clearances','Aerial Win%','Dribbles Stopped%', 'Dribbled Past', 'PAdj Tack&Int','Fouls']

## Spé lat&éraux 
#metrics = ['PAdj Interceptions','Dribbles Stopped%','Pressure Regains','Deep Progressions','F3 Pass Forward%','Successful Crosses']

## 6
#metrics = ['PAdj Tack&Int','Aggressive Actions','Long Ball%','Passes Pressured%','Pass Forward%','xGBuildup']

## GK
#metrics = ['GSAA','Save%','xSv%','Shots Faced','xG Faced','PSxG Faced']
#metrics = ['Long Ball%','Average Pass X','Pass Length','L/R Footedness%','Passing%','Long Balls']

# 8
metrics = ['xG & xG Assisted','Shots & Key Passes','Shots','Passes Inside Box','Touches In Box', 'Dispossessed']

fig,axes = plt.subplots(3,2,figsize=(16,9))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
#mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0 
counter2=0
met_counter = 0

for i,ax in zip(data['Name'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.2,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='grey')
    ax.set_xlabel(f'{metrics[met_counter]}',c='black')
    
    for x in range(len(data['Name'])):
        # if data['Name'][x] == 'Anthony Sauthier':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightskyblue',zorder=2)
        if data['Name'][x] == 'Grejohn Kyei':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=120,c='#870E26',zorder=2)
        if data['Name'][x] == 'Alex Schalk':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)
        # if data['Name'][x] == 'Moussa Diallo':
        #    ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='yellow',zorder=2)              
        # if data['Name'][x] == 'Yoan Severin':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)
        # if data['Name'][x] == 'Vincent Sasso':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='red',zorder=2)       
        # if data['Name'][x] == 'Arial Mendy':
        #     ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='deeppink',zorder=2)
#        if data['Name'][x] == 'Koro Koné':
#            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='blue',zorder=2)                           
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
s='<Attaquant Super League - Occasions de buts'
highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                highlight_colors = ['black'],
                va='center'
               )
    
fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color='black')
# plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background