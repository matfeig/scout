# -*- coding: utf-8 -*-
"""
Created on Sun May 31 13:33:38 2020

@author: feig
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, Ellipse
from matplotlib.lines import Line2D
import matplotlib.transforms as transforms
import seaborn as sns; sns.set(style="white")
#from matplotlib.collections import LineCollection


############ Importation des données ############
data = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/Dataevent/stg_zur.csv")

############ SuppresLausanne des NaN ############
data = data.dropna()

############ SuppresLausanne des doublons ############
data = data.drop_duplicates(subset=['start', 'end', 'code', 'Team', 'Action', 'Half', 'pos_x', 'pos_y'], keep='first')


#concatener 3 derniers matchs 

#from mplsoccer.pitch import Pitch
#pitch = Pitch(pitch_color='lightgrey', line_color='white', stripe=False, axis=False, label=False, tick=False)
#fig, ax = pitch.draw()

############################################################################
############################# Tracé du terrain #############################
############################################################################

def draw_pitch(pitch, line, orientation,view, ax=None):
    """
    Paramètres :

    pitch : 
        couleur du fond du terrain
    line : 
        couleur des lignes
    orientation : 
        "h" pour horizontal
        "v" pour vertical
    view : 
        "full" pour terrain entier
        "def" pour moitié inférieure du terrain
        "off" pour moitié supérieure du terrain
    """
    
    orientation = orientation
    view = view
    line = line
    pitch = pitch
    ax=ax
    
    if orientation.lower().startswith("h"):    
        if view.lower().startswith("off"):
            if ax is None :
                fig,ax = plt.subplots(figsize=(8,10.4))
            plt.xlim(50,106)
            plt.ylim(-5,70)
        elif view.lower().startswith("def"):
            if ax is None :
                fig,ax = plt.subplots(figsize=(8,10.4))
            plt.xlim(-1,53)
            plt.ylim(-5,70)
        else:
            if ax is None:
                fig,ax = plt.subplots(figsize=(15,9.5))
            #plt.xlim(-1,106)
            #plt.ylim(-10,70)
        ax.axis('off') # this hides the x and y ticks
    
        # side and goal lines #
        #ly1 = [0,0,68,68,0]
        #lx1 = [0,105,105,0,0]
        rec1 = Rectangle((0,0), 105, 68, linewidth=2, edgecolor=line, facecolor=pitch, zorder=0)
        ax.add_patch(rec1)

        rec1b = Rectangle((0,0), 105, 68, linewidth=2, edgecolor=line, fill=False, zorder=20)
        ax.add_patch(rec1b)

        # boxes, 6 yard box and goals

            #outer boxes#
        #ly2 = [13.84,13.84,54.16,54.16] 
        #lx2 = [105,88.5,88.5,105]
        rec2 = Rectangle((105,13.84), -16.5, 40.32, linewidth=2, color=line, fill=False)
        ax.add_patch(rec2)        

        #ly3 = [13.84,13.84,54.16,54.16] 
        #lx3 = [0,16.5,16.5,0]
        rec3 = Rectangle((0,13.84), 16.5, 40.32, linewidth=2, color=line, fill=False)
        ax.add_patch(rec3)

            #goals#
        rec4 = Rectangle((105,30.84), 0.2, 7.32, linewidth=2, color=line, fill=False)
        ax.add_patch(rec4)

        rec5 = Rectangle((0,30.84), -0.2, 7.32, linewidth=2, color=line, fill=False)
        ax.add_patch(rec5)

           #6 yard boxes#
        rec6 = Rectangle((105,24.84), -5.5, 18.32, linewidth=2, color=line, fill=False)
        ax.add_patch(rec6)

        rec7 = Rectangle((0,24.84), 5.5, 18.32, linewidth=2, color=line, fill=False)
        ax.add_patch(rec7)

        #Halfway line, penalty spots, and kickoff spot

        rec8 = Rectangle((52.5,0), 0, 68, linewidth=2, color=line, fill=False)
        ax.add_patch(rec8)

        ## Circles and arcs
        centerCircle = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False,alpha=1)
        leftArc = Arc((10,34),height=20,width=20,angle=0,theta1=310,theta2=50,color=line, linewidth=1.5)
        rightArc = Arc((95,34),height=20,width=20,angle=0,theta1=130,theta2=230,color=line, linewidth=1.5)
        
        ## Pitch rectangle
        #rec3 = plt.Rectangle((-1, -3), 107,75,ls='-',color=pitch, alpha=1)

        #ax.add_patch(rec3)
        ax.add_patch(centerCircle)
        ax.add_patch(leftArc)
        ax.add_patch(rightArc)
        
        ## Points
        centreSpot = plt.Circle((52.5,34), 0.71, color=line)
        leftPenSpot = plt.Circle((9.5,34), 0.5, color=line)
        rightPenSpot = plt.Circle((94.5,34), 0.5, color=line)
        
        ax.add_patch(centreSpot)
        ax.add_patch(leftPenSpot)
        ax.add_patch(rightPenSpot)
        
        return ax
    else :
        if view.lower().startswith("off"):
            fig,ax = plt.subplots(figsize=(10.4,8))
            plt.xlim(-5,70)
            plt.ylim(50,105)
        elif view.lower().startswith("def"):
            fig,ax = plt.subplots(figsize=(10.4,8))
            plt.xlim(-5,70)
            plt.ylim(-2.5,52.5)
        else:
            if ax is None:
                fig,ax = plt.subplots(figsize=(8.5,13))
            #plt.xlim(-10,70)
            #plt.ylim(-1,106)
        ax.axis('off') # this hides the x and y ticks
    
        # side and goal lines #
        #ly1 = [0,0,68,68,0]
        #lx1 = [0,105,105,0,0]
        rec1 = Rectangle((0,0), 68, 105, linewidth=2, edgecolor=line, facecolor=pitch, zorder=0)
        ax.add_patch(rec1)
        rec1b = Rectangle((0,0), 68, 105, linewidth=2, edgecolor=line, fill=False, zorder=20)
        ax.add_patch(rec1b)

        # boxes, 6 yard box and goals

            #outer boxes#
        #ly2 = [13.84,13.84,54.16,54.16] 
        #lx2 = [105,88.5,88.5,105]
        rec2 = Rectangle((13.84,105), 40.32, -16.5, linewidth=2, color=line, fill=False)
        ax.add_patch(rec2)        

        #ly3 = [13.84,13.84,54.16,54.16] 
        #lx3 = [0,16.5,16.5,0]
        rec3 = Rectangle((13.84,0), 40.32, 16.5, linewidth=2, color=line, fill=False)
        ax.add_patch(rec3)

            #goals#
        rec4 = Rectangle((30.84,105), 7.32, 0.2, linewidth=2, color=line, fill=False)
        ax.add_patch(rec4)

        rec5 = Rectangle((30.84,0), 7.32, -0.2, linewidth=2, color=line, fill=False)
        ax.add_patch(rec5)

           #6 yard boxes#
        rec6 = Rectangle((24.84,105), 18.32, -5.5, linewidth=2, color=line, fill=False)
        ax.add_patch(rec6)

        rec7 = Rectangle((24.84,0), 18.32, 5.5, linewidth=2, color=line, fill=False)
        ax.add_patch(rec7)

        #Halfway line, penalty spots, and kickoff spot########################################

        rec8 = Rectangle((0,52.5), 68, 0, linewidth=2, color=line, fill=False)
        ax.add_patch(rec8)

        ## Circles and arcs
        centerCircle = plt.Circle((34, 52.5), 9.15,ls='solid',lw=1.5,color=line, fill=False,alpha=1)
        leftArc = Arc((34,10),height=20,width=20,angle=0,theta1=400,theta2=140,color=line, linewidth=1.5)
        rightArc = Arc((34,95),height=20,width=20,angle=0,theta1=220,theta2=320,color=line, linewidth=1.5)

        ax.add_patch(centerCircle)
        ax.add_patch(leftArc)
        ax.add_patch(rightArc)

        ## Points
        centreSpot = plt.Circle((34,52.5), 0.71, color=line)
        leftPenSpot = plt.Circle((34,9.5), 0.5, color=line)
        rightPenSpot = plt.Circle((34,94.5), 0.5, color=line)
        
        ax.add_patch(centreSpot)
        ax.add_patch(leftPenSpot)
        ax.add_patch(rightPenSpot)
        
        return ax

draw_pitch("white", "black", "h", "full")

#####################################################################################
########## Fonction pour tracer les localisations pour une action choisie ###########
#####################################################################################

def drawAction(typeAction, team, pitch, line, orientation,view, diff='action', deb=0, fin=max(data.start)):
    """
    Paramètres :

    typeAction :
        action à plotter
    mark :
        symbole pour représenter l'action'
    pitch : 
        couleur du fond du terrain
    line : 
        couleur des lignes
    orientation : 
        "h" pour horizontal
        "v" pour vertical
    view : 
        "full" pour terrain entier
        "half" pour moitié de terrain
    diff :
        "action" pour différentier les points suivant le type d'action
        "player" pour différentier les points selon le joueur
    """
    if type(typeAction) == str:
        typeAction = [typeAction]
    col_list = ['red', 'navy', 'limegreen', 'orange', 'fuchsia', 'turquoise', 'dimgray', 'darkmagenta', 'forestgreen', 'yellow', 'saddlebrown']
    action = data[(data.Action.isin(typeAction)) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )]
    if diff == 'action':
        groups = action.groupby("Action")
    elif diff == 'joueur' or diff == 'player':
        groups = action.groupby("code")
    draw_pitch(pitch, line, orientation,view)
    i=0
    plt.suptitle(team, fontsize = 20, color='firebrick', family = 'monospace', fontweight = 'bold' )

    if orientation.lower().startswith("h"):
        for name, group in groups:
            plt.plot(group["pos_x"], group["pos_y"], marker="o", linestyle="", label=name, markersize=10, color=col_list[i])
            i+=1 
        if view.lower().startswith("off"):
            plt.arrow(71.5, -1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(77.5, -5, "Sens du jeu", ha="center", va="center", size=20)
            s=len(typeAction)//5
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05+0.05*s),fontsize='x-large', frameon = False, ncol=min(len(typeAction),4))
        elif view.lower().startswith("def"):
            plt.arrow(21.5, -1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(27.5, -5, "Sens du jeu", ha="center", va="center", size=20)
            s=len(typeAction)//5
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05+0.05*s),fontsize='x-large', frameon = False, ncol=min(len(typeAction),4))
        else :
            plt.arrow(46.5, -1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(52.5, -5, "Sens du jeu", ha="center", va="center", size=20)
            s=len(typeAction)//5
            if diff == 'action':
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05+0.05*s),fontsize='x-large', frameon = False, ncol=min(len(typeAction),5))
            elif diff == 'joueur' or diff == 'player':
                plt.legend(loc='center left', bbox_to_anchor=(0.95, 0.5),fontsize='x-large', frameon = False, ncol=1)
        plt.show()
        
    else : #si vertical, il faut intervertir les x et y et miroiter y
        for name, group in groups:
            plt.plot(68-group["pos_y"], group["pos_x"], marker="o", linestyle="", label=name, markersize=10, color=col_list[i])
            i+=1
        if view.lower().startswith("off"):
            plt.arrow(-1.5, 71.5, 0, 10, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(-5, 77.5, "Sens du jeu", ha="center", va="center", size=20, rotation=90)
            s=len(typeAction)//5
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.07+0.05*s),fontsize='x-large', frameon = False, ncol=min(len(typeAction),4))
        elif view.lower().startswith("def"):
            plt.arrow(-1.5, 21.5, 0, 10, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(-5, 27.5, "Sens du jeu", ha="center", va="center", size=20, rotation=90)
            s=len(typeAction)//5
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.07+0.05*s),fontsize='x-large', frameon = False, ncol=min(len(typeAction),4))
        else :
            plt.arrow(-1.5, 46.5, 0, 10, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(-5, 52.5, "Sens du jeu", ha="center", va="center", size=20, rotation=90)
            s=len(typeAction)//5
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05+0.05*s),fontsize='x-large', frameon = False, ncol=min(len(typeAction),5))
        plt.show()
drawAction(['Shots'],'Molde', "papayawhip", "black", "h", "full", diff='joueur')
drawAction(['Passes into the penalty box'],'Lausanne', "papayawhip", "black", "h", "full", diff='joueur')
drawAction(['Key passes (accurate)'],'Lausanne', "papayawhip", "black", "h", "full", diff='joueur')
drawAction(['Passes into the penalty box', 'Goals'],'Lausanne', "papayawhip", "black", "h", "full", diff='action')
drawAction(['Shots'],'Lausanne', "papayawhip", "black", "h", "full", diff='joueur')
drawAction(['Interceptions', 'Picking-ups'],'Lausanne', "papayawhip", "black", "h", "full", diff='action')
drawAction(['Interceptions', 'Picking-ups'],'Lausanne', "papayawhip", "black", "h", "full", diff='joueur')


########################################################################################
################################### Passe décisive #####################################
########################################################################################

def drawAssists(team, pitch, line, orientation,view, deb=0, fin=max(data.start)):
    goals = data[(data.Action == 'Goals') & (data.Team == team) & (data.start >= deb*60) & (data.start <= fin*60 )]
    draw_pitch(pitch, line, orientation,view)
    col_list = ['darkgreen', 'turquoise', 'blue', 'mediumvioletred', 'orange','red']
    col_dict = {}
    assistants = data[(data.Team == team) & (data.Action == 'Assists')]
    for i in assistants.code.unique():
        col_dict[i] = col_list.pop()
    for i in range(len(goals)):
        sec = goals.iloc[i].start
        assist = data[(data.Team == team) & (data.Action == 'Assists') & (data.start > sec - 10) & (data.start <= sec)]

        if orientation.lower().startswith("h"):
            print(assist.code.iloc[0])
            plt.scatter(assist.pos_x, assist.pos_y, marker = 'x', color = col_dict[assist.code.iloc[0]], s=100, zorder=3)
            plt.scatter(goals.iloc[i].pos_x, goals.iloc[i].pos_y, marker = 'o', color = 'darkred', s=100, zorder=3)
            plt.plot([assist.pos_x, goals.iloc[i].pos_x], [assist.pos_y, goals.iloc[i].pos_y], color = col_dict[assist.code.iloc[0]])
        elif orientation.lower().startswith("v"):
            plt.scatter(68-assist.pos_y, assist.pos_x, marker = 'x', color = col_dict[assist.code.iloc[0]], s=100, zorder=3)
            plt.scatter(68-goals.iloc[i].pos_y, goals.iloc[i].pos_x, marker = 'o', color = 'darkred', s=100, zorder=3)
            plt.plot([68-assist.pos_y, 68-goals.iloc[i].pos_y], [assist.pos_x, goals.iloc[i].pos_x], color = col_dict[assist.code.iloc[0]])
    plt.title(team,fontsize = 18, color='darkred', family = 'monospace', fontweight = 'bold' )
    if orientation.lower().startswith("h"):
        if view.lower().startswith("full"):
            legend_elements = [Line2D([0], [0], marker='X', color='w', label='Assist',markerfacecolor='black', markersize=15),
                               Line2D([0], [0], marker='o', color='w', label='Goal',markerfacecolor='darkred', markersize=15)]
            for i in assistants.code.unique():
                legend_elements.append(Line2D([0], [0], marker='X', color='w', label=i.split()[-1],markerfacecolor=col_dict[i], markersize=15))
            plt.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.6,-0.07),fontsize='xx-large', ncol=2, frameon = False)
            plt.text(20, -5, "Sens du jeu", ha="center", va="center", size=20)
            plt.arrow(14, -1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)

        elif view.lower().startswith("off"):
            legend_elements = [Line2D([0], [0], marker='X', color='w', label='Assist',markerfacecolor='black', markersize=15),
                               Line2D([0], [0], marker='o', color='w', label='Goal',markerfacecolor='darkred', markersize=15)]
            for i in assistants.code.unique():
                legend_elements.append(Line2D([0], [0], marker='X', color='w', label=i.split()[-1],markerfacecolor=col_dict[i], markersize=15))
            plt.legend(handles=legend_elements, loc=(0.4,-0.1),fontsize='xx-large', ncol=2, frameon = False)
            plt.text(64, -4, "Sens du jeu", ha="center", va="center", size=20)
            plt.arrow(58, -1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)
    if orientation.lower().startswith("v"):
        if view.lower().startswith("full"):
            legend_elements = [Line2D([0], [0], marker='X', color='w', label='Assist',markerfacecolor='black', markersize=15),
                               Line2D([0], [0], marker='o', color='w', label='Goal',markerfacecolor='darkred', markersize=15)]
            for i in assistants.code.unique():
                legend_elements.append(Line2D([0], [0], marker='X', color='w', label=i.split()[-1],markerfacecolor=col_dict[i], markersize=15))
            plt.legend(handles=legend_elements, loc=(-0.4,0.7),fontsize='xx-large', frameon = False)
            plt.arrow(-1.5, 46.5, 0, 10, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(-5, 53.2, "Sens du jeu", ha="center", va="center", size=20, rotation=90)

        elif view.lower().startswith("off"):
            legend_elements = [Line2D([0], [0], marker='X', color='w', label='Assist',markerfacecolor='black', markersize=15),
                               Line2D([0], [0], marker='o', color='w', label='Goal',markerfacecolor='darkred', markersize=15)]
            for i in assistants.code.unique():
                legend_elements.append(Line2D([0], [0], marker='X', color='w', label=i.split()[-1],markerfacecolor=col_dict[i], markersize=15))
            plt.legend(handles=legend_elements, loc=(-0.3,0.6),fontsize='xx-large', frameon = False)
            plt.arrow(-1.5, 54, 0, 10, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(-5, 60, "Sens du jeu", ha="center", va="center", size=20, rotation=90)
    
    plt.show()

drawAssists("Molde", "papayawhip", "black", "h", "full")
drawAssists("Lausanne", "papayawhip", "black", "h", "full")


#######################################################################################
##################################### Heatmap #########################################
#######################################################################################
  
#####
##### Heatmap de zones
#####
    
#import matplotlib.colors as colors
from collections import OrderedDict
cmaps = OrderedDict()


def heat_zones(typeAction, team, orientation, view, deb=0, fin=max(data.start)):
    z11 = len(data[(data.pos_x >= 87.5) & (data.pos_y >= 54.16) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z12 = len(data[(data.pos_x >= 87.5) & (data.pos_y < 54.16) & (data.pos_y >= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z13 = len(data[(data.pos_x >= 87.5) & (data.pos_y < 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z21 = len(data[(data.pos_x < 87.5) & (data.pos_x >= 70) & (data.pos_y >= 54.16) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z22 = len(data[(data.pos_x < 87.5) & (data.pos_x >= 70) & (data.pos_y < 54.16) & (data.pos_y >= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z23 = len(data[(data.pos_x < 87.5) & (data.pos_x >= 70) & (data.pos_y <= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )]) 
    z31 = len(data[(data.pos_x < 70) & (data.pos_x >= 52.5) & (data.pos_y >= 54.16) & (data.Action == typeAction) & (data.Team == team)  & (data.start >= deb*60) & (data.start <= fin*60 )])
    z32 = len(data[(data.pos_x < 70) & (data.pos_x >= 52.5) & (data.pos_y < 54.16) & (data.pos_y >= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z33 = len(data[(data.pos_x < 70) & (data.pos_x >= 52.5) & (data.pos_y <= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z41 = len(data[(data.pos_x < 52.5) & (data.pos_x >= 35) & (data.pos_y >= 54.16) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z42 = len(data[(data.pos_x < 52.5) & (data.pos_x >= 35) & (data.pos_y < 54.16) & (data.pos_y >= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z43 = len(data[(data.pos_x < 52.5) & (data.pos_x >= 35) & (data.pos_y <= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z51 = len(data[(data.pos_x < 35) & (data.pos_x >= 17.5) & (data.pos_y >= 54.16) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z52 = len(data[(data.pos_x < 35) & (data.pos_x >= 17.5) & (data.pos_y < 54.16) & (data.pos_y >= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z53 = len(data[(data.pos_x < 35) & (data.pos_x >= 17.5) & (data.pos_y <= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z61 = len(data[(data.pos_x < 17.5) & (data.pos_y >= 54.16) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z62 = len(data[(data.pos_x < 17.5) & (data.pos_y < 54.16) & (data.pos_y >= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    z63 = len(data[(data.pos_x < 17.5) & (data.pos_y <= 13.84) & (data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )])
    
    zones = np.array([[z11, z12, z13],
             [z21, z22, z23],
             [z31, z32, z33],
             [z41, z42, z43],
             [z51, z52, z53],
             [z61, z62, z63]]) 
    
    if orientation.lower().startswith("v"):
        if view.lower().startswith("full"):
            sns.heatmap(zones, annot=True, linewidths=1)  
        elif view.lower().startswith("def"):
            sns.heatmap(zones[3:6], annot=True, linewidths=1)
        elif view.lower().startswith("off"):
            sns.heatmap(zones[0:3], annot=True, linewidths=1)

    elif orientation.lower().startswith("h"):
        zones = np.flip(zones.T,1)
        if view.lower().startswith("full"):
            sns.heatmap(zones, annot=True, linewidths=1, cmap='YlOrRd')
            
            #ax = draw_pitch("white", "black", "h", "full")
            #ax.imshow(zones, aspect="auto", extent=(0,105,0,34), cmap='Reds')
            plt.show()


        elif view.lower().startswith("def"):
            sns.heatmap(zones[:,0:3], annot=True, linewidths=1)
        elif view.lower().startswith("off"):
            sns.heatmap(zones[:,3:6], annot=True, linewidths=1)
  
    plt.show()


heat_zones("Interceptions", "Molde", "h", "full")


#####
##### Heatmap "chaleur"
#####

def heat_map(typeAction, team, orientation, view, levels, deb=0, fin=max(data.start)//60):
    if type(typeAction) == str:
        typeAction = [typeAction]
    elif type(typeAction) != list :
        return ("Erreur d'entrée : typeAction doit être une chaîne de caractère ou une liste")

    action = data[(data.Action.isin(typeAction)) & (data.Team == team) & (data.start >= deb*60) & (data.start <= fin*60 )]
    mark = ['X','o', '^', 's', '$O$', '*']
    color_list = ['yellow','fuchsia', 'gray', 'navy', 'deepskyblue']
    legend_elements = []      
    if orientation.lower().startswith("h"):
        draw_pitch("papayawhip", "black", orientation,view)
        ax = sns.kdeplot(action.pos_x, action.pos_y, shade = "True", cmap = "YlOrRd", n_levels = levels, zorder=1)
        ax.collections[0].set_alpha(0)
        if view.lower().startswith("full"):
            plt.ylim(0, 68) # need this, otherwise kde plot will go outside
            plt.xlim(0, 105)
        elif view.lower().startswith("def"):
            plt.ylim(0, 68)
            plt.xlim(0, 53)
        elif view.lower().startswith("off"):
            plt.ylim(0, 68)
            plt.xlim(52, 105)

        plt.title(team,fontsize = 18, color='darkred', family = 'monospace', fontweight = 'bold' )
        plt.suptitle("Heatmap" + '(de ' + str(deb) + ' à ' +str(fin) +' min)' , fontsize = 20, family = 'monospace')
        for i in range(len(typeAction)) :
            act = data[(data.Action == typeAction[i]) & (data.Team == team) & (data.start >= deb*60) & (data.start <= fin*60 )]
            plt.scatter(act.pos_x, act.pos_y, color=color_list[i], marker=mark[i], s=150, zorder=3)
            legend_elements.append(Line2D([0], [0], marker=mark[i], color='w', label=typeAction[i], markerfacecolor=color_list[i], markersize=15))
        if view.lower().startswith("full"):
            plt.arrow(46.5, 1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(52.5, -2, "Sens du jeu", ha="center", va="center", size=20)
        elif view.lower().startswith("def"):
            plt.arrow(35, 1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)
            plt.text(41, -2, "Sens du jeu", ha="center", va="center", size=20)
        elif view.lower().startswith("off"):
            plt.text(64, -2, "Sens du jeu", ha="center", va="center", size=20)
            plt.arrow(58, 1.5, 10, 0, color='lightcoral', width=1, head_width=2, snap=True)

        plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.06),fontsize='x-large', frameon = False, ncol=2)

    else : #si vertical, il faut intervertir les x et y et miroiter y
        draw_pitch("papayawhip", "black", orientation,view)

        sns.kdeplot(68-action.pos_y, action.pos_x, shade = "True", cmap = "YlOrRd", n_levels = levels, zorder=1)
        plt.ylim(0, 105) # need this, otherwise kde plot will go outside
        plt.xlim(0, 68)

        #plt.title(team,fontsize = 18, color='darkred', family = 'monospace', fontweight = 'bold' )
        #plt.suptitle("Heatmap" + '(de ' + str(deb) + ' à ' +str(fin) +' min)' , fontsize = 20, family = 'monospace')

        for i in range(len(typeAction)) :
            act = data[(data.Action == typeAction[i]) & (data.Team == team) & (data.start >= deb*60) & (data.start <= fin*60 )]
            plt.scatter(68-act.pos_y, act.pos_x, color=color_list[i], marker=mark[i], s=150)
            legend_elements.append(Line2D([0], [0], marker=mark[i], color='w', label=typeAction[i], markerfacecolor=color_list[i], markersize=15))
        plt.arrow(1.5, 6, 0, 10, color='lightcoral', width=1, head_width=2, snap=True)
        plt.text(-2, 12.7, "Sens du jeu", ha="center", va="center", size=20, rotation=90)
        plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5),fontsize='xx-large', frameon = False, ncol=1)


heat_map('Shots', "Molde", "h", "full", 50)
heat_map('Key passes (accurate)', "Molde", "h", "full", 50)
heat_map('Passes into the penalty box', "Lausanne", "h", "full", 50)
heat_map(['Shot into the bar/post', 'Assists', 'Goals','Dribbles (Successful actions)', 'Key passes (accurate)'], "Lausanne", "h", "full", 50)
heat_map(['Interceptions', 'Challenges (won)', 'Picking-ups', 'Fouls'], "St. Gallen", "h", "full",50)
heat_map(['Interceptions', 'Picking-ups'], "Molde", "h", "full",50)



heat_map('Passes accurate', "Lille", "h", "full", 50, fin=150)
#heat_map('Passes accurate', "Lausanne", "v", "full", 50, fin=45)
#heat_map('Passes accurate', "Lausanne", "v", "full", 50, deb=45)

#########################################################################################
##################################### Jointplot #########################################
#########################################################################################

def draw_jointplot(typeAction, team, plotType, pitch, line, orientation,view, deb=0, fin=max(data.start)):
    """
    Paramètres :

    typeAction :
        action à plotter
    team :
        équipe à considérer
    plotType:
        "scatter" pour des points
        "hex" pour les alvéoles
        "kde" pour la distribution
    pitch : 
        couleur du fond du terrain
    line : 
        couleur des lignes
    orientation : 
        "h" pour horizontal
        "v" pour vertical
    view : 
        "full" pour terrain entier
    """

    assert plotType in ["scatter","hex","kde"], str('Erreur de saisie : le type de jointplot n\'est pas bon ("')+ plotType + str('").\nJointplot acceptés : "scatter", "hex", ou "kde"')
    if orientation.lower().startswith("h"):
        action = data[(data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )]

        if plotType == "scatter" :
            joint_shot_chart = sns.jointplot(action.pos_x, action.pos_y, stat_func=None, kind=plotType, marginal_kws=dict(bins=10), space=0, s=200, color='deepskyblue', edgecolor='navy', linewidth=2)  
            joint_shot_chart.fig.set_size_inches(15,9.5)
            ax = joint_shot_chart.ax_joint
        elif plotType == "hex":
            joint_shot_chart = sns.jointplot(action.pos_x, action.pos_y, stat_func=None, kind=plotType, marginal_kws=dict(bins=10), joint_kws=dict(gridsize=8), space=0, edgecolor = 'cyan', linewidth=2)
            joint_shot_chart.fig.set_size_inches(15,9.5)
            ax = joint_shot_chart.ax_joint
        else :
            joint_shot_chart = sns.jointplot(action.pos_x, action.pos_y, stat_func=None, kind=plotType, space=0, n_levels=50, cmap = "YlOrRd", color="red")
            joint_shot_chart.fig.set_size_inches(15,9.5)
            ax = joint_shot_chart.ax_joint
            ax.collections[0].set_alpha(0)

        draw_pitch(pitch, line, orientation,view, ax=ax)
        ax.set_xlim(0,105)
        ax.set_ylim(0,68)
        plt.suptitle(team + " - " + typeAction,fontsize = 20, family = 'monospace', fontweight = 'bold')


    else : #si vertical, il faut intervertir les x et y et miroiter y
        action = data[(data.Action == typeAction) & (data.Team == team ) & (data.start >= deb*60) & (data.start <= fin*60 )]

        if plotType == "scatter" :
            joint_shot_chart = sns.jointplot(68-action.pos_y, action.pos_x, stat_func=None, kind=plotType, marginal_kws=dict(bins=10), space=0, s=200, color='deepskyblue', edgecolor='navy', linewidth=2)  
            joint_shot_chart.fig.set_size_inches(9.5,15)
            ax = joint_shot_chart.ax_joint
        elif plotType == "hex":
            joint_shot_chart = sns.jointplot(68-action.pos_y, action.pos_x, stat_func=None, kind=plotType, marginal_kws=dict(bins=10), joint_kws=dict(gridsize=8), space=0, edgecolor = 'cyan', linewidth=2)
            joint_shot_chart.fig.set_size_inches(9.5,15)
            ax = joint_shot_chart.ax_joint
        else :
            joint_shot_chart = sns.jointplot(68-action.pos_y, action.pos_x, stat_func=None, kind=plotType, space=0, n_levels=50, cmap = "YlOrRd", color="red")
            joint_shot_chart.fig.set_size_inches(9.5,15)
            ax = joint_shot_chart.ax_joint
            ax.collections[0].set_alpha(0)

        draw_pitch(pitch, line, orientation,view, ax=ax)
        ax.set_xlim(0,68)
        ax.set_ylim(0,105)
        plt.suptitle(team + " - " + typeAction,fontsize = 20, family = 'monospace', fontweight = 'bold')

draw_jointplot("Interceptions", "Molde", "kde", "papayawhip", "black", "h", "full")
draw_jointplot("Interceptions", "Molde", "scatter", "papayawhip", "black", "h", "full")

draw_jointplot("Lost balls", "Lausanne", "kde", "papayawhip", "black", "h", "full")
draw_jointplot("Lost balls", "Lausanne", "scatter", "papayawhip", "black", "h", "full")

draw_jointplot("Passes accurate", "Lausanne", "kde", "papayawhip", "black", "h", "full")


draw_jointplot("Passes accurate", "Lausanne", "scatter", "papayawhip", "black", "h", "full")
draw_jointplot("Passes accurate", "Lausanne", "kde", "papayawhip", "black", "h", "full")
draw_jointplot("Passes accurate", "Lausanne", "hex", "papayawhip", "black", "h", "full")


#########################################################################################
############################ Création Animation #########################################
#########################################################################################

#import imageio
#import os
#from os import listdir
#from os.path import isfile, join
#
#### Plot des figures et sauvegardes en tant qu'images dans  ###
#### le dossier dans lequel on travaille                     ###
#for i in range(5,100):
#    heat_map(['Passes into the penalty box', 'Assists', 'Goals','Dribbles (Successful actions)'], "Servette Football Club Geneve", "h", "full", 50, 0, i)
#
#    plt.savefig('HEATMAP_{}.png'.format(i))
#
#files = os.listdir(".")
#
#### On trie les fichiers pour que HEATMAP5 apparaisse avant     ###
#### HEATMAP12 (ce qui n'est pas l'ordre alphabétique)           ###
#files = [ ( int (_.replace("HEATMAP","").replace(".png","")), _) for _ in files ]
#files.sort()
#files = [ _[1] for _ in files ]
#
#files = [ ( "HEATMAP_%03d.png" % i, _) for i,_ in enumerate(files) ]
#for new_name, old_name in files :
#    if new_name != old_name :
#        os.rename(old_name, new_name)
#
#### On récupère les fichers ###
#images = []
#fichiers = [f for f in listdir('D:/Documents/Stats/SFC/heatmaps') if isfile(join('D:/Documents/Stats/SFC/heatmaps', f))]
#
#
####### On créé la vidéo mp4 (remplacer par .gif si on veut un GIF) ######
#for filename in fichiers:
#    images.append(imageio.imread(filename))
#imageio.mimsave('D:\Documents\Stats\SFC\heatmaps\TEST.mp4', images, fps=1)
#
#
####### autre manière de créer une vidéo mp4 ######
##with imageio.get_writer('D:/Documents/Stats/SFC/vid/video.mp4', mode='I', fps = 1) as writer:
##    for filename in fichiers:
##        image = imageio.imread(filename)
##        writer.append_data(image)


#########################################################################################
############################ Dégagement gardien #########################################
#########################################################################################

def plotPasse(x1,y1,x2,y2, col):
    x = np.linspace(x1,x2,1000)
    y = np.linspace(y1,y2,1000)
    lwidths = (0.004*x)**3 # scatter 'o' marker size is specified by area not radius 
    plt.scatter(x,y, s=lwidths, color=col)
    plt.xlim(0,105)
    plt.ylim(0,68)

def goalKicks(team, heatmap=False):
    goalkeeper = data[(data.Action=='Goal-kicks') & (data.Team == team)].code.unique()[0]
    dataPasse = data[(data.Action=='Passes accurate') & (data.code == goalkeeper)]
    draw_pitch("papayawhip", "black", 'h', 'full')
    plt.suptitle(team, fontsize = 20, color='firebrick', family = 'monospace', fontweight = 'bold' )
    receveur_list = {}
    loc = [[], []]
    for i in dataPasse.index :
        passe = dataPasse.loc[i]
        timePasses = passe.start
        if 'Goal kicks' in list(data[data.start==timePasses].Action.unique()):
            typePasses = 'Goal-kicks'
        else :
            typePasses = 'Accurate passes'
        timeAction = min(data[(data.start > timePasses) & (data.start < timePasses+10)].start)
        Action = data[(data.start == timeAction) & (data.Team == team)]
        loc[0].append(Action.pos_x.unique()[0])
        loc[1].append(Action.pos_y.unique()[0])
        receveur = data[(data.start == timeAction) & (data.Team == team)].code.unique()[0]
        if receveur in receveur_list :
            receveur_list[receveur] += 1
        else :
            receveur_list[receveur] = 1
        if typePasses == 'Accurate passes':
            plt.scatter(passe.pos_x, passe.pos_y, marker = 'x', color='blue', s=100, zorder=3)
            plt.scatter(Action.pos_x, Action.pos_y, marker = 'o', color='blue', s=100, zorder=3)
            plotPasse(passe.pos_x,passe.pos_y,Action.pos_x,Action.pos_y, col='blue')
        elif typePasses == 'Goal-kicks':
            plt.scatter(passe.pos_x, passe.pos_y, marker = 'x', color='red', s=100, zorder=3)
            plt.scatter(Action.pos_x, Action.pos_y, marker = 'o', color='red', s=100, zorder=3)
            plotPasse(passe.pos_x,passe.pos_y,Action.pos_x,Action.pos_y, col='red')
    legend_elements = [Line2D([0], [0], marker='X', color='papayawhip', label='Goal throwing location',markerfacecolor='black', markersize=15),
                       Line2D([0], [0], marker='o', color='papayawhip', label='Target',markerfacecolor='black', markersize=10)]
    plt.legend(handles=legend_elements, loc='center', bbox_to_anchor=(0.48,1.04),fontsize='x-large', ncol=2, frameon = False)    
    plt.text(42.5, -3, 'In-game passes', ha='center', fontsize=20, color='blue')
    plt.text(60.5, -3, 'Goal-kick', ha='center', fontsize=20, color='red')
    if heatmap == True :
        print(loc[0])
        print(loc[1])
        ax = sns.kdeplot(np.array(loc[0]), np.array(loc[1]), shade = "True", cmap = "YlOrRd", n_levels = 50, zorder=1)
        ax.collections[0].set_alpha(0)
    plt.show()
    plt.figure(figsize=(10,7))
    plt.bar(np.arange(len(receveur_list)), [receveur_list[i] for i in receveur_list], color='firebrick')
    plt.grid(True)  
    plt.xticks(np.arange(len(receveur_list)-0.3), [i.split()[-1] for i in receveur_list], rotation = 60, size=15)
    plt.yticks(size=15)


goalKicks("St. Gallen", heatmap= True)

#########################################################################################
################################### Ellipses ############################################
#########################################################################################

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of `x` and `y`

    Parameters
    ----------
    x, y : array_like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    Returns
    -------
    matplotlib.patches.Ellipse

    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimenLausannel dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse), mean_x, mean_y

def ellipse(team, deb=0, fin=max(data.start)//60):
    players = data[data.Team == team].code.unique()
    fig, ax_nstd = plt.subplots(figsize=(15,9.5))
    draw_pitch("lightgrey", "black", "h", "full", ax=ax_nstd)
    for player in players[:11] :
        action = data[(data.code == player) & (data.start >= deb*60) & (data.start <= fin*60 )]
        ax_nstd.scatter(action.pos_x, action.pos_y, s=0.5, color='lightgrey')
        p, x, y = confidence_ellipse(action.pos_x, action.pos_y, ax_nstd, n_std=0.5, label=r'$1\sigma$', edgecolor='gold', linewidth=3, fill=True, facecolor='orange', alpha=0.2)
        plt.text(x, y, player.split()[0][:-1], ha="center", va="center",fontsize = 15, family = 'monospace', fontweight = 'bold')
        plt.title(team, fontsize = 30, color='firebrick', family = 'monospace', fontweight = 'bold' )
    plt.show()
ellipse("St. Gallen")
