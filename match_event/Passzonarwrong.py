#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 10:58:49 2021

@author: matfeig
"""

#https://medium.com/analytics-vidhya/football-stats-programming-with-python-pass-sonar-83108d9ee836
#https://medium.com/nightingale/passsonar-visualizing-player-interactions-in-soccer-analytics-7708e1d94afc

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import math
import matplotlib.pyplot as plt
import matplotlib.patches as pat

from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_color='lightgrey', line_color='white', stripe=False, axis=False, label=False, tick=False)
fig, ax = pitch.draw()


df = pd.read_csv('sfc_vadbomb.csv')

team = df[(df.team_id == 1330)]
events = team[(team.event_type_id == 30)]

#Data frame player player id et player name 
players = events.groupby(["player_name"],as_index=False)
players = players.agg({"player_id": "mean"})


##Visualisation vertical du terrain 
#events["location_x"] = round((events["location_x"]*68/100),1)
#events["location_y"] = round((events["location_y"]*105/100),1)
#events["end_location_x"] = round((events["end_location_x"]*68/100),1)
#events["end_location_y"] = round((events["end_location_y"]*105/100),1)


pass_events = events[events.event_type_id == 30]
pass_position = pass_events.groupby(["player_id"],as_index=False)
pass_position = pass_position.agg({"location_x": "mean","location_y": "mean"})
pass_position = pd.merge(pass_position, players, on="player_id")

#accurate_pass_events = pass_events[(pass_events.outcome_id==9)]


#if "pass_angle" in pass_events > 0:
pass_events['angle_deg']=pass_events['pass_angle'] * 180/math.pi
#else:
#    pass_events['angle_deg']=pass_events['pass_angle'] * 180/math.pi
                        
                        
def divide(angle, divisions):
  degree = 360 / divisions
  division = ((angle + (degree / 2)) // degree) + 1
  if division > angle:
    division = 1
  return division

def divide_pass_direction(row):
  return divide(row["angle_deg"],12)
  
pass_events["direction"] = pass_events.apply(divide_pass_direction, axis=1)

pass_sonar = pass_events.groupby(["player_name", "direction"], as_index=False)
pass_sonar = pass_sonar.agg({"pass_length": "mean", "event_type_id": "count"})
pass_sonar = pass_sonar.rename(columns={"event_type_id": "amount"})


fig, ax = pitch.draw()

for _, player in pass_position.iterrows():
  ax.text(
     player.location_x
    ,player.location_y
    ,player.player_name.encode().decode("unicode-escape", 'ignore')
    ,ha="center"
    ,va="center"
    ,color="black"
  )
  
  for _, pass_detail in pass_sonar[pass_sonar.player_name == player.player_name].iterrows():
    #Start degree of direction 1
    theta_left_start = 360
    
    #Color coding by distance
    color = "black"
    if pass_detail.pass_length < 15:
      color = "gold"
    elif pass_detail.pass_length< 25:
      color = "darkorange"
    #Calculate degree in matplotlib figure
    theta_left = theta_left_start - (360 / 12) * (pass_detail.direction - 1)
    theta_right = theta_left - (360 / 12)
    pass_wedge = pat.Wedge(
      center=(player.location_x, player.location_y)
      ,r=int(pass_detail.amount)*0.9
      ,theta1=theta_right
      ,theta2=theta_left
      ,facecolor=color
      ,edgecolor="white"
    )
    ax.add_patch(pass_wedge)
    
