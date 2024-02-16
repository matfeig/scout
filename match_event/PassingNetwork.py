# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 18:19:58 2020

@author: peter
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv('lau_sion.csv')

f = {'pos_x':['mean'], 'pos_y':['mean'], 'Action': ['count']}
df_AvgPosPasses = df[(df['Action']=='Passes accurate')].groupby(['code']).agg(f).reset_index()

df_AvgPosPasses.columns = ['code','X','Y','Passes']

Passer_Servette = []
Receiver_Servette = []
xPos_Pass_Serv = []
yPos_Pass_Serv = []
xPos_Rec_Serv = []
yPos_Rec_Serv = []
Passer_Zurich = []
Receiver_Zurich = []
xPos_Pass_Zurich = []
yPos_Pass_Zurich = []
xPos_Rec_Zurich = []
yPos_Rec_Zurich = []

tmp_passer = ''
tmp_receiver = ''
tmp_team = ''

for index, row in df.iterrows():
    print(index)
    print(row['code'])
    print(row['Action'])
    if(row['Action']=='Passes accurate'):
        tmp_passer = row['code']
        tmp_team = row['Team']
        tmp_xpos_pass = row['pos_x']
        tmp_ypos_pass = row['pos_y']
        tmp_xpos_rec = 0
        tmp_ypos_rec = 0
        find_receiver = False
        print('Tmp_passer: ',tmp_passer)
        print('Tmp_team: ',tmp_team)
        i = 1
        while not find_receiver:
            if(index+i >= len(df.index)):
                break
            print(find_receiver)
            print('code: ',df.iloc[index+i]['code'])
            print('Team: ',df.iloc[index+i]['Team'])
            if(df.iloc[index+i]['code']!=tmp_passer and df.iloc[index+i]['Team']==tmp_team):
                tmp_receiver = df.iloc[index+i]['code']
                tmp_xpos_rec = df.iloc[index+i]['pos_x']
                tmp_ypos_rec = df.iloc[index+i]['pos_y']
                find_receiver = True
            else:
                i = i+1
        if(tmp_team=='Sion'):
            Passer_Servette.append(tmp_passer)
            Receiver_Servette.append(tmp_receiver)
            xPos_Pass_Serv.append(tmp_xpos_pass)
            yPos_Pass_Serv.append(tmp_ypos_pass)
            xPos_Rec_Serv.append(tmp_xpos_rec)
            yPos_Rec_Serv.append(tmp_ypos_rec)
        if(tmp_team=='Lausanne-Sport'):
            Passer_Zurich.append(tmp_passer)
            Receiver_Zurich.append(tmp_receiver)
            xPos_Pass_Zurich.append(tmp_xpos_pass)
            yPos_Pass_Zurich.append(tmp_ypos_pass)
            xPos_Rec_Zurich.append(tmp_xpos_rec)
            yPos_Rec_Zurich.append(tmp_ypos_rec)

dfRelPasses_Serv = pd.DataFrame()
dfRelPasses_Zur = pd.DataFrame()

dfRelPasses_Serv['Passer'] = Passer_Servette
dfRelPasses_Serv['Receiver'] = Receiver_Servette
dfRelPasses_Serv['xPos_Pass'] = xPos_Pass_Serv
dfRelPasses_Serv['yPos_Pass'] = yPos_Pass_Serv
dfRelPasses_Serv['xPos_Rec'] = xPos_Rec_Serv
dfRelPasses_Serv['yPos_Rec'] = yPos_Rec_Serv


df_countRelPasses_Serv = dfRelPasses_Serv.groupby(['Passer','Receiver']).agg(['count']).reset_index()


df_countRelPasses_Serv = df_countRelPasses_Serv.drop(['yPos_Pass','xPos_Rec','yPos_Rec'], axis=1)
df_countRelPasses_Serv.columns = ['Passer','Receiver','Passes']

#Create network plot
import networkx as nx

G1 = nx.DiGraph(team='Sion')

for index, row in df_countRelPasses_Serv.iterrows():
    G1.add_edge(row['Passer'], row['Receiver'], weight=row['Passes'])


pos1 = nx.spring_layout(G1)
nome2degree = dict(G1.degree())
nx.draw(G1,pos=pos1,node_size=[deg * 50 for deg in nome2degree.values()],nodelist=list(nome2degree.keys()),font_size='smaller',with_labels=True, font_weight='light', alpha=0.5)

plt.show()

##Alternative method
#edge_x = []
#edge_y = []
#for edge in G1.edges():
#    x0, y0 = G1.nodes[edge[0]]['pos']
#    x1, y1 = G1.nodes[edge[1]]['pos']
#    edge_x.append(x0)
#    edge_x.append(x1)
#    edge_x.append(None)
#    edge_y.append(y0)
#    edge_y.append(y1)
#    edge_y.append(None)
#
#edge_trace = go.Scatter(
#    x=edge_x, y=edge_y,
#    line=dict(width=0.5, color='#888'),
#    hoverinfo='none',
#    mode='lines')



