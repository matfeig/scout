#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 10:54:29 2023

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Arc
import seaborn as sns
from mplsoccer.pitch import Pitch, VerticalPitch
import tqdm
from matplotlib.animation import FuncAnimation, writers
from matplotlib.collections import LineCollection
import highlight_text
import matplotlib.font_manager
from IPython.core.display import HTML
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cmasher as cmr
from mplsoccer import VerticalPitch
from mplsoccer.utils import FontManager
from highlight_text import fig_text
from pywaffle import Waffle # PyWaffle Documentation --> https://buildmedia.readthedocs.org/media/pdf/pywaffle/latest/pywaffle.pdf
import matplotlib.pyplot as plt #Matplotlib pyplot to plot the charts
import matplotlib as mpl
from highlight_text import htext #used for highlighting the title
import matplotlib.font_manager as fm
from matplotlib import rcParams
from highlight_text import fig_text
#from PIL import Image
import urllib
import os
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches
from urllib.request import urlopen
import matplotlib.pyplot as plt
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from weasyprint import HTML
from mizani.formatters import percent_format
#from plotnine import *
import matplotlib.patches as patches
import matplotlib.colors as mcolors
#####################
### download data ###
#####################

df2 = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/yverdon_sfc_3.csv")
df1 = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/event_match/23_24/yverdon_sfc_3.csv")
#df3 = pd.read_csv("/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/GPS/23_24/sfc_slavia.csv", sep=',')


df1['player_name'] = df1['player_name'].replace({
    'Timothé Cognat': 'Timothe Cognat'
})

###Clean data  ####
# Find the index of the event after which you want to drop all rows
end_idx = df1[(df1['period'] == 2) & (df1['event_type_name'] == 'Half End')].index.min()

# Drop all rows after this index
df1 = df1.loc[:end_idx]


#############################
### Test d'automatisation ###
#############################

#Select players with desired positions and team
desired_positions = ["Left Defensive Midfield"]

servette_players = df1.loc[(df1["team_name"] == "Servette") & df1["player_position_name"].isin(desired_positions)]["player_name"].unique()

# servette_players = np.delete(servette_players, 1, axis=0)
# servette_players = np.delete(servette_players, 1, axis=0)
    
#############################
###     Ballon touchés    ###
#############################


#servette_players = df1.loc[(df1["team_name"] == "Servette") & df1["player_position_name"].isin(desired_positions)]["player_name"].unique()

for player_name in servette_players:
    # Select events for each player
    player = df1.loc[df1['player_name'] == player_name]
    playe = df2.loc[df2['player_name'] == player_name]
    
    # Select ball receipt events
    pos = player.loc[(player.event_type_name == "Ball Receipt*")] 
    miss = player.loc[(player.event_type_name == "Miscontrol") |
                      (player.event_type_name == "Dispossessed")|
                      ((player.event_type_name == "Ball Receipt*") & (player.outcome_name == "Incomplete"))]
    
    # Calculate the ratio
    if len(pos) + len(miss) == 0:  # Avoid division by zero
        ratio = 0
    else:
        ratio = len(pos) / (len(pos) + len(miss))
    

    # Plot ball receipt events
    pitch = VerticalPitch(line_zorder=2, line_color='black', linewidth=1)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
    pitch.kdeplot(pos.location_x, pos.location_y, ax=ax['pitch'], cmap='Blues', fill=True, levels=100)
    pitch.scatter(pos.location_x, pos.location_y, alpha=1, s=30, color="black", ax=ax['pitch'])
    pitch.scatter(miss.location_x, miss.location_y, alpha=1, s=30, color="red", ax=ax['pitch'])
    fig_text(0.07, 0.04, "Red - Ball Lost | " + player_name, color="black", fontweight="bold", fontsize=10, backgroundcolor='white')
    
    # Display the ratio on the top-right corner of the figure
    ax['pitch'].text(0.35, 1, f"Ratio réussi: {ratio:.2%}", 
                     color='black', ha='right', va='top', transform=ax['pitch'].transAxes, fontsize=12)
    
    fig.suptitle("Ballon Touchés", fontsize=22, fontweight="bold", color="black")
    filepath = os.path.join('/Users/matfeig/Documents/SFC/rapport', f'balltouch_{player_name}.png')
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.show()
    
    
#########################
### Plot pass & Carry ###
#########################

