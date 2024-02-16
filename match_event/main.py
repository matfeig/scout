# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 18:57:49 2020

@author: monte
"""

import plot

team = 'BSC Young Boys'              #équipe à considérer
pitch_color = "papayawhip"                          #couleur du terrain
line_color = "black"                                #couleur des lignes
list_action = ['Interceptions', 'Picking-ups']      #liste d'action à considérer


plot.drawAction(list_action ,team, pitch_color, line_color, "h", "full", diff='joueur')

plot.drawAssists(team, pitch_color, line_color, "h", "full")

plot.heat_zones(list_action, team, "h", "full")

plot.heat_map(list_action, team, "h", "full",50)

plot.draw_jointplot(list_action, team, "scatter", pitch_color, line_color, "h", "full")
plot.draw_jointplot(list_action, team, "kde", pitch_color, line_color, "h", "full")
plot.draw_jointplot(list_action, team, "hex", pitch_color, line_color, "h", "full")

plot.goalKicks(team, heatmap=True)
plot.goalKicks(team, heatmap=False)

plot.draw_ellipse(team, orientation='h')
