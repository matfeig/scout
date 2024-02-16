#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 21:29:51 2024

@author: matfeig
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
from matplotlib.lines import Line2D
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load the data from the Excel file
file_path = "/Users/matfeig/Library/CloudStorage/OneDrive-GENEVESPORTSA/Contingent/sfc_contingent.xlsx"
data = pd.read_excel(file_path)

# Filtering the data for team "Pro" and Type not equal to "Transfer" or "out loan"
sfc_data = data[(data['Equipe'] == 'Pro') & ~(data['Type'].isin(['Transfer', 'out loan']))]

# Assuming 'Date naissance' is the column for birthdates
sfc_data['Date naissance'] = pd.to_datetime(sfc_data['Date naissance'])

# Calculate current date
current_date = datetime.now()

# Calculate age and add as a new column
sfc_data['Age'] = sfc_data['Date naissance'].apply(lambda x: current_date.year - x.year - ((current_date.month, current_date.day) < (x.month, x.day)))

# Display the first few rows of the data with the new 'Age' column
sfc_data.head()

# Calculating the end year of the contract
sfc_data['End Contract'] = sfc_data['Debut Contrat'] + sfc_data['Durée Contrat']

# Group by 'Age' and sum 'Min SFC'
df_age_sum = sfc_data.groupby('Age')['Min SFC'].sum().reset_index()

sfc_data['age_begin'] =sfc_data.apply(lambda row: row['Age'] - (2023 - row['Debut Contrat']) ,axis=1)
sfc_data['age_end'] = sfc_data.apply(lambda row: row['Age'] - (2023 - row['End Contract']) ,axis=1)


#################################################################################################
# Assuming sfc_data is your DataFrame and it's clean

# Preparing the data
X = sfc_data[['Age']]  # Predictor variable
y = sfc_data['Min SFC']  # Response variable

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Creating the linear regression model
model = LinearRegression()

# Training the model
model.fit(X_train, y_train)

# Predicting the test set results
y_pred = model.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Now the model can be used to predict minutes played based on age
# Example: predicting for a player of age 25
predicted_minutes = model.predict(np.array([[25]]))
print(f'Predicted Minutes for Age 25: {predicted_minutes[0]}')

####################################################################################

plt.figure(figsize=(10, 6))

# Plotting scatters with color based on the condition
for i in range(len(sfc_data)):
    color = 'green' if sfc_data['End Contract'].iloc[i] == 2025 else 'red' if sfc_data['End Contract'].iloc[i] == 2024 else 'blue'
    plt.scatter(sfc_data['Age'].iloc[i], sfc_data['Min SFC'].iloc[i], color=color)
    plt.text(sfc_data['Age'].iloc[i], sfc_data['Min SFC'].iloc[i] + 20, sfc_data['Nom'].iloc[i], 
             fontsize=8, ha='center', va='bottom')

# Adding labels slightly higher above each scatter point
for i in range(len(sfc_data)):
    plt.text(sfc_data['Age'].iloc[i], sfc_data['Min SFC'].iloc[i] + 20, sfc_data['Nom'].iloc[i], 
             fontsize=8, ha='center', va='bottom')
    

plt.xlabel('Age')
plt.ylabel('Minutes de jeu')
plt.title('Minutes de jeu vs Age')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid(True, linestyle='--')

# Adjusting x-axis range
plt.xticks(range(min(sfc_data['Age']), max(sfc_data['Age']) + 1, 1))

plt.scatter([], [], color='red', label='2024')
plt.scatter([], [], color='green', label='2025')

# Generate a range of ages from min to max
age_range = np.linspace(sfc_data['Age'].min(), sfc_data['Age'].max(), 100).reshape(-1, 1)

# Predict the minutes for this range of ages
predicted_minutes = model.predict(age_range)

#Plot the regression line
plt.plot(age_range, predicted_minutes, color='grey', label='Predicted Minutes', linewidth=0.5)

# Add the legend to the plot
plt.legend(title='End Contract')

plt.show()

#########################################################################


plt.figure(figsize=(16, 9))

# Create a color map based on the size of the bars
colors = plt.cm.Blues(df_age_sum['Min SFC'] / df_age_sum['Min SFC'].max())
bars = plt.bar(df_age_sum['Age'], df_age_sum['Min SFC'], color=colors)

# Calculate percentage of total Min SFC for each age range and annotate the plot
ranges = [(16, 19), (20, 23), (24, 29), (30, 37)]
for r in ranges:
    total_minutes = sfc_data['Min SFC'].sum()
    range_minutes = sfc_data[(sfc_data['Age'] >= r[0]) & (sfc_data['Age'] <= r[1])]['Min SFC'].sum()
    percentage = (range_minutes / total_minutes) * 100
    plt.text(sum(r)/2, 2.4 * max(sfc_data['Min SFC']),f"{percentage:.2f}%", ha='center', color='darkblue', fontweight='bold', fontsize=16)
    
# Annotations below the vertical lines
plt.text(17, max(sfc_data['Min SFC']) * 2.75, 'Potential',fontweight='bold', fontsize=13, rotation=0, color='black')
plt.text(21, max(sfc_data['Min SFC']) * 2.75, 'Pre-peak',fontweight='bold', fontsize=13, rotation=0, color='black')
plt.text(26, max(sfc_data['Min SFC']) * 2.75, 'Peak',fontweight='bold', fontsize=13, rotation=0, color='black')
plt.text(33, max(sfc_data['Min SFC']) * 2.75, 'Experience',fontweight='bold', fontsize=13, rotation=0, color='black')

