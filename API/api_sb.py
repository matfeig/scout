#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 08:22:08 2022

@author: matfeig"""

from statsbombpy import sb
import pandas as pd
import numpy as np


DEFAULT_CREDS = {
    "user": "m.feigean@servettefc.ch",
    "passwd": "QzG3Kdlu",
}

# Looking at all competitions to search for comp and season id
comp = sb.competitions(creds = DEFAULT_CREDS)

############### SFC Super League #################################################################

#Choosing a competitions and season
swiss_2022 = sb.matches(competition_id= 80,season_id=281, creds = DEFAULT_CREDS)

player_match = sb.player_match_stats(3922596,creds = DEFAULT_CREDS)
player_match.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/yverdon_sfc_3.csv')

#lineup = sb.lineups(match_id=3838760,creds = DEFAULT_CREDS)["Servette"]

player_season = sb.player_season_stats(competition_id=80, season_id=281,creds = DEFAULT_CREDS)
player_season.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_season/23_24/matchday_23.csv')

team_season = sb.team_season_stats(competition_id=80, season_id=281,creds = DEFAULT_CREDS)
team_season.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_season/23_24/team_season_match_23.csv')

events = sb.events(match_id=3838760,creds = DEFAULT_CREDS)
events = sb.events(match_id=3838760,creds = DEFAULT_CREDS, split=True, flatten_attrs=False)


####### EUROPE ###################################################################################

#Choosing a competitions and season
swiss_2022 = sb.matches(competition_id=35,season_id=281, creds = DEFAULT_CREDS)

player_match = sb.player_match_stats(3910045,creds = DEFAULT_CREDS)
player_match.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/sfc_roma.csv')

#lineup = sb.lineups(match_id=3838760,creds = DEFAULT_CREDS)["Servette"]

player_season = sb.player_season_stats(competition_id=35, season_id=281,creds = DEFAULT_CREDS)
player_season.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_season/23_24/sfc_roma.csv')

# team_season = sb.team_season_stats(competition_id=80, season_id=235,creds = DEFAULT_CREDS)
# team_season.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_season/23_24/team_season_match_1.csv')

#########    M21  ########################################################################

#Choosing a competitions and season
swiss_2022 = sb.matches(competition_id=1525,season_id=281, creds = DEFAULT_CREDS)

player_match = sb.player_match_stats(3902918,creds = DEFAULT_CREDS)
player_match.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_match/23_24/M21/rapper_sfc_1.csv')

#lineup = sb.lineups(match_id=3838760,creds = DEFAULT_CREDS)["Servette"]

player_season = sb.player_season_stats(competition_id=1525, season_id=281,creds = DEFAULT_CREDS)
player_season.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/player_season/23_24/M21/j15.csv')

# team_season = sb.team_season_stats(competition_id=80, season_id=235,creds = DEFAULT_CREDS)
#team_season.to_csv('/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/team_season/23_24/team_season_match_1.csv')

######################
#### Recrutement #####
######################

df1 = sb.player_season_stats(competition_id=35, season_id=281,creds = DEFAULT_CREDS)
#player_season.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/suisse.csv')

df2 = sb.player_season_stats(competition_id=47, season_id=235,creds = DEFAULT_CREDS)
#player_season.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/austria.csv')

df3 = sb.player_season_stats(competition_id=63, season_id=235,creds = DEFAULT_CREDS)
#player_season.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/netherland.csv')

df4 = sb.player_season_stats(competition_id=13, season_id=235,creds = DEFAULT_CREDS)
#player_season.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/portugal.csv')

df5 = sb.player_season_stats(competition_id=8, season_id=235,creds = DEFAULT_CREDS)
#player_season.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/france.csv')

df = pd.concat([df1, df2, df3, df4, df5])
df.columns = df.columns.str.lstrip("player_season_")
df.to_csv('/Users/matfeig/Dropbox/SFC/Database/recrutement/df_api_stats_03-2023.csv')