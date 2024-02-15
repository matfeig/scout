#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 17:59:29 2023

@author: matfeig
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = '/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_season/23_24/matchday_10.csv'
data = pd.read_csv(file_path)

name_mapping = {
    "Dereck Germano Kutesa": "Dereck Kutesa",
    "Jeremy Bruno Guillemenot": "Jeremy Guillemenot",
    "Chris Vianney Bedia": "Chris Bedia"
}

# Applying the changes
data['player_name'].replace(name_mapping, inplace=True)

# Verifying the changes
data[data['player_name'].isin(name_mapping.values())][['player_name']]

primary_positions = data['primary_position'].unique()
primary_positions_list = primary_positions.tolist()
primary_positions_list

offensive_indices = [0, 1, 5, 13,15, 17,2,14]
midfielder_indices = [2, 6, 14, 18, 19]
defense_indices = [3, 4, 8, 9, 10, 11, 12, 16, 20]

# Extracting positions
offensive_positions = [primary_positions_list[i] for i in offensive_indices]
midfielder_positions = [primary_positions_list[i] for i in midfielder_indices]
defense_positions = [primary_positions_list[i] for i in defense_indices]

# Creating a new DataFrame with players in offensive positions and with more than 200 minutes played
data = data[(data['primary_position'].isin(offensive_positions)) & (data['player_season_minutes'] > 300)]


#####################################################################################################

# Define a function to create the scatter plots
def create_scatter_plot(x, y, title, xlabel, ylabel, data, quantile=0.90):
    plt.figure(figsize=(16, 9))
    sns.set_style("whitegrid")
    
    # Plotting
    scatter = sns.scatterplot(
        x=x,
        y=y,
        hue=x,  # Color map based on x
        palette='viridis',
        data=data,
        s=50
    )
   
    for i in range(data.shape[0]):
        if data.iloc[i]['team_name'] == 'Servette':
            plt.text(
                x=data.iloc[i][x],
                y=data.iloc[i][y],
                s=data.iloc[i]['player_name'],
                fontdict=dict(color='black', size=10),
                bbox=dict(facecolor='yellow', alpha=0.5)
            )
    
    
    # Labeling players in top quantile% for both x and y
    top_x = data[x].quantile(quantile)
    top_y = data[y].quantile(quantile)

    top_players = data[(data[x] >= top_x) | (data[y] >= top_y)]

    for i in range(top_players.shape[0]):
        plt.text(
            x=top_players.iloc[i][x],
            y=top_players.iloc[i][y],
            s=top_players.iloc[i]['player_name'],
            fontdict=dict(color='black', size=10),
            bbox=dict(facecolor='white', alpha=0.5)
        )
        
    # Titles and labels
    plt.title(title, fontsize=15)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    plt.legend(title=xlabel, title_fontsize='13', fontsize='11', loc='upper left')
    sns.despine(right=True, top=True)

    plt.show()
    

# Creating plots with updated variables
create_scatter_plot('player_season_dribbles_90', 'player_season_dispossessions_90', 'Joueurs Offensifs - Super League - Dribbling vs Technique', 'Dribbles', 'Perte de balle', data)
create_scatter_plot('player_season_np_xg_90', 'player_season_npga_90', 'Joueurs Offensifs - Super League - Efficacité', 'NP xG/90', 'Buts', data)
create_scatter_plot('player_season_obv_dribble_carry_90', 'player_season_obv_pass_90', 'Joueurs Offensifs - Super League - Progresseur vs Passeur', 'Menace Percussion', 'Menance Passes', data)
create_scatter_plot('player_season_aerial_wins_90', 'player_season_padj_pressures_90', 'Joueurs Offensifs - Super League - Fighter', 'Duels Gagnés', 'Pressing sur porteur', data)
create_scatter_plot('player_season_np_psxg_90', 'player_season_np_xg_per_shot', 'Joueurs Offensifs - Super League - Tir et Positionnement', 'Qaulité de Tir', 'Qualité Positionnement', data)