for player in servette_players:
    mask = (df1['player_name'] == player) & (df1['team_name'] == "Servette")
    df_player = df1.loc[mask, :]
    
    # Additional mask to ensure only events during 'Regular Play' are considered
    mask_regular_play = df_player['play_pattern_name'] == "Regular Play"
    df_player = df_player.loc[mask_regular_play, :]
    
    passes = df_player.loc[df_player['event_type_name'] == 'Pass'].set_index('id')

    mask_bronze = (df_player.event_type_name == 'Pass')
    df_pass = df_player.loc[mask_bronze, ['location_x', 'location_y', 'end_location_x', 'end_location_y']]
    mask_bronz = (df_player.event_type_name == 'Carries')
    df_cary = df_player.loc[mask_bronz, ['location_x', 'location_y', 'end_location_x', 'end_location_y']]
    mask_bron = (df_player.event_type_name == 'Dribble')
    df_dribble = df_player.loc[mask_bron, ['location_x', 'location_y']]
    
    # Calculating positive and negative x changes
    df_player['x_change'] = df_player['end_location_x'] - df_player['location_x']
    positive_x = df_player['x_change'][df_player['x_change'] > 0].sum()
    negative_x = df_player['x_change'][df_player['x_change'] < 0].sum()
    
    # Calculating the ratio
    if len(df_player) > 0:
        ratio_x_per_event = positive_x / len(df_player)
    else:
        ratio_x_per_event = 0

    pitch = VerticalPitch(line_color='black', linewidth=1)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
    
    for i, row in df_pass.iterrows():
        if row["end_location_x"] >= 0 and row["end_location_x"] <= 100 and \
            row["end_location_y"] >= 0 and row["end_location_y"] <= 80:
            color = "grey"
        else:
            color = "tan"
        pitch.arrows(row["location_x"], row["location_y"],
                    row["end_location_x"], row["end_location_y"],width=2,
                    headwidth=4, headlength=4, color=color, ax=ax['pitch'])
   
    for i, row in df_cary.iterrows():
       if row["end_location_x"] >= 0 and row["end_location_x"] <= 100 and \
           row["end_location_y"] >= 0 and row["end_location_y"] <= 80:
           color = "black"
       else:
           color = "black"
       pitch.arrows(row["location_x"], row["location_y"],
                   row["end_location_x"], row["end_location_y"],width=2,
                   headwidth=4, headlength=4,linestyle='--',color=color, ax=ax['pitch'])        
    
    pitch.scatter(df_dribble.location_x, df_dribble.location_y, alpha = 0.9, s = 30, color = "blue", ax=ax['pitch'])
    fig_text(0.07,0.04,f"Noir - Passes | Gris - Conduite | Bleu - Dribble - {player}", color = "black",fontweight = "bold", fontsize = 8,backgroundcolor='white')
    ax['pitch'].axhline(y=80, xmin=0, xmax=100, color='grey', linestyle='--')
    # Displaying the calculated sums in the top-left corner
    ax['pitch'].text(0, 1, f"Vers l'avant': {positive_x:.2f} | Vers l'arrière': {negative_x:.2f}", 
                    color='black', ha='left', va='top', transform=ax['pitch'].transAxes, fontsize=10)
    ax['pitch'].text(1, 1, f"Ratio: {ratio_x_per_event:.2f} m en moyenne", 
                    color='black', ha='right', va='top', transform=ax['pitch'].transAxes, fontsize=10)
   
    
    fig.suptitle("Passes Carries Dribbles", fontsize = 22, fontweight = "bold")
    
    filepath = os.path.join('/Users/matfeig/Documents/SFC/rapport', f'event_{player}.png')
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.show() 


#calculate the number of passes in the surface area and plot it in the pitch 

###########################
####### Defensive activities ##
###############################

