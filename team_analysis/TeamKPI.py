#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 11:10:13 2022

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

df1 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/stat_2022.csv')
df1 = df1.rename(columns={'Team Name': 'Team'})
df2 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/stat_2021.csv')
df2 = df2.rename(columns={'Team Name': 'Team'})
df3 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/stat_2020.csv')
df3 = df3.rename(columns={'Team Name': 'Team'})
df10 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/stat_2023.csv')
df10 = df10.rename(columns={'Team Name': 'Team'})

df4 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/2022.csv')
df5 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/2021.csv')
df6 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/2020.csv')
df11 = pd.read_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_league/2023.csv')


df7 = df1.merge(df4,on='Team')
df8 = df2.merge(df5,on='Team')
df9 = df3.merge(df6,on='Team')
df12 = df10.merge(df11,on='Team')

df = pd.concat([df7,df8,df9, df12])
df.reset_index(inplace=True)

###Our aim is to get a model together that would help us to predict a team’s points based on their squad value
sns.pairplot(df[['Pts','W', 'GD', 'Sh', 'xG','P','Possession%','OBV','Goals.1']])
#sns.pairplot(df[['Pts','Goal Difference', 'NP Goal Difference', 'NP xG Difference', 'xG/Shot','Penalty Goals','Passes Inside Box','Shot Distance','SP xG']])

dfcor = df[['Pts','W', 'GD', 'Sh', 'xG','P','Possession%','OBV','Goals.1']]
correlation_df = dfcor.corr()

df['Pts'].corr(df['W'])


tot_corr_df = df.corr()
pts = tot_corr_df['Pts']
pts.to_excel('correlation.xlsx')


#1- Get our two columns into variables, then reshape them

# Goal Difference
# Goals
# OBV
# xGD
# NP xG
# Shot OBV
# D&C OBV
# Passes Inside Box
# Deep Progressions
# Goals.1
#P asses.1

X = df['Pressures']
y = df['Pts']

X = X.values.reshape(-1,1)
y = y.values.reshape(-1,1)

#2- Use the train_test_split function to create our training sets & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)

lm = LinearRegression()
lm.fit(X_train,y_train)

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)

print(lm.coef_)

predictions = lm.predict(X_test)
plt.scatter(X_test, y_test,  color='black')
plt.plot(X_test, predictions, color='blue', linewidth=1)
plt.axhline(y=2, xmin=0.05, xmax=50, linewidth=0.5, color = '#870E26')
#plt.axhline(y=50, xmin=0.05, xmax=50, linewidth=0.5, color = 'black')
#plt.axhline(y=54, xmin=0.05, xmax=50, linewidth=0.5, color = 'RED')
plt.title("GD vs points - Model One")
plt.show()

required_pts = 66
goal_diff_needed = (required_pts - lm.intercept_)/lm.coef_
print(goal_diff_needed)
print(goal_diff_needed/38)

