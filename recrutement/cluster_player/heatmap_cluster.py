#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 16:38:11 2021

@author: matfeig
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#######################
### Joueur Offensif ###
#######################

# Download data - Obsolute value / median value
data = pd.read_excel("fw_kmeans_absvalues_median.xlsx")
del data ["k_means"]
data.head(6)

# Prepare the data
## Drop the cluster 
#data = data.drop(columns = "Cluster")
## Store all column names in a list to add to the final dataframe
columns = data.columns.tolist()
print (columns)


##Scale data because the "Carries" values are much higher than the others¶
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
data_scaled = pd.DataFrame(scaler.fit_transform(data), columns = columns)

#Prepare the names of clusters for the heatmap
y_axis_labels = ["Selfish & Risky","Scoring chance generator", "Dribblers","Target Man","Finisher", "Efficient attacking creator"]
#y_axis_labels = ["1", "2", "3", "4", "5", "6"]



#3. Plot the heatmap
##The "cmap" parameter controls the colour palette. See more colour options here: https://seaborn.pydata.org/tutorial/color_palettes.html
##To inverse the gradient, add the "_r" to the "Blues" – > "Blues_r"

fig, ax = plt.subplots()
fig.set_size_inches(16, 6)
ax=sns.heatmap(data_scaled,cmap = "Blues", yticklabels=y_axis_labels)
plt.show()