for player_name in servette_players:
    # Select events for each player
    player = df1.loc[df1['player_name'] == player_name]
    
    tot = player.loc[(player.event_type_name == "Interception") |
                     (player.event_type_name == "Ball recovery") |
                     (player.event_type_name == "Duel")|
                     (player.event_type_name == "Dribbled Past") |
                     ((player.event_type_name == "Duel") & (player.type_name == "Aerial Lost"))|
                     (player.event_type_name == "Block") |
                     (player.event_type_name == "Clearance")]
    
    
    pos = player.loc[(player.event_type_name == "Interception") |
                      (player.event_type_name == "Ball recovery") |
                      (player.event_type_name == "Duel")]          
                     
    miss = player.loc[(player.event_type_name == "Dribbled Past") |
                      ((player.event_type_name == "Duel") & (player.type_name == "Aerial Lost"))]  

    de = player.loc[(player.event_type_name == "Block") |
                      (player.event_type_name == "Clearance")]
                     
                     

    # Plot ball receipt events
    pitch = VerticalPitch(line_zorder=2, line_color='black', linewidth=1)
    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
    pitch.kdeplot(tot.location_x, tot.location_y, ax=ax['pitch'], cmap='YlOrRd', fill=True, levels=10, alpha= 0.3)
    pitch.scatter(pos.location_x, pos.location_y, alpha=1, s=30, color="blue", ax=ax['pitch'])
    pitch.scatter(miss.location_x, miss.location_y, alpha=1, s=30, color="red", ax=ax['pitch'])
    pitch.scatter(de.location_x, de.location_y, alpha=1, s=30, color="black", ax=ax['pitch'])
    
    #fig_text(0.07, 0.04, "Defensive activity | " + player_name, color="black", fontweight="bold", fontsize=12, backgroundcolor='white')
    fig_text(0.07,0.04,"Blue - Good Def | Red - Lost | Black - Urgence", color = "black",fontweight = "bold", fontsize = 8,backgroundcolor='white')

    fig.suptitle("Defensive territory", fontsize=22, fontweight="bold", color="black")
    filepath = os.path.join('/Users/matfeig/Documents/SFC/rapport', f'def_{player_name}.png')
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.show()  
    
##### Pressure map  ######


for player_name in servette_players:
    player_data = df1.loc[(df1["player_name"] == player_name) & (df1["event_type_name"] == "Pressure")]
    

    if player_data.empty:
        pitch = VerticalPitch(line_zorder=2, line_color='black', half=False, linewidth=1)
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                             endnote_height=0.04, title_space=0, endnote_space=0)
        fig.suptitle("No Pressure event found for this player", fontsize=26, fontweight="bold", color="black")
        plt.show()
    else:
        total_pressures = len(player_data)
        total_duration = player_data['duration'].sum()
        average_duration_per_pressure = total_duration / total_pressures if total_pressures > 0 else 0

        pitch = VerticalPitch(line_zorder=2, line_color='black', half=False, linewidth=1)
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                             endnote_height=0.04, title_space=0, endnote_space=0)
        #pitch.kdeplot(player_data.location_x, player_data.location_y, ax=ax['pitch'], cmap='Blues', fill=True, levels=100,)
        for i, row in player_data.iterrows():
            if row["counterpress"] == True:
                pitch.scatter(row.location_x, row.location_y, alpha=1, s=1000*np.sqrt(row.duration), color="red", ax=ax['pitch'])
            else:
                pitch.scatter(row.location_x, row.location_y, alpha=0.2, s=1000*np.sqrt(row.duration), color="black", ax=ax['pitch'])

        fig_text(0.07, 0.04, "", color="black", fontweight="bold", fontsize=12, backgroundcolor='white')
        fig.suptitle("Action Pressing", fontsize=26, fontweight="bold", color="black")
        fig_text(0.07, 0.04, f"Red - Counterpressing for {player_name}", color="black", fontweight="bold", fontsize=12, backgroundcolor='white')
        ax['pitch'].text(0.03, 1, f"Pressures: {total_pressures}", color='black', ha='left', va='top', transform=ax['pitch'].transAxes, fontsize=14)
        ax['pitch'].text(0.97, 1, f"Duration avg: {average_duration_per_pressure:.2f}", color='black', ha='right', va='top', transform=ax['pitch'].transAxes, fontsize=14)
        #plt.tight_layout()
        filepath = os.path.join('/Users/matfeig/Documents/SFC/rapport', f'pressure_{player_name}.png')
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        

### Time series ###
  
