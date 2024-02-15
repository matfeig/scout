#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 16:47:51 2022

@author: matfeig
"""
from pywaffle import Waffle # PyWaffle Documentation --> https://buildmedia.readthedocs.org/media/pdf/pywaffle/latest/pywaffle.pdf
import matplotlib.pyplot as plt #Matplotlib pyplot to plot the charts
import pandas as pd
import matplotlib as mpl
from highlight_text import htext #used for highlighting the title

### Open csv player stats statsbomb ##
df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/player_analysis/passes.csv")
df.head()


### Soterd values #
df = df.sort_values(by=['Pass Forward%'], ascending = False)


### Switching column and rows  transpose ####
data = df.T
data.columns = data.iloc[0]
data = data.drop ('Name')
data.head()


my_list = data.columns.values.tolist()
data3 = pd.DataFrame(data,columns=my_list)


#### Plot one player ###
fig = plt.figure(
    FigureClass= Waffle,
    values = data3.iloc[:,0],
    labels = list(data3.index),
    rows = 10,
    #columns = 10 forcer 100 value
    title = {
        'label' : my_list[0]
    },
)

#Create the waffle chart. We use pyplot.figure() witht the figure class = Waffle
#Refer to the documentation to get exact explanation on everything.
fig = plt.figure(
    FigureClass = Waffle,
    rows= 10,
    figsize = (10,10),
    plots={
        '331': {                              #refer matplotlib subplot grids, '331' means 3 x 3 grid, first subplot
            'values': data3.iloc[:,0],
            'title': {
                'label': my_list[0],
                'color': 'White'
            },
        },
        '332': {                             
            'values': data3.iloc[:,1],
            'title': {
                'label': my_list[1],
                'color': 'white'
            },
        },
        '333': {                           #Line 20   
            'values': data3.iloc[:,2],
            'title': {
                'label': my_list[28],
                'color': 'white'
            }
        },
        '334':{                              
            'values': data3.iloc[:,3],
            'title': {
                'label': my_list[3],
                'color': 'white'
            },
        },
        '335': {                              
            'values': data3.iloc[:,4],
            'title': {
                'label': my_list[4],
                'color': 'white'
            },
        },
        '336': {
            'values': data3.iloc[:,5],                              
            'title': {
                'label': my_list[5],
                'color': 'white'
            },
        },
        '337': {                              
            'values': data3.iloc[:,6],
            'title': {
                'label': my_list[6],
                'color': 'white'
            },
        },
        '338': {                             
            'values': data3.iloc[:,7],
            'title': {
                'label': my_list[7],
                'color': 'white'
                ''
            },
        },
        '339': {
            'values': data3.iloc[:,8],
            'title': {
                'label': my_list[8],
                'color': 'white'
            },
            },
    },
    rounding_rule='floor',
    colors=("#a3a3c2", "#75a3a3", "#ff4d4d"),
    facecolor=background
)

#Different colors so we don't have to type them in every time
background = "#313332"
text_color = 'w'
primary = 'red'
secondary = 'lightblue'
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color


#Create the text and highlight the different points
s = "Top Passers in La Liga + How They Made Their Passes \n<LEFT>, <RIGHT>, <HEAD>, + <OTHER>"
htext.fig_htext(s,
                x=.02,y=.9,
                fontfamily='Andale Mono',
                highlight_weights=['bold'],
                string_weight='bold',
                fontsize=18,
                color=text_color,
                highlight_colors=['#a3a3c2','#75a3a3','#ff4d4d','#00cc99'])
fig.patch.set_facecolor(background)
fig.text(.01,0.05,"each block represents roughly 50 passes\n@mckayjohns / data via fbref & statsbomb",fontstyle='italic',fontsize=9,fontfamily='Andale Mono',color=text_color)


#plt.savefig('waffle.png',dpi=300,bbox_inches = 'tight',facecolor=background)



