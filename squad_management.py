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

# Load the data from the Excel file
file_path = "/Users/matfeig/Library/CloudStorage/OneDrive-GENEVESPORTSA/Contingent/sfc_contingent.xlsx"
data = pd.read_excel(file_path)


# Filtering the data for team "Pro" and Type not equal to "Transfer" or "out loan"
sfc_data = data[(data['Equipe'] == 'Pro') & ~(data['Type'].isin(['Transfer', 'out loan']))]



## Add Age ##

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

##########################################################################

plt.figure(figsize=(10, 6))

# Plotting scatters with color based on the condition
for i in range(len(sfc_data)):
    color = 'green' if sfc_data['End Contract'].iloc[i] == 2025 else 'red' if sfc_data['End Contract'].iloc[i] == 2024 else 'blue'
    plt.scatter(sfc_data['Age'].iloc[i], sfc_data['Value'].iloc[i], color=color)
    plt.text(sfc_data['Age'].iloc[i], sfc_data['Value'].iloc[i] + 20, sfc_data['Nom'].iloc[i], 
             fontsize=8, ha='center', va='bottom')

# Adding labels slightly higher above each scatter point
for i in range(len(sfc_data)):
    plt.text(sfc_data['Age'].iloc[i], sfc_data['Value'].iloc[i] + 20, sfc_data['Nom'].iloc[i], 
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

# Generate a range of ages from min to max
age_range = np.linspace(sfc_data['Age'].min(), sfc_data['Age'].max(), 100).reshape(-1, 1)

# Add the legend to the plot
plt.legend(title='End Contract')

plt.show()