for player in servette_players:
    # Get data where obv_total_net is not NaN
    player_data = df1.loc[(df1["team_name"] == "Servette") & (df1["player_name"] == player) & (~df1['obv_total_net'].isna())]
    
    # Check if player_data is not empty
    if not player_data.empty:
        fig = plt.figure(figsize=(16,6))
        axes = fig.add_subplot(1,1,1)
        
        # Find the range of obv_total_net
        # min_obv = player_data['obv_total_net'].min()
        # max_obv = player_data['obv_total_net'].max()
        
        min_obv = -0.0010029767
        max_obv = 9.921808E-4
        
        
        # Calculate the sum of obv_total_net * 100
        sum_obv = (player_data['obv_total_net'] * 10).sum()
        
    
        # Create a colormap and normalize based on obv_total_net range
        cmap = plt.cm.coolwarm
        norm = mcolors.Normalize(vmin=min_obv, vmax=max_obv)
        
        # Plot the data using stem plot with colors according to obv_total_net
        for _, row in player_data.iterrows():
            markerline, stemlines, baseline = axes.stem([row['minute']], [row['location_x']], use_line_collection=True, basefmt=' ')
            plt.setp(stemlines, 'color', cmap(norm(row['obv_total_net'])))
            plt.setp(markerline, 'color', cmap(norm(row['obv_total_net'])))
        
        # Set the y-axis value range
        axes.set_ylim(0, 124)
        
        # Format the chart
        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)
        axes.set_xlim([-1, 95])
        plt.xticks(np.arange(0, 95, 5))
        axes.set_title(f'Contribution au jeu - Menace: {sum_obv:.2f} | de -4 à +8 (Rouge + et Bleu -)', fontsize=18, fontweight="bold", color="black", pad=15)
        axes.set_xlabel('Match Time', color="black", fontweight="bold", fontsize=12)
        axes.set_ylabel('Pitch Height', color="black", fontweight="bold", fontsize=12)
        
        # Add a shaded area from y=60 to y=120 with a label
        axes.axhspan(60, 124, facecolor='lightgrey', alpha=0.16)  # `alpha` is for transparency
        axes.text(80, 117, "Moitié de terrain adv", fontsize=12, color="black", va="center", ha="left", backgroundcolor='lightgrey')
        axes.text(80, 5, "Moitié de terrain SFC", fontsize=12, color="black", va="center", ha="left", backgroundcolor='lightgrey')

        # Calculate and display statistics
        events_opponent_half = player_data[player_data['location_x'] > 60].shape[0]
        events_sfc_half = player_data[player_data['location_x'] <= 60].shape[0]
        events_per_minute = player_data.shape[0] / 90  # Assuming a match duration of 90 minutes
    
        light_white = (1, 1, 1, 0.7)  # RGBA for light white with 70% opacity
        bbox_props = dict(boxstyle="round,pad=0.3", facecolor=light_white, edgecolor=light_white, lw=2)
        axes.text(0.01, 0.98, f"Adv half: {events_opponent_half}", fontweight="bold",color='black', ha='left', va='top', transform=axes.transAxes, fontsize=12, bbox=bbox_props)
        axes.text(0.01, 0.93, f"SFC half: {events_sfc_half}",fontweight="bold", color='black', ha='left', va='top', transform=axes.transAxes, fontsize=12, bbox=bbox_props)
        axes.text(0.01, 0.88, f"Events/min: {events_per_minute:.2f}", fontweight="bold",color='black', ha='left', va='top', transform=axes.transAxes, fontsize=12, bbox=bbox_props)        
        filepath = os.path.join('/Users/matfeig/Documents/SFC/rapport', f'obv_{player}.png')
        fig.savefig(filepath, dpi=300, bbox_inches='tight')

        # Show the plot
        plt.show()


# #### Waffle ####

#player = ["Boubacar Fofana", "Hussayn Touati","Ronny Rodelin","Timothé Cognat", "Alexis Antunes","Chris Vianney Bedia", "Enzo Crivelli","Dereck Germano Kutesa","Jeremy Bruno Guillemenot","Miroslav Stevanović", "Alexis Antunes", "Bendegúz Bolla", "David Douline"]  # replace with actual player names
player = ["Gaël Ondoua"]

servette_player = list(set(df2['player_name']).intersection(set(player)))


