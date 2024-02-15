#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 18:10:14 2023

@author: matfeig
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import matplotlib.pyplot as plt
from itertools import product
import seaborn as sns

import matplotlib.pyplot as plt
import six

# Function to adjust overlapping annotations
def stack_and_avoid_overlap(x, y, names):
    coord_to_name = {}
    
    for i, (xi, yi) in enumerate(zip(x, y)):
        key = None
        
        # Check if this point is close to a previously processed point based on both criteria
        for (xj, yj) in coord_to_name:
            if abs(xi - xj) < 30 and abs(yi - yj) < 10:
                key = (xj, yj)
                break
        
        # If not found a close point, use its own coordinates
        if key is None:
            key = (xi, yi)
        
        if key in coord_to_name:
            coord_to_name[key].append(names[i])
        else:
            coord_to_name[key] = [names[i]]
    
    for (xi, yi), stacked_names in coord_to_name.items(): 
        y_offset = 3
        for name in stacked_names:
            plt.annotate(name, (xi, yi + y_offset), fontsize=9, ha='center', va='bottom')
            y_offset += 6
            
# Load the previously uploaded Excel file
df_minutes_new = pd.read_excel('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/squad/minute.xlsx', index_col=0)

df_minutes_new.fillna("", inplace=True)

# Ensure all columns are numeric
for col in df_minutes_new.columns:
    df_minutes_new[col] = pd.to_numeric(df_minutes_new[col], errors='coerce')

# Initialize the player_columns_new variable based on the DataFrame columns
player_columns_new = df_minutes_new.columns
player_columns_new = [col for col in df_minutes_new.columns if col not in ["Opponent", "Team","Date"]]

player_x_values = {}
player_y_values = {}

# For each player, calculate the required values
for player in player_columns_new:
    player_data = df_minutes_new[player]
    
    # X-axis: cumulative sum of minutes played
    player_x_values[player] = player_data.sum()
    
    # Y-axis: sum of minutes from the last 3 games the player participated in (excluding NaN values)
    last_3_games_sum = []
    for idx in range(len(player_data)):
        # Get the last 3 games excluding NaN values
        valid_games = player_data.iloc[:idx+1].dropna()
        last_3_games = valid_games[-3:]
        last_3_games_sum.append(last_3_games.sum())
    
    player_y_values[player] = last_3_games_sum[-1]  # Taking the last value as it represents the most recent game

# Now, plotting the graph
plt.figure(figsize=(12, 7))

# Shading the regions based on the conditions
plt.axhspan(0, 350, xmin=1600/max(player_x_values.values()), xmax=max(player_x_values.values())/max(player_x_values.values()), facecolor='#255075', alpha=0.5)
plt.axhspan(0, 150, xmin=0, xmax=800/max(player_x_values.values()), facecolor='#abcae4', alpha=0.5)
plt.axhspan(100, 350, xmin=800/max(player_x_values.values()),xmax=1600/max(player_x_values.values()), facecolor='#3d84bf', alpha=0.5)
plt.axhspan(0, 100, xmin=800/max(player_x_values.values()),xmax=1600/max(player_x_values.values()), facecolor='#0b1925', alpha=0.5)
plt.axhspan(250,350, xmin=0,xmax=800/max(player_x_values.values()), facecolor='#316a9a', alpha=0.5)
plt.axhspan(150,250, xmin=0, xmax=800/max(player_x_values.values()), facecolor='#86b2d8', alpha=0.5)


# Annotate the regions
plt.text(1650, 335, "Key and Robust", fontsize=12, ha="left",fontweight='bold', color='white')
plt.text(5, 135, "Less used", fontsize=12, ha="left",fontweight='bold', color='white')
plt.text(5, 335, "Player of the moment", fontsize=12, ha="left",fontweight='bold', color='white')
plt.text(810, 335, "Core Player", fontsize=12, ha="left",fontweight='bold', color='white')
plt.text(5, 235, "Given Minutes", fontsize=12, ha="left",fontweight='bold', color='white')
plt.text(810,90, "Less Concerned", fontsize=12, ha="left",fontweight='bold', color='white')

