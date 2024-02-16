#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 16:16:39 2022

@author: matfeig
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

contracts = pd.read_excel("Classeur1.xlsx")

team_age_minutes = pd.read_csv('team-age-minutes.csv')

contracts['age_begin'] = contracts.apply(lambda row: row['Age'] - (2022 - row['begin']) ,axis=1)
contracts['age_end'] = contracts.apply(lambda row: row['Age'] - (2022 - row['end']) ,axis=1)

x = contracts[['Name','Age','age_begin','age_end']].copy()


fig = go.Figure()
x = x.sort_values('Age').copy()
fig.add_trace(
    go.Scatter(mode='markers',x=x['age_begin'],y=x['Name'], name='Age at start of contract',
    marker=dict(
            symbol = 'line-ns',
            color='rgba(135, 206, 250, 0.5)',
            size=10,
            line=dict(
                color='red',
                width=2
            )
        ),))

fig.add_trace(
    go.Scatter(mode='markers',x=x['age_end'],y=x['Name'],name='Age at end of contract',
    marker=dict(
            symbol = 'line-ns',
            color='rgba(135, 206, 250, 0.5)',
            size=10,
            line=dict(
                color='red',
                width=2
            )
        ),))
    
for i in range(len(x)):
    selected = x.iloc[i]
    y_ = selected['Name']
    x_0 = selected['age_begin']
    x_1 = selected['age_end']
    fig.add_shape(type="line", x0=x_0, y0=y_, x1=x_1, y1=y_, line_width=2, line_color="black")


fig.add_trace(
    go.Scatter(mode='markers',x=x['Age'],y=x['Name'],name='Current age',
    marker=dict(
            color='rgba(135, 206, 250, 0.5)',
            size=10,
            line=dict(
                color='red',
                width=2
            )
        ),))

fig.add_shape(type='rect',x0=15,x1=21,y0=-2,y1=28,fillcolor='#e9f1f8',opacity=0.2)
fig.add_shape(type='rect',x0=21,x1=27,y0=-2,y1=28,fillcolor='#d6e5f2',opacity=0.2)
fig.add_shape(type='rect',x0=27,x1=31,y0=-2,y1=28,fillcolor='#9fc2e0',opacity=0.2)
fig.add_shape(type='rect',x0=31,x1=40,y0=-2,y1=28,fillcolor='#5593c8',opacity=0.2)


    
fig.update_layout(height=1200)
# fig.update_yaxes(type='category')
#for template in ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]:
for template in ["plotly_white"]:
    fig.update_layout(template=template, title=template)
    fig.write_html("nom_du_fichier.html", auto_open=True)
    fig.show()