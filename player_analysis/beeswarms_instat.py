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

# the famous import font code to use Andale Mono
import matplotlib.font_manager
from IPython.core.display import HTML

def make_html(fontname):
    return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])

df = pd.read_csv('player_stats.csv')
df1 = pd.read_csv('player_stats-2.csv')
df2 = pd.read_csv('player_stats-3.csv')
df3 = pd.read_csv('player_stats-4.csv')
df4 = pd.read_csv('player_stats-5.csv')
data = pd.concat([df,df1,df2,df3,df4])
#data = pd.read_xlsx('airton.xlsx')

#set default colors
text_color = 'white'
background = '#313332'


##### Plot pour un single player #####
####                             ####
fig, ax = plt.subplots(figsize=(10,5))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

data = data.sort_values(by='Name',ascending=False)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
spines = ['top','bottom','left','right']
for x in spines:
    if x in spines:
        ax.spines[x].set_visible(False)
sns.swarmplot(x='xG',data=data,color='white',zorder=1)

#plot 
plt.scatter(x=0.6,y=0,c='red',edgecolor='white',s=150,zorder=2)
plt.text(s='Name',x=0.6,y=-.04,c=text_color)

plt.title('xG Super League 2020/21',c=text_color,fontsize=14)
plt.xlabel('xG per 90',c=text_color)

### Important ###
print(data.head())
data.Name.unique()
data = data.reset_index()

####
####
#### Occasions de buts #######
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
#### Spécifique Defenseur  #######
####
####

metrics = ['PAdj Clearances','Aerial Win%','Average DA X','Tack&Int','Dribbles Stopped%','Dribbled Past']

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