# Additional annotations below the vertical lines
plt.text(17.8, 2.6 * max(sfc_data['Min SFC']), '0-20% temps de jeu\n10% du budget', color='black', ha='center')
plt.text(21.5, 2.6 * max(sfc_data['Min SFC']), '20-50% temps de jeu\n20% du budget', color='black', ha='center')
plt.text(26.5, 2.6 * max(sfc_data['Min SFC']), '>50% temps de jeu\n50% du budget', color='black', ha='center')
plt.text(33.7, 2.6 * max(sfc_data['Min SFC']), '0-20% temps de jeu\n20% du budget', color='black', ha='center')

# Adding labels and title
plt.title("Répartition des minutes par catégorie", fontweight='bold', fontsize=18, pad=40)
plt.xlabel("Age", fontweight='bold', fontsize=14)
plt.ylabel("Miinutes de jeu", fontweight='bold', fontsize=14)

# Setting the x-axis and y-axis limits
plt.xticks(np.arange(df_age_sum['Age'].min(), df_age_sum['Age'].max() + 1, 1))
plt.xlim(df_age_sum['Age'].min() - 2, df_age_sum['Age'].max() + 2)
plt.ylim(0, df_age_sum['Min SFC'].max() + 2000)

# Additional plot enhancements
plt.axvline(x=19.5, color='grey', linestyle='--')
plt.axvline(x=23.5, color='grey', linestyle='--')
plt.axvline(x=29.5, color='grey', linestyle='--')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
plt.show()


##########################################################################

# Calculate the sum of the 'Value' column
total_value = sfc_data['Value'].sum()/1000000


plt.figure(figsize=(10, 6))

# Plotting scatters with color based on the condition
for i in range(len(sfc_data)):
    color = 'green' if sfc_data['End Contract'].iloc[i] == 2025 else 'red' if sfc_data['End Contract'].iloc[i] == 2024 else 'blue'
    plt.scatter(sfc_data['Age'].iloc[i], sfc_data['Value'].iloc[i], color=color)
   
# Adding labels slightly higher above each scatter point
for i in range(len(sfc_data)):
    plt.text(sfc_data['Age'].iloc[i], sfc_data['Value'].iloc[i] +9000, sfc_data['Nom'].iloc[i], 
             fontsize=8, ha='center', va='bottom')

plt.xlabel('Age')
plt.ylabel('Value')
plt.title('Valeur marchande vs Age')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.grid(True, linestyle='--')

# Adjusting x-axis range
plt.xticks(range(min(sfc_data['Age']), max(sfc_data['Age']) + 1, 1))

plt.scatter([], [], color='red', label='2024')
plt.scatter([], [], color='green', label='2025')

plt.text(0.05, 0.90, f'Total Value: {total_value} M', transform=plt.gca().transAxes, 
         fontsize=12, verticalalignment='top',bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

# Generate a range of ages from min to max
age_range = np.linspace(sfc_data['Age'].min(), sfc_data['Age'].max(), 100).reshape(-1, 1)

# Add the legend to the plot
plt.legend(title='End Contract')

plt.show()


###################################################################################

# Preparing the data
x = sfc_data[['Nom', 'Age', 'age_begin', 'age_end']].copy()
x = x.sort_values('Age').copy()

# Creating the figure
fig = go.Figure()

# Adding traces
# Age at start of contract
fig.add_trace(
    go.Scatter(mode='markers', x=x['age_begin'], y=x['Nom'], name='Age at start of contract',
               marker=dict(symbol='line-ns', color='rgba(135, 206, 250, 0.5)', size=10,
                           line=dict(color='MediumPurple', width=2))))

# Age at end of contract
fig.add_trace(
    go.Scatter(mode='markers', x=x['age_end'], y=x['Nom'], name='Age at end of contract',
               marker=dict(symbol='line-ns', color='rgba(135, 206, 250, 0.5)', size=10,
                           line=dict(color='red', width=3))))

# Lines between start and end of contract
for i in range(len(x)):
    selected = x.iloc[i]
    y_ = selected['Nom']
    x_0 = selected['age_begin']
    x_1 = selected['age_end']
    fig.add_shape(type="line", x0=x_0, y0=y_, x1=x_1, y1=y_, line_width=2, line_color="black")

# Current age
fig.add_trace(
    go.Scatter(mode='markers', x=x['Age'], y=x['Nom'], name='Current age',
               marker=dict(color='rgba(135, 206, 250, 0.5)', size=10,
                           line=dict(color='magenta', width=4))))

# Adding colored age brackets
fig.add_shape(type='rect', x0=15, x1=21, y0=-2, y1=28, fillcolor='lightblue', opacity=0.2)
fig.add_shape(type='rect', x0=21, x1=25, y0=-2, y1=28, fillcolor='lightyellow', opacity=0.2)
fig.add_shape(type='rect', x0=25, x1=29, y0=-2, y1=28, fillcolor='lightpink', opacity=0.2)
fig.add_shape(type='rect', x0=29, x1=40, y0=-2, y1=28, fillcolor='mediumvioletred', opacity=0.2)

# Update layout
fig.update_layout(template="plotly", title="Contract Ages and Current Age of Players", height=1200)

fig.write_html("/Users/matfeig/Desktop/plot.html")
# Show the figure
fig.show()


##################################################################################

# Sorting the players by 'Min SFC' in descending order and selecting the top 15 players
top_15_players = sfc_data.sort_values(by='Min SFC', ascending=False).head(15)

# Calculating the total minutes played by these top 15 players
total_minutes_top_15 = top_15_players['Min SFC'].sum()

# Calculating the total minutes played by all players in the filtered data
total_minutes_all_players = sfc_data['Min SFC'].sum()

# Computing the percentage of minutes played by the top 15 players
percentage_top_15 = (total_minutes_top_15 / total_minutes_all_players) * 100 if total_minutes_all_players else 0

percentage_top_15













