#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 18:46:05 2023

@author: matfeig
"""
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/event_match/23_24/slo_sfc_1.csv')

# Display the first few rows of the dataset
df.head()

# Filter the required columns
filtered_df = df[['minute', 'obv_total_net']]

# Group by 'minute' and calculate the sum for 'obv_total_net' to handle multiple entries per minute
grouped_df = filtered_df.groupby('minute').sum().reset_index()

# Calculate the cumulative sum for 'obv_total_net'
grouped_df['cumulative_obv_total_net'] = grouped_df['obv_total_net'].cumsum()

grouped_df.head()

# Identify the opponent's name
teams = df['team_name'].unique()
opponent_team = [team for team in teams if team != 'Servette'][0]  # Assuming there are only two teams in the dataset

# Using a close approximation to the color "grenat" using RGB values
grenat_color = (153/255, 0, 51/255)  # RGB representation

# Plotting
plt.figure(figsize=(14, 8))
bars = plt.bar(grouped_df['minute'], grouped_df['cumulative_obv_total_net'], color=grenat_color)

# Coloring bars below 0 with a different color
for bar in bars:
    if bar.get_height() < 0:
        bar.set_color('grey')

# Setting labels, title, and axis properties
plt.ylabel('Cumulative OBV Total Net')
plt.xlabel('Minute')
plt.title('Cumulative OBV Total Net per Minute')
plt.axhline(0, color='black',linewidth=0.5)  # Add a horizontal line at y=0 for clarity
plt.xticks(range(0, grouped_df['minute'].max() + 1, 5))  # Setting x-axis interval to 5 minutes
plt.ylim(-15, 15)  # Setting y-axis limits

# Removing top and right axis
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)


plt.text(0.07, 0.60, 'Servette', transform=plt.gca().transAxes, ha='right', va='top', color=grenat_color)
plt.text(0.07, 0.40, opponent_team, transform=plt.gca().transAxes, ha='right', va='bottom', color='grey')
plt.tight_layout()

plt.show()

#############################

# Splitting the data based on the team
servette_df = df[df['team_name'] == 'Servette']
opponent_df = df[df['team_name'] == opponent_team]

# Grouping by 'minute' and calculating the cumulative sum for each team
servette_grouped = servette_df.groupby('minute')['obv_total_net'].sum().cumsum().reset_index()
opponent_grouped = opponent_df.groupby('minute')['obv_total_net'].sum().cumsum().reset_index()

# Merging the two datasets on 'minute'
merged_df = servette_grouped.merge(opponent_grouped, on='minute', how='outer', suffixes=('_servette', '_opponent'))
merged_df = merged_df.sort_values(by='minute').fillna(method='ffill').fillna(0)  # Fill NaN values

merged_df.head()




# Adjusting the opponent's values based on the given conditions
merged_df['adjusted_opponent'] = merged_df['obv_total_net_opponent'].apply(lambda x: 0 if x < 0 else -x)  # Set values < 0 to 0 and invert all values

# Plotting with the adjusted values
plt.figure(figsize=(14, 8))

# Bars for Servette
bars_servette = plt.bar(merged_df['minute'], merged_df['adjusted_servette'], color=grenat_color)

# Bars for Opponent
bars_opponent = plt.bar(merged_df['minute'], merged_df['adjusted_opponent'], color='grey')

# Setting labels, title, and axis properties
plt.ylabel('Adjusted Cumulative OBV Total Net')
plt.xlabel('Minute')
plt.title('Adjusted Cumulative OBV Total Net per Minute for Each Team')
plt.axhline(0, color='black',linewidth=0.5)  # Add a horizontal line at y=0 for clarity
plt.xticks(range(0, merged_df['minute'].max() + 1, 5))  # Setting x-axis interval to 5 minutes
plt.ylim(-15, 15)  # Setting y-axis limits

# Removing top and right axis
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Labels for teams
plt.text(0.95, 0.95, 'Servette', transform=plt.gca().transAxes, ha='right', va='top', color=grenat_color)
plt.text(0.95, 0.05, opponent_team, transform=plt.gca().transAxes, ha='right', va='bottom', color='grey')

plt.tight_layout()
plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Load the data again
df = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/event_match/23_24/slo_sfc_1.csv')


# Splitting the data based on the team
servette_df = df[df['team_name'] == 'Servette']
opponent_df = df[df['team_name'] != 'Servette']

# Identify the opponent's name
opponent_team = opponent_df['team_name'].iloc[0]

# Grouping by 'minute' and calculating the cumulative sum for each team
servette_grouped = servette_df.groupby('minute')['obv_total_net'].sum().cumsum().reset_index()
opponent_grouped = opponent_df.groupby('minute')['obv_total_net'].sum().cumsum().reset_index()

# Merging the two datasets on 'minute'
merged_df = servette_grouped.merge(opponent_grouped, on='minute', how='outer', suffixes=('_servette', '_opponent'))
merged_df = merged_df.sort_values(by='minute').fillna(method='ffill').fillna(0)  # Fill NaN values

# Adjusting the values based on the given conditions
merged_df['adjusted_servette'] = merged_df['obv_total_net_servette'].apply(lambda x: x if x >= 0 else 0)
merged_df['adjusted_opponent'] = merged_df['obv_total_net_opponent'].apply(lambda x: 0 if x < 0 else -x)  # Set values < 0 to 0 and invert all values

# Plotting with the adjusted values
plt.figure(figsize=(14, 8))

# Bars for Servette
bars_servette = plt.bar(merged_df['minute'], merged_df['adjusted_servette'], color=(153/255, 0, 51/255))  # RGB for grenat

# Bars for Opponent
bars_opponent = plt.bar(merged_df['minute'], merged_df['adjusted_opponent'], color='grey')

# Setting labels, title, and axis properties
plt.ylabel('Adjusted Cumulative OBV Total Net')
plt.xlabel('Minute')
plt.title('Adjusted Cumulative OBV Total Net per Minute for Each Team')
plt.axhline(0, color='black',linewidth=0.5)  # Add a horizontal line at y=0 for clarity
plt.xticks(range(0, merged_df['minute'].max() + 1, 5))  # Setting x-axis interval to 5 minutes
plt.ylim(-15, 15)  # Setting y-axis limits

# Removing top and right axis
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Labels for teams
plt.text(0.95, 0.95, 'Servette', transform=plt.gca().transAxes, ha='right', va='top', color=(153/255, 0, 51/255))
plt.text(0.95, 0.05, opponent_team, transform=plt.gca().transAxes, ha='right', va='bottom', color='grey')

plt.tight_layout()
plt.show()




import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('/mnt/data/sfc_stg_1.csv')

# Splitting the data based on the team
servette_df = df[df['team_name'] == 'Servette']
opponent_df = df[df['team_name'] != 'Servette']

# Identify the opponent's name
opponent_team = opponent_df['team_name'].iloc[0]

# Grouping by 'minute' and calculating the cumulative sum for each team
servette_grouped = servette_df.groupby('minute')['obv_total_net'].sum().cumsum().reset_index()
opponent_grouped = opponent_df.groupby('minute')['obv_total_net'].sum().cumsum().reset_index()

# Merging the two datasets on 'minute'
merged_df = servette_grouped.merge(opponent_grouped, on='minute', how='outer', suffixes=('_servette', '_opponent'))
merged_df = merged_df.sort_values(by='minute').fillna(method='ffill').fillna(0)  # Fill NaN values

# Adjusting the values based on the given conditions
merged_df['adjusted_servette'] = merged_df['obv_total_net_servette'].apply(lambda x: x if x >= 0 else 0)
merged_df['adjusted_opponent'] = merged_df['obv_total_net_opponent'].apply(lambda x: 0 if x < 0 else -x)  # Set values < 0 to 0 and invert all values

# Plotting with the adjusted values
plt.figure(figsize=(14, 8))

# Bars for Servette
bars_servette = plt.bar(merged_df['minute'], merged_df['adjusted_servette'], color=(153/255, 0, 51/255))  # RGB for grenat

# Bars for Opponent
bars_opponent = plt.bar(merged_df['minute'], merged_df['adjusted_opponent'], color='grey')

# Setting labels, title, and axis properties
plt.ylabel('Adjusted Cumulative OBV Total Net')
plt.xlabel('Minute')
plt.title('Adjusted Cumulative OBV Total Net per Minute for Each Team')
plt.axhline(0, color='black',linewidth=0.5)  # Add a horizontal line at y=0 for clarity
plt.xticks(range(0, merged_df['minute'].max() + 1, 5))  # Setting x-axis interval to 5 minutes
plt.ylim(-15, 15)  # Setting y-axis limits

# Removing top and right axis
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Labels for teams
plt.text(0.95, 0.95, 'Servette', transform=plt.gca().transAxes, ha='right', va='top', color=(153/255, 0, 51/255))
plt.text(0.95, 0.05, opponent_team, transform=plt.gca().transAxes, ha='right', va='bottom', color='grey')

plt.tight_layout()
plt.show()

