plt.scatter(list(player_x_values.values()), list(player_y_values.values()), color='black')

# Stack annotations and avoid overlaps
stack_and_avoid_overlap(list(player_x_values.values()), list(player_y_values.values()), list(player_x_values.keys()))

# Remove the top x-axis and the right y-axis
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

plt.title("Total vs Last 3 games\nMinutes", fontsize=14, ha="center",fontweight='bold', color='black')
plt.xlabel("Total Minutes", fontsize=12, ha="center",fontweight='bold', color='black')
plt.ylabel("Minutes last 3 games", fontsize=12, ha="center",fontweight='bold', color='black')
plt.grid(True, linestyle='--',linewidth=0.5)
plt.tight_layout()
plt.show()


#### Slect Range of Date #############################################################################################################################

df_sample = pd.read_excel('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/squad/minute.xlsx', index_col=0)

# Filter the dataframe based on the provided date range
start_date = "2023-10-20"
end_date = "2023-11-02"
df_filtered = df_sample[(df_sample["Date"] >= start_date) & (df_sample["Date"] <= end_date)]

# Fill NaN values and ensure all columns are numeric
df_filtered.fillna("", inplace=True)
for col in df_filtered.columns:
    df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')

# Initialize the player_columns_new variable based on the filtered DataFrame columns
player_columns_new = [col for col in df_filtered.columns if col not in ["Opponent", "Team", "Date"]]

player_x_values = {}
player_y_values = {}

# For each player, calculate the required values based on the filtered dataframe
for player in player_columns_new:
    player_data = df_filtered[player]
    
    # X-axis: cumulative sum of minutes played within the date range
    player_x_values[player] = player_data.sum()
    
    # Y-axis: sum of minutes from all the games within the date range the player participated in (excluding NaN values)
    games_sum = []
    for idx in range(len(player_data)):
        valid_games = player_data.iloc[:idx+1].dropna()
        games_sum.append(valid_games.sum())
    
    player_y_values[player] = games_sum[-1]  # Taking the last value as it represents the most recent game within the date range

player_x_values, player_y_values


# Function to adjust overlapping annotations
def stack_and_avoid_overlap(x, y, names):
    coord_to_name = {}
    
    for i, (xi, yi) in enumerate(zip(x, y)):
        key = None
        
        # Check if this point is close to a previously processed point based on both criteria
        for (xj, yj) in coord_to_name:
            if abs(xi - xj) < 30 and abs(yi - yj) < 10:
                key = (xj, yj)
                break
        
        # If not found a close point, use its own coordinates
        if key is None:
            key = (xi, yi)
        
        if key in coord_to_name:
            coord_to_name[key].append(names[i])
        else:
            coord_to_name[key] = [names[i]]
    
    for (xi, yi), stacked_names in coord_to_name.items():
        y_offset = 3
        for name in stacked_names:
            plt.annotate(name, (xi, yi + y_offset), fontsize=9, ha='center', va='bottom')
            y_offset += 6

# Fill NaN values and ensure all columns are numeric
df_sample.fillna("", inplace=True)
for col in df_sample.columns:
    df_sample[col] = pd.to_numeric(df_sample[col], errors='coerce')

# Initialize the player_columns based on the DataFrame columns
player_columns = [col for col in df_sample.columns if col not in ["Opponent", "Team", "Date"]]

player_x_values_total = {}
player_y_values_filtered = {}

# For each player, calculate the required values
for player in player_columns:
    player_data_total = df_sample[player]
    player_data_filtered = df_filtered[player]
    
    # X-axis: cumulative sum of minutes played over entire dataset
    player_x_values_total[player] = player_data_total.sum()
    
    # Y-axis: cumulative sum of minutes played within the date range
    player_y_values_filtered[player] = player_data_filtered.sum()

