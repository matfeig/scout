# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 00:00:20 2020

@author: peter
"""

import pandas as pd
import matplotlib.pyplot as plt
#import plotly.graph_objects as go
import matplotlib.patches as patches
import numpy as np

def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    #Pitch = plt.Rectangle([0,0], width = 120, height = 80, fill = False)
    Pitch = plt.Rectangle([0,0], width = 105, height = 68, fill = False)
    #Left, Right Penalty Area and midline
    #LeftPenalty = plt.Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False)
    LeftPenalty = plt.Rectangle([0,16.3], width = 14.6, height = 35.3, fill = False)
    #RightPenalty = plt.Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False)
    RightPenalty = plt.Rectangle([90.4,16.3], width = 14.6, height = 35.3, fill = False)
    #midline = patches.ConnectionPatch([60,0], [60,80], "data", "data")
    midline = patches.ConnectionPatch([52.5,0], [52.5,68], "data", "data")

    #Left, Right 6-yard Box
    #LeftSixYard = plt.Rectangle([0,32], width = 4.9, height = 16, fill = False)
    #RightSixYard = plt.Rectangle([115.1,32], width = 4.9, height = 16, fill = False)
    LeftSixYard = plt.Rectangle([0,26], width = 4.9, height = 16, fill = False)
    RightSixYard = plt.Rectangle([100.1,26], width = 4.9, height = 16, fill = False)
    
    #Prepare Circles
    #centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    #centreSpot = plt.Circle((60,40),0.71,color="black")
    centreCircle = plt.Circle((52.5,34),8.1,color="black", fill = False)
    centreSpot = plt.Circle((52.5,34),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    #leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    #rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftPenSpot = plt.Circle((9.7,34),0.71,color="black")
    rightPenSpot = plt.Circle((95.3,34),0.71,color="black")
    
    #leftArc = patches.Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    #rightArc = patches.Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    leftArc = patches.Arc((9.7,34),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = patches.Arc((95.3,34),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    for i in element:
        ax.add_patch(i)
 
def getGKDF(df,team):
    xpos_gk = []
    ypos_gk = []
    receiver = []
    xpos_rec = []
    ypos_rec = []
    action = []
    for index, row in df.iterrows():
        if(row['Action']=='Goal kicks' and row['Team']==team):
            tmp_passer = row['code']
            xpos_gk.append(row['pos_x'])
            ypos_gk.append(row['pos_y'])
           # print('Goal Kick!')
            find_receiver = False
            i = 1
            while not find_receiver:
                if(index+i >= len(df.index)):
                    break
                if(df.iloc[index+i]['code']!=tmp_passer and df.iloc[index+i]['Team']==team):
                    tmp_receiver = df.iloc[index+i]['code']
                    tmp_xpos_rec = df.iloc[index+i]['pos_x']
                    tmp_ypos_rec = df.iloc[index+i]['pos_y']
                    tmp_time = df.iloc[index+i]['start']
                    find_receiver = True
                else:
                    i = i+1
            receiver.append(tmp_receiver)
            xpos_rec.append(tmp_xpos_rec)
            ypos_rec.append(tmp_ypos_rec)
            tmp_df = df.loc[(df['start']==tmp_time) & (df['Team']==team)]
            action.append(tmp_df)
    return receiver,xpos_rec,ypos_rec,action,xpos_gk,ypos_gk
       
df1 = pd.read_csv('luz_yb.csv')
receiver1,xpos_rec1,ypos_rec1,action1,xpos_gk1,ypos_gk1 = getGKDF(df1,'Young Boys')

df2 = pd.read_csv('lau_yb.csv')
receiver2,xpos_rec2,ypos_rec2,action2,xpos_gk2,ypos_gk2 = getGKDF(df2,'Young Boys')

xpos_rec = xpos_rec1+xpos_rec2
ypos_rec = ypos_rec1+ypos_rec2
receiver = receiver1+receiver2
xpos_gk = xpos_gk1+xpos_gk2
ypos_gk = ypos_gk1+ypos_gk2

fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
draw_pitch(ax1)
ax1.scatter(xpos_rec,ypos_rec,c='red',s=120,zorder=3)
i=0
for pl in receiver:
    text = pl.split('.')[0]
    if(int(text)>9):
        ax1.annotate(text, (xpos_rec[i]-1.8, ypos_rec[i]-1.0),zorder=4,fontsize=8.5,color="white",weight='bold')
    else:
        ax1.annotate(text, (xpos_rec[i]-1., ypos_rec[i]-1.0),zorder=4,fontsize=8.5,color="white",weight='bold')
    ax1.arrow(xpos_gk[i],ypos_gk[i],xpos_rec[i]-xpos_gk[i],ypos_rec[i]-ypos_gk[i],width=0.1,color="white",head_width=0.8,linestyle=":")
    i+=1
    
ax1.set_facecolor('xkcd:green')
fig.suptitle("Goal kicks of Team", fontsize=16)
fig.savefig('GoalKick_Map_FC Team.pdf')


