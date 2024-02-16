#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 13:30:48 2023

@author: matfeig
"""
import pandas as pd

# Load the dataset with the correct delimiter and skip the first row
data = pd.read_csv('/Users/matfeig/Desktop/test.csv', delimiter=';', skiprows=1)

# Display the first few rows of the dataset
data.head()

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Sort data by 'V02max' in descending order
sorted_by_v02max = data_2023.sort_values(by="V02max", ascending=False)

# Calculate colors for each data point in the sorted dataset
sorted_colors_v02max = cmap(norm(sorted_by_v02max["V02max"].values))


# Beeswarm plot with 'Nom' sorted by 'V02max', adjusted colors, and a dashed line at V02max = 80
plt.figure(figsize=(20, 8))
sns.swarmplot(x=sorted_by_v02max["Nom"], y=sorted_by_v02max["V02max"], color="none", size=8, edgecolor=sorted_colors_v02max)
plt.axhline(80, color='grey', linestyle='--', label="V02max = 80")
plt.xticks(rotation=90)
plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), label="V02max")
plt.title('V02max Servette FC - 2023 - été')
plt.ylabel("V02max")
plt.legend()
plt.tight_layout()
plt.show()