# Plotting the graph
plt.figure(figsize=(12, 7))

# Shading the regions based on the conditions
plt.axhspan(0, 350, xmin=1000/max(player_x_values_total.values()), xmax=max(player_x_values_total.values())/max(player_x_values_total.values()), facecolor='#255075', alpha=0.5)
plt.axhspan(0, 150, xmin=0, xmax=400/max(player_x_values_total.values()), facecolor='#abcae4', alpha=0.5)
plt.axhspan(50, 250, xmin=400/max(player_x_values_total.values()), xmax=1000/max(player_x_values_total.values()), facecolor='#3d84bf', alpha=0.5)
plt.axhspan(0, 50, xmin=400/max(player_x_values_total.values()), xmax=1000/max(player_x_values_total.values()), facecolor='#0b1925', alpha=0.5)
plt.axhspan(250, 350, xmin=0, xmax=1000/max(player_x_values_total.values()), facecolor='#316a9a', alpha=0.5)
plt.axhspan(150, 250, xmin=0, xmax=400/max(player_x_values_total.values()), facecolor='#86b2d8', alpha=0.5)

# Annotate the regions
plt.text(1100, 335, "Key and Robust", fontsize=12, ha="left", fontweight='bold', color='white')
plt.text(115, 135, "Sparring or injured", fontsize=12, ha="left", fontweight='bold', color='white')
plt.text(115, 335, "Player of the moment", fontsize=12, ha="left", fontweight='bold', color='white')
plt.text(500, 235, "Core", fontsize=12, ha="left", fontweight='bold', color='white')
plt.text(115, 235, "Given Minutes", fontsize=12, ha="left", fontweight='bold', color='white')
plt.text(500, 35, "Less Concerned", fontsize=12, ha="left", fontweight='bold', color='white')

plt.scatter(list(player_x_values_total.values()), list(player_y_values_filtered.values()), color='black')

# Stack annotations and avoid overlaps
stack_and_avoid_overlap(list(player_x_values_total.values()), list(player_y_values_filtered.values()), list(player_x_values_total.keys()))

# Remove the top x-axis and the right y-axis
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

#plt.title("Total Minutes vs Minutes within Selected Date Range", fontsize=14, ha="center", fontweight='bold', color='black')
plt.xlabel("Total Minutes Played", fontsize=12, ha="center", fontweight='bold', color='black')
plt.ylabel("Minutes Played from last 3 weeks", fontsize=12, ha="center", fontweight='bold', color='black')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

#########################################################################################
data = pd.read_excel('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/squad/minute.xlsx', index_col=0)


# Step 1: Select data for Team == SFC
sfc_data = data[data['Team'] == 'SFC'].copy()

# Step 2: Replace "Nan" and np.nan with 0
sfc_data.replace("Nan", np.nan, inplace=True)
sfc_data.fillna(0, inplace=True)

# Convert player columns to numeric
player_columns = sfc_data.columns[3:]
sfc_data[player_columns] = sfc_data[player_columns].apply(pd.to_numeric, errors='coerce')

# Step 3: Find the maximum value for each row and create a new column 'maxtime'
sfc_data['maxtime'] = sfc_data[player_columns].max(axis=1)


# Step 4: Calculate the total minutes and max possible minutes

total_minutes_played = sfc_data[player_columns].sum()


total_max_minutes = sfc_data['maxtime'].sum()

# Calculate the % of total minutes played compared to the maximum possible minutes
player_percentage_total = (total_minutes_played / total_max_minutes) * 100

# Step 5: Plot the new data
# Set up the matplotlib figure
# Sort values for plotting
sorted_percentage_total = player_percentage_total.sort_values(ascending=False)


# Adjust the size of the percentage values and format
plt.figure(figsize=(12, 6))
#sns.set_theme(style="whitegrid")

# Draw a bar plot
bar_plot = sns.barplot(x=sorted_percentage_total.index, y=sorted_percentage_total.values, palette='viridis', edgecolor=".2")

