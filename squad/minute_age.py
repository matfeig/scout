#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:54:30 2023

@author: matfeig
"""

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_excel("/Users/matfeig/Library/CloudStorage/OneDrive-GENEVESPORTSA/Contingent/sfc_contingent.xlsx")

# Calculate the current year
current_year = datetime.now().year

# Calculate age based on "Date naissance"
df['Age'] = current_year - pd.to_datetime(df['Date naissance']).dt.year

# Display the updated dataframe with the new "Age" column
df_grouped =df[['Numero','Nom',"Equipe","Type", 'Date naissance', 'Age','Minutes']]
df_grouped = df_grouped[df_grouped['Equipe'] == 'Pro']
df_grouped = df_grouped[~df_grouped['Type'].isin(['out loan', 'Under21', 'Transfer'])]

# Creating the 'Min_adjus' column
df_grouped['Min_adjus'] = df_grouped['Minutes'] + 15

# Sorting the dataframe by 'Minutes'
df_grouped.sort_values(by='Min_adjus', inplace=True)

# Iterating through rows to ensure no duplicate values in 'Min_adjus' by comparing with all previous rows
for idx in range(1, len(df_grouped)):
    while df_grouped.iloc[idx]['Min_adjus'] in df_grouped['Min_adjus'].iloc[:idx].values:
        df_grouped.iloc[idx, df_grouped.columns.get_loc('Min_adjus')] += 25

# Checking if there are any duplicate 'Min_adjus' values after the adjustment
duplicate_min_adjus = df_grouped[df_grouped.duplicated(subset='Min_adjus', keep=False)]

# # Set the color palette to be used for the histogram
# colors = plt.cm.Greys(np.linspace(0.1, 5, len(df)))
# df_grouped = df_grouped.sort_values(by='Age')

# Generating colors for each individual player based on their minutes
normalized_minutes_sorted = (df_grouped['Minutes'] - df_grouped['Minutes'].min()) / (df_grouped['Minutes'].max() - df_grouped['Minutes'].min())
colors = plt.cm.Blues(normalized_minutes_sorted)

plt.figure(figsize=(16, 9))
bars = plt.bar(df_grouped['Age'], df_grouped['Minutes'], color=colors)

# Setting the "Numero" label at positions adjusted by 'Min_adjus'
for idx, bar in enumerate(bars):
    adjusted_yval = df_grouped['Min_adjus'].iloc[idx]
    label_text = "n°" + str(int(df_grouped['Numero'].iloc[idx]))
    plt.text(bar.get_x() + bar.get_width()/2, adjusted_yval, 
             label_text, 
             ha='center', va='bottom', color='black', fontweight='bold', fontsize=8)


# Calculate percentage of total minutes for each age range and annotate the plot
ranges = [(16, 19), (20, 23), (24, 29), (30, 37)]
for r in ranges:
    total_minutes = df_grouped['Minutes'].sum()
    range_minutes = df_grouped[(df_grouped['Age'] >= r[0]) & (df_grouped['Age'] <= r[1])]['Minutes'].sum()
    percentage = (range_minutes / total_minutes) * 100
    plt.text(sum(r)/2, 1.10 * max(df_grouped['Minutes']), 
             f"{percentage:.2f}%", 
             ha='center', color='black', fontweight='bold', fontsize=12)
    
# Annotations below the vertical lines
plt.text(17, max(df_grouped['Minutes']) * 1.2, 'Potential',fontweight='bold', fontsize=13, rotation=0, color='black')
plt.text(21, max(df_grouped['Minutes']) * 1.2, 'Pre-peak',fontweight='bold', fontsize=13, rotation=0, color='black')
plt.text(26, max(df_grouped['Minutes']) * 1.2, 'Peak',fontweight='bold', fontsize=13, rotation=0, color='black')
plt.text(33, max(df_grouped['Minutes']) * 1.2, 'Experience',fontweight='bold', fontsize=13, rotation=0, color='black')

# Additional annotations below the vertical lines
plt.text(17.5, 1.15 * max(df_grouped['Minutes']), '0-20% temps de jeu\n10% du budget', color='black', ha='center')
plt.text(21.5, 1.15 * max(df_grouped['Minutes']), '20-50% temps de jeu\n20% du budget', color='black', ha='center')
plt.text(26.5, 1.15 * max(df_grouped['Minutes']), '>50% temps de jeu\n50% du budget', color='black', ha='center')
plt.text(33.7, 1.15 * max(df_grouped['Minutes']), '0-20% temps de jeu\n20% du budget', color='black', ha='center')

# Additional plot enhancements
plt.axvline(x=19.5, color='grey', linestyle='--')
plt.axvline(x=23.5, color='grey', linestyle='--')
plt.axvline(x=29.5, color='grey', linestyle='--')
plt.xlim(16, 37)
plt.xticks(np.arange(16, 38, 1))
plt.ylim(0, 2300)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title("Analyse Contingent | Age", fontweight='bold', fontsize=20, pad=20)
plt.xlabel("Age",fontweight='bold', fontsize=14)
plt.ylabel("Minutes",fontweight='bold', fontsize=14)
plt.tight_layout()
plt.show()
