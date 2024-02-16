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


data = pd.read_excel('fw_kmeans_absvalues.xlsx')
data = data[ (data.k_means == 2)]

#data = pd.read_xlsx('airton.xlsx')

#set default colors
text_color = 'black'
background = 'white'



### Important ###
print(data.head())
data.Player.unique()
data = data.reset_index()

####
####
#### Occasions de buts #######
####
####

metrics = ["xG", "Shots", "Dispossessed", "Turnovers", "Deep Progressions", "Carries",
"Dribbles", "Successful Dribbles", "Touches In Box", "Successful Crosses",
"PintoB", "Key Passes", "xG Assisted", "Assists", "Aerial Wins",
"Passes Inside Box"]

fig,axes = plt.subplots(8,2,figsize=(25,25))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

for i,ax in zip(data['Player'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
    sns.swarmplot(x=metrics[met_counter],data=data,ax=axes[counter,counter2],zorder=1,color='#64645e')
    ax.set_xlabel(f'{metrics[met_counter]}',c='black')
    
    for x in range(len(data['Player'])):
        if data['Player'][x] == 'Felix Mambimbi':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='seagreen',zorder=2)
        if data['Player'][x] == 'Alexis Antunes':
           ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='orange',zorder=2)  
        if data['Player'][x] == 'Edon Zhegrova':
            ax.scatter(x=data[metrics[met_counter]][x],y=0,s=100,c='lightgrey',zorder=2)                          
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1
#ax.text(s='Timothé Cognat',x=0.6,y=-.04,c=text_color)            
# s='<Risky & Selfish'
# highlight_text.fig_text(s=s, x=.25, y=.88, #highlight_weights = ['bold'],
#                 fontsize=22,
#                 fontfamily = 'Andale Mono',
#                 color = text_color,
#                 #highlight_colors = ['#6CABDD'],
#                 va='center'
#                ) 
#fig.text(.12,.05,"Statistique moyenne par match/90 minutes joués",fontsize=11, fontfamily='Andale Mono',color=text_color)
#plt.savefig('attaquant_occasions de buts.png',dpi=500,bbox_inches = 'tight',facecolor=background)