# Customize the plot
plt.title('% Minutes jouées par joueur',fontsize=18,fontweight='bold', pad=25)
plt.xlabel('')
plt.ylabel('% Minutes jouées')

# Modify the x-axis labels to add "*" after Sawadogo and Camara
x_labels = [label + "*" if label in ["Camara", "Sawadogo","Omeragic"] else label for label in sorted_percentage_total.index]
bar_plot.set_xticklabels(x_labels, rotation=90)

plt.xticks(rotation=90)
plt.ylim(0, 100)  # Set y-axis limits from 0 to 100
plt.yticks(range(0, 101, 10))  # Set y-axis ticks with a range of 10

# Add the values on top of the bars with reduced font size and 1 decimal place
# For "Camara et Sawadogo", only the minutes are displayed, not the percentage.
for i, (player, percentage, minutes) in enumerate(zip(sorted_percentage_total.index, sorted_percentage_total.values, total_minutes_played[sorted_percentage_total.index].values)):
    if player in ["Camara", "Sawadogo","Omeragic"]:
        # Only show the minutes for Camara and Sawadogo
        bar_plot.text(i, percentage + 1, f"{minutes:.0f}m", ha='center', va='bottom', fontsize=5)
    else:
        # Show both percentage and minutes for other players
        bar_plot.text(i, percentage + 1, f"{percentage:.1f}% \n{minutes:.0f}m", ha='center', va='bottom', fontsize=5)

# Remove the top and right axis
sns.despine()

