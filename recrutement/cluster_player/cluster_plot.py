#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 11:30:12 2021

@author: matfeig
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

df = pd.read_excel("wingers_kmeans_absvalues.xlsx")

dfns=df[df["Comp"] != "it Serie A"]
df

df_fw_list=list(dfns["Player"])
df_fw_list

df1=df.replace(to_replace=df_fw_list,value="")
df1

df1=df1.drop(columns=["Unnamed: 0","Squad","Comp"])
df1

pd.set_option("display.max_rows",70)
df1.isnull().sum()

df1=df1.fillna(df1.mean())

df1.isnull().sum()

names=df1.Player.tolist()
clusters=df1.k_means.tolist()
df1=df1.drop(["Player"],axis=1)
df1=df1.drop(["k_means"],axis=1)
df1.head()

from sklearn import preprocessing
x = df1.values # numpy array
scaler = preprocessing.MinMaxScaler()
x_scaled = scaler.fit_transform(x)
X_norm = pd.DataFrame(x_scaled)

from sklearn.decomposition import PCA
pca = PCA(n_components = 2) # 2D PCA for the plot
reduced = pd.DataFrame(pca.fit_transform(X_norm))

reduced['cluster'] = clusters
reduced['name'] = names
reduced.columns = ['x', 'y', 'cluster', 'name']
reduced.head()

sns.set(style="white")


ax = sns.lmplot(x="x", y="y", hue='cluster', data = reduced, legend=False,
                fit_reg=False, height = 30, scatter_kws={"s": 250})

texts = []
for x, y, s in zip(reduced.x, reduced.y,reduced.name):
  texts.append(plt.text(x, y, s))

ax.set(ylim=(-2, 2))
plt.tick_params(labelsize=15)
plt.xlabel("PC 1", fontsize = 20)
plt.ylabel("PC 2", fontsize = 20)
plt.show()