for player in servette_player:
    player_data = df2.loc[(df2["team_name"] == "Servette") & (df2["player_name"] == player)]
    
    waf = player_data[['player_name',
                       'player_match_forward_passes',
                       'player_match_op_key_passes',
                       'player_match_interceptions',
                       'player_match_tackles',
                       'player_match_deep_progressions',
                       'player_match_successful_aerials'
                       ]]
    
    waf = waf.rename(columns={'player_match_forward_passes': 'Passes_forward',
                              'player_match_op_key_passes':'key_passes',
                              'player_match_interceptions':'Interceptions',
                              'player_match_tackles':'Tackles',
                              'player_match_deep_progressions':'deep_progressions',
                              'player_match_successful_aerials':'aerials' ,
                              })

    # Transpose the data and set the columns to be the player names
    data = waf.T
    data.columns = data.iloc[0]
    data = data.drop('player_name')

    challenge = player_data['player_match_challenge_ratio'].sum()  # assuming you want the sum; adjust as needed
    passes = player_data['player_match_passing_ratio'].sum()  # assuming you want the sum; adjust as needed
    obv = player_data['player_match_obv'].sum()  # assuming you want the sum; adjust as needed
    xg = player_data['player_match_xgbuildup'].sum()  # assuming you want the sum; adjust as needed
    
    # Plot the waffle chart
    fig = plt.figure(
        FigureClass=Waffle, 
        rows=5,
        values=data[player],
        cmap_name="tab20c",
        labels=[f"{col}: {val}" for col, val in data[player].items()],
        legend={'loc': 'upper left', 'bbox_to_anchor': (1.1, 1)}
    )    
        
    #plt.title(f"{player}", fontsize=14, fontweight='bold')
    title_text = f"Apport au jeu | xG chain: {xg:.2f} & Passes Ratio: {passes:.2f}"
    fig.suptitle(title_text, fontsize=11, fontweight="bold", color="black", ha='center')
    #fig_text(0.07, 0.04, f"Apport au jeu Off | xG_chain : {xg:.2f} & OBV : {obv:.2f}", color="black", fontweight="bold", fontsize=11, backgroundcolor='white')
    filepath = os.path.join('/Users/matfeig/Documents/SFC/rapport', f'waffle_{player}.png')
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

    plt.show()


##  plot table athetic data ####  



# player = ["GUILLEMENOT","RODELIN","STEVANOVIC"] 

# # define the columns to display in the table
# params = ['Max Acceleration', 'Sprints', 'Max Speed', 'Accelerations Zone 5']
# min_range = [4, 2, 25, 2]
# max_range = [7.5,30, 36, 30]

# # instantiate PyPizza class
# baker = PyPizza(
#     params=params,
#     min_range=min_range,
#     max_range=max_range,
#     background_color="white", straight_line_color="#000000",
#     last_circle_color="#000000", last_circle_lw=2.5, straight_line_lw=1,
#     other_circle_lw=0, other_circle_color="#000000", inner_circle_size=20,
# )

# # iterate over each player
# for p in player:
#     # get the row of the player from the dataframe
#     player_row = df3.loc[df3['Player Last Name'] == p]

#     # get the values for the player
#     values = [player_row[param].values[0] for param in params]

#     # plot pizza
#     fig, ax = baker.make_pizza(
#         values,
#         figsize=(6, 6),
#         color_blank_space="same",
#         blank_alpha=0.4,
#         param_location=110,
#         kwargs_slices=dict(
#             facecolor="#1A78CF", edgecolor="#000000",
#             zorder=1, linewidth=1
#         ),
#         kwargs_params=dict(
#             color="black", fontsize=12, zorder=5, va="center"
#         ),
#         kwargs_values=dict(
#             color="#000000", fontsize=12, zorder=3,
#             bbox=dict(
#                 edgecolor="#000000", facecolor="#1A78CF",
#                 boxstyle="round,pad=0.2", lw=1
#             )
#         )
#     )

#     # set the title of the chart to the player's name
#     #ax.set_title(p, fontsize=20)
#     #fig.suptitle(f"{player}", fontsize=11, fontweight="bold", color="black")
#     fig.suptitle(f"{p}", fontsize=11, fontweight="bold", color="black" )
#     plt.show()