# Calculate the percentage of minutes played by under 21 players
under_21_players = ['Kaloga', 'Ouattara', 'Besson', 'Henchoz', 'Diba','Magnin']
under_21_minutes = total_minutes_played[under_21_players].sum()
total_min = total_max_minutes*11 #ici  il m faut modifier le coe en premnant les carton rouge 
under_21_percentage = (under_21_minutes / total_min) * 100 
# Add text for under 21 players' minutes
plt.text(25, 107, f"< 21 ans % minutes: {under_21_percentage:.1f}% ({under_21_minutes:.0f} min)", fontsize=8, ha='left', va='center', bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.2'))

# Calculate the percentage of minutes played by under 21 players
sfc_21_players = ['Kaloga', 'Ouattara', 'Besson', 'Henchoz','Magnin']
sfc_21_minutes = total_minutes_played[sfc_21_players].sum()
total_min = total_max_minutes*11
sfc_21_percentage = (sfc_21_minutes / total_min) * 100 
# Add text for under 21 players' minutes
plt.text(25, 102, f"< 21 ans % minutes SFC: {sfc_21_percentage:.1f}% ({sfc_21_minutes:.0f} min)", fontsize=8, ha='left', va='center', bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.2'))

# Calculate the percentage of minutes played by under 21 players
under_32_players = ['Rouiller', 'Douline', 'Stevanovic','Baron','Frick','Mall','Rodelin']
under_32_minutes = total_minutes_played[under_32_players].sum()
total_min = total_max_minutes*11
under_32_percentage = (under_32_minutes / total_min) * 100 
# Add text for under 21 players' minutes
plt.text(25, 97, f"> 30 ans % minutes: {under_32_percentage:.1f}% ({under_32_minutes:.0f} min)", fontsize=8, ha='left', va='center', bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.2'))

# Calculate the percentage of minutes played by under 21 players
under_28_players = ['Rouiller', 'Douline', 'Stevanovic','Baron','Frick','Mall','Rodelin','Ondoua','Crivelli']
under_28_minutes = total_minutes_played[under_28_players].sum()
total_min = total_max_minutes*11
under_28_percentage = (under_28_minutes / total_min) * 100 
# Add text for under 21 players' minutes
plt.text(25, 92, f"> 28 ans % minutes: {under_28_percentage:.1f}% ({under_28_minutes:.0f} min)", fontsize=8, ha='left', va='center', bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.2'))


plt.text(10, 104,"* Les joueurs en prêt sont exclus des calculs", fontsize=10, ha='left', va='center')

# Display the plot
plt.tight_layout()
plt.show()

#################################################################################################################################################

# Filter the data for the specified opponents
opponents = ["Romaa", "Roma", "Tiraspol", "Sheriff", "Prague"]
filtered_data = df_minutes_new[df_minutes_new["Opponent"].isin(opponents)]

# Summing up the minutes for each player
# Excluding non-player columns: week, Date, Team, and Opponent
player_minutes = filtered_data.drop(columns=["Date", "Team", "Opponent"]).apply(pd.to_numeric, errors='coerce').sum()

# Sorting the players by total minutes played
sorted_player_minutes = player_minutes.sort_values(ascending=False)

# Removing the specified players from the dataset
players_to_remove = ["Omeragic", "Sawadogo", "Camara"]
filtered_player_minutes = sorted_player_minutes.drop(players_to_remove)

# Recalculating the colors for each group after removing the players
new_first_group_end = 11
new_second_group_end = 18
new_colors = ['blue'] * min(new_first_group_end, len(filtered_player_minutes)) \
             + ['orange'] * min(new_second_group_end - new_first_group_end, max(len(filtered_player_minutes) - new_first_group_end, 0)) \
             + ['gray'] * max(len(filtered_player_minutes) - new_second_group_end, 0)

# Recreating the bar plot
plt.figure(figsize=(15, 8))


bars = plt.bar(filtered_player_minutes.index, filtered_player_minutes, color=new_colors)

# Adding the total minutes above each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom',fontsize=8)

# Setting up the x-axis with rank and player names
ranked_player_names = [f"{rank+1}. {player}" for rank, player in enumerate(filtered_player_minutes.index)]
plt.xticks(ticks=range(len(filtered_player_minutes)), labels=ranked_player_names, rotation=45)

# Setting y-axis ticks to increment by 50
plt.yticks(range(0, int(max(filtered_player_minutes) + 50), 50))

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Adding title and labels
plt.title('Total Minutes jouées en Europa League - (Hors Slavia vs SFC (4-0))')
plt.xlabel('Players (Rank)')
plt.ylabel('Total Minutes')
plt.xticks(rotation=90)
# Showing the plot
plt.show()

##################

# Filter the data for the team 'SFC'
sfc_data = df_minutes_new[df_minutes_new['Team'] == 'SFC']

# Calculate the number of games played
# Assuming each row represents a game
number_of_games_played = sfc_data.shape[0]

number_of_games_played

# Identify the player columns (columns after "Opponent")
player_columns = sfc_data.columns[sfc_data.columns.get_loc("Opponent") + 1:]

# Exclude the specified players
excluded_players = ['Sawadogo', 'Camara', 'Omeragic']

# Adjust the calculation to handle non-numeric values correctly and exclude specific players
player_game_percentages_adjusted = pd.DataFrame(columns=['Player', '% Games Played'])

for player in player_columns:
    if player not in excluded_players:
        # Convert non-numeric values to NaN, then to 0, and check if the player played at least 1 minute
        games_played = sfc_data[sfc_data[player].replace('', pd.NA).fillna(0).astype(float) > 0].shape[0]
        # Calculate the percentage of games played
        percent_of_games_played = (games_played / number_of_games_played) * 100
        # Append the result to the dataframe
        player_game_percentages_adjusted = player_game_percentages_adjusted.append({'Player': player, 
                                                                                    '% Games Played': percent_of_games_played}, 
                                                                                   ignore_index=True)

# Sort, round off, and render the table
player_game_percentages_sorted = player_game_percentages_adjusted.sort_values(by='% Games Played', ascending=False)
player_game_percentages_sorted['% Games Played'] = player_game_percentages_sorted['% Games Played'].round(1)




def render_mpl_table(data, col_width=3.0, row_height=0.5, font_size=10,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

render_mpl_table(player_game_percentages_sorted, header_columns=0, col_width=2.0)
plt.show()





