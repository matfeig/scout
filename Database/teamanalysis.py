#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 20:30:24 2021

@author: matfeig
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


file = '/Users/matfeig/Dropbox/SFC/code/Database/team_matches.csv'
data = pd.read_csv(file)

data.describe()

exploration = data.describe()
exploration = exploration.drop(exploration.columns[[0, 1, 2]], axis=1)
exploration.describe().to_csv('description.csv')

data.isna().any()

data.team_name.unique()
team = data.groupby(['team_name']).mean()
team = team.drop(team.columns[[0, 1, 2]], axis=1)
team.describe().to_csv('teamdescription.csv')

df_analysis = pd.concat([exploration, team])
df_analysis.to_csv('team.csv')