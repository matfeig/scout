#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 11:48:52 2023

@author: matfeig
"""
from statsbombpy import sb
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure, show, output_notebook
from bokeh.layouts import column
from bokeh.models import HoverTool
import os
import zipfile
import matplotlib.pyplot as plt

# set up credentials for StatsBomb API access
user="m.feigean@servettefc.ch" #replace between the quotation marks with the email address that you use to login to StatsBomb IQ
password="QzG3Kdlu" #replace between the quotation marks with the password that you use to login to StatsBomb IQ

# team="Servette" #team name, as it appears in IQ
# window=5 #rolling average window
# team_color1="#870E26"
# team_color2="black"

# # List of competition and season combinations
# combinations = [(80, 281), (35, 281)]
# all_matches = pd.DataFrame()


team = "Servette FC M-21"
window=5 #rolling average window
team_color1="#870E26"
team_color2="black"

# List of competition and season combinations
combinations = [(1525,281)]
all_matches = pd.DataFrame()

file_path="/Users/matfeig/Desktop/" 


# Loop through the combinations to fetch matches
for comp, season in combinations:
    matches = sb.matches(competition_id=comp, season_id=season, creds={"user": user, "passwd": password})
    
    # Print number of matches retrieved for debugging
    print(f"Retrieved {len(matches)} matches for competition {comp} and season {season}.")
    
    matches = matches[((matches['home_team'] == team) | (matches['home_team'] == teamyouth)) | 
                      ((matches['away_team'] == team) | (matches['away_team'] == teamyouth))]
    
    
    # Print number of matches for "Servette" for debugging
    print(f"Found {len(matches)} matches for 'Servette' in competition {comp} and season {season}.")
    
    matches = matches.sort_values(by=['match_date'])
    matches = matches[matches["match_status"] == "available"]
    
    # Print number of available matches for "Servette" for debugging
    print(f"Found {len(matches)} available matches for 'Servette' in competition {comp} and season {season}.")
    
    # Append to the all_matches DataFrame
    #all_matchs = matches.sort_values(by=['match_date'])
    all_matches = pd.concat([all_matches, matches])
  
all_matches = all_matches.sort_values(by=['match_date'])
list_matches = all_matches.match_id.tolist()


data = []
for n in list_matches:
      match_events=sb.player_match_stats(match_id=n, creds={"user": user, "passwd": password})
      teams=list(match_events.team_name.unique())
      match_events["opponent"]=np.where(match_events["team_name"]==team,teams[1],teams[0])
      data.append(match_events)
data=pd.concat(data)
data=data.reset_index(drop=True)

temp_df=data.drop_duplicates(subset=['match_id'])
temp_df.index.name = 'game_week'
temp_df=temp_df.reset_index()
temp_df=temp_df[["match_id","game_week"]]

data=pd.merge(data,temp_df, how="left",on=["match_id"])
df = data

########## Normalise the data ##################

# List of columns to exclude from normalization
excluded_columns = ['match_id', 'team_id', 'team_name', 'player_id', 'player_name', 'player_match_minutes','opponent', 'game_week']

# Identify numeric columns (excluding the ones in excluded_columns)
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
columns_to_normalize = [col for col in numeric_columns if col not in excluded_columns]

# Normalize columns
for col in columns_to_normalize:
    data[col] = ((data[col] - data[col].min()) / (data[col].max() - data[col].min())) * 100

# Display the normalized dataset
data.head()

data.to_csv('file_name.csv')

##################################

positive_columns = [
    'player_match_np_xg', 'player_match_op_xa', 'player_match_possession',
    'player_match_successful_aerials', 'player_match_forward_passes',
    'player_match_aggressive_actions', 'player_match_xgbuildup',
    'player_match_pressures', 'player_match_obv_pass', 'player_match_obv_shot',
    'player_match_obv_defensive_action', 'player_match_obv_dribble_carry'
]

# List of columns with negative influence
negative_columns = ['player_match_dispossessions', 'player_match_turnovers']

# Calculate the score for each player by match_id
data['score'] = data[positive_columns].sum(axis=1) - data[negative_columns].sum(axis=1)

# Filter out only players from 'Servette' or 'Servette FC M-21'
filtered_data = data[data['team_name'].isin(['Servette', 'Servette FC M-21'])]

# Display the first few rows of the data with scores
filtered_data[['player_name', 'match_id', 'score']].head()


# List of unique players from 'Servette' or 'Servette FC M-21'
unique_players = filtered_data['player_name'].unique()


# Using matplotlib for plotting individual graphs for the first few players
num_players_to_plot = 5

fig, axes = plt.subplots(num_players_to_plot, 1, figsize=(15, 5 * num_players_to_plot))

for ax, player in zip(axes, unique_players[:num_players_to_plot]):
    player_data = filtered_data[filtered_data['player_name'] == player]
    ax.plot(player_data['opponent'], player_data['score'], marker='o', label=player)
    ax.set_xlabel('Opponent')
    ax.set_ylabel('Score')
    ax.set_title(f'Score over Opponents for {player}')
    ax.grid(True)
    ax.legend()
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
