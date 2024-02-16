#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 16:37:21 2022

@author: matfeig
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

#load data
data = pd.read_excel("superleague.xlsx")
data.head()
data.describe()

###Our aim is to get a model together that would help us to predict a team’s points based on their squad value
sns.pairplot(data[['year','GD', 'squad-value', 'points', 'position','goal','goala']])

#Points & goal difference correlate really strongly, as you might expect.
#Squad value goes up as goal difference and points go up, but as more of a curve than a line.
#Squad value has increased over time (important! We’ll come back to this)


#We need to define what performance is. I think that we can answer 
#this by seeing which of points and position correlate more with squad value.
#Let’s check if position correlates more than points:

abs(data['squad-value'].corr(data['position'])) < data['squad-value'].corr(data['points'])
#The squad value is more correlated with points
correlation_df = data.corr()

#1- Get our two columns into variables, then reshape them

X = data['squad-value']
y = data['points']

X = X.values.reshape(-1,1)
y = y.values.reshape(-1,1)

#2- Use the train_test_split function to create our training sets & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)

lm = LinearRegression()
lm.fit(X_train,y_train)

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)

print(lm.coef_)

predictions = lm.predict(X_test)
plt.scatter(X_test, y_test,  color='purple')
plt.plot(X_test, predictions, color='green', linewidth=3)
plt.title("Suisse Squad value vs points - Model One")
plt.show()

plt.scatter(y_test,predictions)

plt.title('How many points out is each prediction?')
sns.distplot((y_test-predictions),bins=50, color = 'purple')

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, predictions))

df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': predictions.flatten()})
df.head()
df['Actual'].corr(df['Predicted'])

#Blank list
relativeValue = []

#Loop through each row
for index, team in data.iterrows():
    
    #Obtain which season we are looking at
    season = team['Season']
    
    #Create a new dataframe with just this season
    teamseason = data[data['Season'] == season]
    
    #Find the max value
    maxvalue = teamseason['Squad Value'].max()
    
    #Divide this row's value by the max value for the season
    tempRelativeValue = team['Squad Value']/maxvalue
    
    #Append it to our list
    relativeValue.append(tempRelativeValue)
    
#Add list to new column in main dataframe
data["Relative Value"] = relativeValue

data.head()
sns.pairplot(data[['GD', 'Squad Value', 'Relative Value', 'Points', 'Position']])

#Assign relevant columns to variables and reshape them
X = data['Relative Value']
y = data['Points']
X = X.values.reshape(-1,1)
y = y.values.reshape(-1,1)

#Create training and test sets for each of the two variables
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)

#Create an empty model, then train it against the variables
lm = LinearRegression()
lm.fit(X_train,y_train)

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)
print(lm.coef_/10)

predictions = lm.predict(X_test)

plt.scatter(X_test, y_test,  color='purple')
plt.plot(X_test, predictions, color='green', linewidth=3)
plt.title("Relative Squad value vs points - Model Two")
plt.show()

plt.scatter(y_test,predictions)
plt.title('How many points out is each prediction?')
sns.distplot((y_test-predictions),bins=50,color='purple')

print('MAE:', metrics.mean_absolute_error(y_test, predictions))






