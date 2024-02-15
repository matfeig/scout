#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 18:09:31 2021

@author: matfeig
"""
import API
import indices
import xThreat
import pandas as pd
import numpy as np
import pandas as pd

df = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/team_matches.csv")
del df['Unnamed: 0']

df

sfc = df.groupby('team_name')

n = df.groupby("team_name").describe()

n.to_excel('file_name.xls', index=True)

