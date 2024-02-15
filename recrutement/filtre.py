#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:07:01 2022

@author: matfeig
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.pyplot import figure

contrat = pd.read_csv('player_contract.csv')
contrat['player_date_of_birth'] = contrat['player_date_of_birth'].str.replace('T00:00:00.000Z','')
contrat['competition_season_title_name_TFM'] = contrat['competition_season_title_name_TFM'].str.replace('Clubs - ','')
contrat['competition_season_title_name_TFM'] = contrat['competition_season_title_name_TFM'].str.replace(' 22/23','')
contrat['joined_date'] = contrat['joined_date'].str.replace('T00:00:00.000Z','')
contrat['contract_until'] = contrat['contract_until'].str.replace('T00:00:00.000Z','')
contrat = contrat.drop(['player_nationality_first_trigram', 'player_nationality_second_trigram','player_nationality_first_confederation',
                        'player_nationality_second_confederation','player_type','competition_pull_type','competition_code_TFM',
                        'season_start_year_TFM','season_start_year_actual','joined_from_club_URL','pull_url'], axis=1)
contrat['contract_until'] = contrat['contract_until'].fillna('unknow')
contrat['contract_until'].dtypes
contrat.dtypes
#contrat['player_height_']= contrat['player_height']*10

player = pd.read_csv("/Users/matfeig/Dropbox/SFC/Database/player_season/player_id.csv")
player = player.rename(columns={'Primary Position':'Primary'})


###
### Changer le nom de column
###
# df.columns = df.columns.str.replace('Non-Penalty Goals', 'Goals')


df= contrat.loc[(contrat.contract_until == "2023-06-30")|(contrat.contract_until == "23-05-31")| (contrat.contract_until == "unknown")|(contrat.contract_until == "2024-06-30")]
df= df.loc[(df.player_position == "Left-Back")]

df1 = player.loc[(player.Primary == "Left Back")|(player.Primary == "Left Wing Back")]
df1 = df1.loc[(df1.Season == "2022/2023")]


# Filtrer l'age
df = df[df.Age> 22]
df = df[df.Age< 30]

##Choisir les variables 
df=df.loc[(df.player_season_minutes>=300)]

#Slect Comptetion
df = df[(df.competion_name != "Challenge League") & (df.competion_name != "Super League")]

#Select team
df = df[(df.team_name != "FC Porto") & (df.team_name!= "Sporting Braga")]

#Filtrer valeur xG
df= df[df.minutes < 900]
df1 = df[df.xG > 0.3]
df2 = df1[df.TB >2]
df3 = df2[df.pshot > 0.20]
df4 = df3[df.aerwinper > 0.010]
df5 = df4[df.perf < 0.0]


## obtenir les joueurs voulus aves les données Statsbomb ###

bool_series = df.duplicated(subset=['player_date_of_birth','competition_season_title_name_TFM'])
true_count = sum(bool_series)
print (true_count)
new_df = pd.merge(df, df1,  how='left', left_on=['player_date_of_birth','competition_season_title_name_TFM'], right_on = ['birth_date','competition_name'])
new_df.to_csv('/Users/matfeig/Dropbox/df.csv')






### erger l

new_df = pd.merge(contrat, player,  how='left', left_on=['player_date_of_birth','competition_season_title_name_TFM'], right_on = ['birth_date','competition_name'])
bool_series = contrat.duplicated(subset=['player_date_of_birth','competition_season_title_name_TFM'])
true_count = sum(bool_series)
print (true_count)


new_df = pd.merge(contrat, player,  how='left', left_on=['player_date_of_birth','competition_season_title_name_TFM'], right_on = ['birth_date','competition_name'])
bool_series = contrat.duplicated(subset=['player_date_of_birth','competition_season_title_name_TFM'])
true_count = sum(bool_series)
print (true_count)



