#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 16:37:21 2023

@author: matfeig
"""
from statsbombpy import sb
import pandas as pd
import numpy as np
from mplsoccer import VerticalPitch, add_image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as font_manager
from scipy.ndimage import gaussian_filter
from matplotlib import patches

user="m.feigean@servettefc.ch" #replace between the quotation marks with the email address that you use to login to StatsBomb IQ
password="QzG3Kdlu" #replace between the quotation marks with the password that you use to login to StatsBomb IQ

team="Servette" #must be same spelling as appears in StatsBomb IQ
competition=80 #StatsBomb's competition id
season=281 #StatsBomb's season id

league="Super League"
season_title="2023/24"

#you can change any of the colours on the data viz should you wish to do so
bgcolor="white"
textc="black"
white="white"
sbred='#e21017'
lightgrey="#d9d9d9"
darkgrey='#9A9A9A'
linec=darkgrey
cmaplist = [white, darkgrey, sbred]
cmap = LinearSegmentedColormap.from_list("", cmaplist)
path_eff = [path_effects.Stroke(linewidth=2, foreground=darkgrey), path_effects.Normal()]


#Choosing matches from competitions and season
matches = sb.matches(competition_id= competition, season_id=season,creds = {"user": user, "passwd": password})

team_matches = matches[(matches['home_team'] == team)|(matches['away_team'] == team)]
team_matches = team_matches[team_matches["match_status"]=="available"]
list_matches=team_matches.match_id.tolist()

#load events from specific matches (faster than pulling a whole competition season)
events = []
for n in list_matches:
    match_events = sb.events(match_id = n,creds= {"user": user, "passwd": password})
    events.append(match_events)
events=pd.concat(events)

#filtering by specific event -> corners
corners = events[events["pass_type"] == "Corner"]

### parse relevant columns to get start and end point of actions
corners[['x', 'y']] = corners['location'].apply(pd.Series)
corners[['pass_end_x', 'pass_end_y']] = corners['pass_end_location'].apply(pd.Series)

#filling blank cells with short corner technique
corners['pass_technique'] = corners['pass_technique'].fillna("Short")

#filter dataframe to get only corners by focus team
focus_corners=corners[(corners['team'] == team)]

#identify corners by backpost, frontpost and penspot
conditions=[((abs(focus_corners['y']-focus_corners['pass_end_y'])) > 43)
& (focus_corners['pass_technique']!="Short")]
values=[1]
focus_corners['backpost']=np.select(conditions, values)

conditions=[((abs(focus_corners['y']-focus_corners['pass_end_y'])) < 37 )
& (focus_corners['pass_technique']!="Short")]
values=[1]
focus_corners['frontpost']=np.select(conditions, values)

conditions=[(focus_corners['backpost']==0) & (focus_corners['frontpost']==0) 
& (focus_corners['pass_technique']!="Short")]
values=[1]
focus_corners['penspot']=np.select(conditions, values)

#separating by left and right corners in own team and also in opposition team
left_corners=focus_corners[(focus_corners['y']<=40) & (focus_corners['x']>=60)]
right_corners=focus_corners[(focus_corners['y']>=40)& (focus_corners['x']>=60)]


#getting the stats of the corners from right and from left : totals, shorts, backposts, etc.def get_corner_stats (data):
def get_corner_stats (data):

    #get total corners
    total=len(data)
    
    # shot, front, back
    short=len(data[(data['pass_technique']=='Short')])*100
    short=round(short/total,1)
    backpost=len(data[(data['backpost']==1)])*100
    backpost=round(backpost/total,1)
    frontpost=len(data[(data['frontpost']==1)])*100
    frontpost=round(frontpost/total,1)
    penspot=len(data[(data['penspot']==1)])*100
    penspot=round(penspot/total,1)
    
    #six-yard, deeper
    sixyard=len(data[(data['pass_end_x']>=114)&(data['pass_technique']!='Short')])*100
    sixyard=round(sixyard/total,1)
    deeper=len(data[(data['pass_end_x']<114)&(data['pass_technique']!='Short')])*100
    deeper=round(deeper/total,1)
    
    goals=len(data[(data['pass_goal_assist']==True)])
    shots_df=data[(data['pass_shot_assist']==True)]
    shots=len(shots_df)
    total_corners=len(data)
    
    shot_ids=shots_df.pass_assisted_shot_id.tolist()

    if len(shot_ids)>0:
       xg_df = []
       for n in shot_ids:
           xg_shot = events[(events['id']==n)]
           xg_df.append(xg_shot)
       xg_df=pd.concat(xg_df)
    
       xg=round(xg_df.shot_statsbomb_xg.sum(),2)
    else:
       xg=0
    
    if data.y.mean()>=40:
        side="right"
    else:
        side="left"
    
    return side, total, short, backpost, frontpost, penspot, sixyard, deeper, goals, shots, total_corners, xg

#define function for removing axis on subplots
def customise_plot(ax):
    for n in ["right","top","left","bottom"]:
        ax.spines[n].set_visible(False)
        ax.patch.set_facecolor(bgcolor)
        ax.tick_params(bottom=False,top=False,labelbottom=False)
        
#create bar chart
def plot_bar (data,groupby,taker_or_target,ax):
    
    target = data.groupby([groupby]).size()
    target=target.reset_index()
    target.rename(columns={target.columns[1]: taker_or_target }, inplace = True)
    target=target.sort_values(taker_or_target, ascending=False)
    target = target.head(5)
    target=target.sort_values(taker_or_target)
    
    bars = target[groupby]
    h = target[taker_or_target]
    y_pos = np.arange(len(bars))

    ax.barh(y_pos, h, color=sbred, edgecolor=darkgrey)
    
    # Create names on the x-axis
    ax.set_yticks(y_pos)
    ax.set_yticklabels(bars,color=textc,size=24)
    
    customise_plot(ax)
    
    text=target[taker_or_target].astype(int)
    for i, v in enumerate(text):
            ax.text(v*0.9, i-0.09, str(v), color=textc, fontsize=28,fontweight="bold",ha='center')
                   
#plotting the data
def plot_corners (data,axA,axB,axC):
    
    #calculate data points
    side, total, short, backpost, frontpost, penspot, sixyard, deeper, goals, shots, total_corners, xg = get_corner_stats (data)
    
    #create a new dataframe that doesn't include short corners
    non_short_df=data.loc[(data['pass_technique']!='Short')]
    
    #create heatmap of end point of crosses
    bin_statistic=pitch.bin_statistic(non_short_df['pass_end_x'], non_short_df['pass_end_y'], statistic='count', bins=(40,30))
    bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
    pitch.heatmap(bin_statistic, edgecolors=bgcolor, cmap=cmap, ax=axA,alpha=0.75)
    
    if side=="left":
        x1_label=26.9 #front post
        x2_label=52.9 #back post
        x3_label=79.9 #6-yard/deeper
        x4_label=3 #short corner
        x4_circle=0 #start point
        
        total=len(data)
        inswinger=len(data.loc[(data['pass_technique']=="Inswinging")])
        inswinger=int(inswinger/total*100)
        lw_i=inswinger/10
        
        outswinger=len(data.loc[(data['pass_technique']=="Outswinging")])
        outswinger=int(outswinger/total*100)
        lw_o=outswinger/10
        
        #inswinger
        style = "Simple, tail_width=0.5, head_width=16, head_length=12"
        a1 = patches.FancyArrowPatch((x4_circle,120), (25,105),
                                 connectionstyle="arc3,rad=.2", color=darkgrey,arrowstyle=style,
                                 lw=lw_i,zorder=5,alpha=1)
        axA.add_patch(a1)
        
        #outswinger
        a2 = patches.FancyArrowPatch((x4_circle,120), (25,110),
                                 connectionstyle="arc3,rad=-0.28", color=darkgrey,arrowstyle=style,
                                 lw=lw_o,zorder=5,alpha=1)
        axA.add_patch(a2)
        
        axA.text(s=f"Rentrant: {inswinger}%",x=x4_circle-5,y=105,size=26,color=darkgrey,ha="center",fontweight='bold')
        axA.text(s=f"Sortant: {outswinger}%",x=x4_circle-5,y=125,size=26,color=darkgrey,ha="center",fontweight='bold')

        
    elif side=="right":
        x1_label=52.9
        x2_label=26.9
        x3_label=3
        x4_label=79.9 
        x4_circle=80
        
        total=len(data)
        inswinger=len(data.loc[(data['pass_technique']=="Inswinging")])
        inswinger=int(inswinger/total*100)
        lw_i=inswinger/10
        
        outswinger=len(data.loc[(data['pass_technique']=="Outswinging")])
        outswinger=int(outswinger/total*100)
        lw_o=outswinger/10
        
        #outswinger
        style = "Simple, tail_width=0.5, head_width=16, head_length=12"
        a1 = patches.FancyArrowPatch((x4_circle,120), (55,110),
                                 connectionstyle="arc3,rad=.2", color=darkgrey,arrowstyle=style,
                                 lw=lw_o,zorder=5,alpha=1)
        axA.add_patch(a1)
        
        #inswinger
        a2 = patches.FancyArrowPatch((x4_circle,120), (55,105),
                                 connectionstyle="arc3,rad=-0.28", color=darkgrey,arrowstyle=style,
                                 lw=lw_i,zorder=5,alpha=1)
        axA.add_patch(a2)
        
        axA.text(s=f"Rentrant: {inswinger}%",x=x4_circle+5,y=105,size=26,color=darkgrey,ha="center",fontweight='bold')
        axA.text(s=f"Sortant: {outswinger}%",x=x4_circle+5,y=125,size=26,color=darkgrey,ha="center",fontweight='bold')

    
    #add circle to highlight which side the corner is taken from
    a_circle = plt.Circle((x4_circle, 120), 3, zorder=5, fill=False,edgecolor=sbred,lw=5,ls="-")
    axA.add_artist(a_circle)
    

    
    
    #plot data relating to target areas
    axA.text(s=f"Total corners: {total}",x=40,y=128,size=32,color=textc,ha='center')
    axA.text(s=f"Premier poteau: {frontpost}%",x=x1_label,y=63,size=28,color=textc,rotation=270,ha="center",path_effects=path_eff)
    axA.text(s=f"Zone penalty: {penspot}%",x=40,y=63,size=28,color=textc,rotation=270,ha="center",path_effects=path_eff)
    axA.text(s=f"Second poteau: {backpost}%",x=x2_label,y=63,size=28,color=textc,rotation=270,ha="center",path_effects=path_eff)
    
    axA.axvline(x=37, ymin=0.5, ymax=0.875,color=darkgrey, lw=3, linestyle='--')
    axA.axvline(x=43, ymin=0.5, ymax=0.875,color=darkgrey, lw=3, linestyle='--') 
    axA.text(s=f"5 mètres: {sixyard}%",x=x3_label,y=115,size=28,color=textc,ha="center",path_effects=path_eff)
    axA.text(s=f"Eloigné: {deeper}%",x=x3_label,y=107,size=28,color=textc,ha="center",path_effects=path_eff)
    axA.text(s=f"Corners\ncourt: {short}%",x=x4_label,y=92.5,size=24,color=textc,ha="center",path_effects=path_eff)
    axA.text(s=f"Buts: {goals} | Shots: {shots} | xG: {xg}",x=40,y=122,size=30,color=sbred,ha="center")
    
    #BAR CHART for first contacts
    plot_bar (non_short_df,'pass_recipient','target',axB)
    
    #BAR CHART for corner kick takers
    plot_bar (data,'player','corners_taken',axC)

#set dimensions of the pitch
pitch = VerticalPitch(half=True,pitch_type='statsbomb',
pitch_color=bgcolor, line_color=linec,line_zorder=1,pad_top=10)

#set figure size and dimensions
fig = plt.figure(figsize=(36,30),constrained_layout=True)
gs = fig.add_gridspec(nrows=3,ncols=4)
fig.patch.set_facecolor(bgcolor)

#plot results for left side corners 
ax1 = fig.add_subplot(gs[0,1:3])
ax1.set_title(label="Corners depuis Gauche",x=0.5,y=1.04,size=30,color=textc,ha='center',fontweight='bold')
pitch.draw(ax=ax1)
ax2 = fig.add_subplot(gs[0,3])
ax2.set_title(label="Top 5 - Joueurs cibles\n depuis la gauche\n(Corners à 2 sont exclus)",x=0.5,y=1.02,size=26,color=textc,ha='center',fontweight='bold')
ax3 = fig.add_subplot(gs[0,0])
ax3.set_title(label="Top 5 - Tireur Corner Gauche",x=0.5,y=1.02,size=26,color=textc,ha='center',fontweight='bold')
plot_corners (left_corners,ax1,ax2,ax3)

#plot results for right side corners 
ax4 = fig.add_subplot(gs[1,1:3])
ax4.set_title(label="Corners depuis Droite",x=0.5,y=1.04,size=30,color=textc,ha='center',fontweight='bold')
pitch.draw(ax=ax4)
ax5 = fig.add_subplot(gs[1,3])
ax5.set_title(label="Top 5 - Joueurs cibles\ndepuis droite\n(Corners à 2 sont exclus)",x=0.5,y=1.02,size=26,color=textc,ha='center',fontweight='bold')
ax6 = fig.add_subplot(gs[1,0])
ax6.set_title(label="Top 5 - Tireur Corner Droite",x=0.5,y=1.02,size=26,color=textc,ha='center',fontweight='bold')
plot_corners (right_corners,ax4,ax5,ax6)

#set titles
fig.text(s=f"{team} Corners | {league} {season_title}", #ha='center'
x=0.02, y =1.09, fontsize=54,color=textc,fontweight='bold')

fig.text(s="Goals, tirs & xG : Premier contract sur corner.\nData visualisation \nMathieu Feigean", #ha='center'
x=0.02, y =1.02, fontsize=36,color=sbred)


