#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:03:45 2023

@author: matfeig
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.colors import Color
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import six
import numpy as np

#Variables

df = pd.read_excel("/Users/matfeig/Library/CloudStorage/OneDrive-GENEVESPORTSA/Contingent/sfc_contingent.xlsx")

####Clean Data####
##################

# Standardize the date format to 'YYYY-MM-DD'
df['Date naissance'] = pd.to_datetime(df['Date naissance']).dt.date
# Calculate the age of each individual
current_year = datetime.now().year
df['Age'] = current_year - df['Date naissance'].apply(lambda x: x.year)
# Display the updated dataframe with the new age column
df[['Nom', 'Prenom', 'Date naissance', 'Age']].head()


####Fitler ###1###
##############
# Filtering the dataframe for 'Potentiel' = 3
filtered_df = df[df['Potentiel'] == 3]
filtered_df = filtered_df[filtered_df['Equipe'] != "Pro"]
filtered_df['Equipe'] = filtered_df['Equipe'].astype(str)
filtered_df['Profil'] = filtered_df['Profil'].astype(str)

# Grouping and sorting process
grouped_df = filtered_df.groupby(['Equipe', 'Nom']).size().reset_index(name='Count')
sorted_df = grouped_df.sort_values(by='Equipe')

# Generate a color map for teams and profiles
unique_teams = sorted_df['Equipe'].unique()
unique_profiles = filtered_df['Profil'].unique()

team_color_map = {team: plt.cm.tab20(i) for i, team in enumerate(unique_teams)}
profile_color_map = {profile: plt.cm.Paired(i) for i, profile in enumerate(unique_profiles)}

# Preparing data for the outer and inner pie charts
names = sorted_df['Nom']
teams = sorted_df['Equipe']
profiles = []
labels = []
colors_for_names = []
colors_for_profiles = []

for _, row in sorted_df.iterrows():
    name = row['Nom']
    team = row['Equipe']
    colors_for_names.append(team_color_map[team])
    player_profiles = filtered_df[filtered_df['Nom'] == name]['Profil'].unique()
    for profile in player_profiles:
        profiles.append(1)  # Assuming each player has a single unique profile
        labels.append(profile)
        colors_for_profiles.append(profile_color_map[profile])

# Creating the figure
plt.figure(figsize=(15, 10))
plt.title('Selection des joueurs à potentiel - Q4 2023', fontsize=16)

# Outer Pie Chart (Names with team colors)
plt.pie(sorted_df['Count'], labels=names, radius=1, colors=colors_for_names, 
        wedgeprops=dict(width=0.3, edgecolor='w'))

# Inner Pie Chart (Profiles with distinct colors)
plt.pie(profiles, radius=0.7, colors=colors_for_profiles, 
        wedgeprops=dict(width=0.3, edgecolor='w'))

# Adding legends for teams and profiles
team_legend = plt.legend(title='Equipe (Team)', handles=[plt.Line2D([0], [0], marker='o', color='w', label=team, markersize=10, markerfacecolor=color) for team, color in team_color_map.items()], bbox_to_anchor=(1.15, 1), loc=2)
plt.gca().add_artist(team_legend)
plt.legend(title='Profil', handles=[plt.Line2D([0], [0], marker='o', color='w', label=profile, markersize=10, markerfacecolor=color) for profile, color in profile_color_map.items()], bbox_to_anchor=(1.15, 0.5), loc=2)

# Displaying the chart
plt.show()

# Filtering players with potential == 3
players_potential_3 = df[df['Potentiel'] == 3]

# Selecting the required columns
required_columns = ['Equipe', 'Nom', 'Prenom', 'Date naissance', 'Prim_pos', 'Profil']
players_data = players_potential_3[required_columns]

# Function to render dataframe as a table and save as an image
def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
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
            cell.set_facecolor(row_colors[k[0]%len(row_colors)])
    
    plt.savefig('/Users/matfeig/Desktop/players_potential_3.png')

# Render and save the table
render_mpl_table(players_data, header_columns=0, col_width=2.0)
'/Users/matfeig/Desktop/players_potential_3.png'












