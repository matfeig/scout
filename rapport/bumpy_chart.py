import json
from urllib.request import urlopen
import requests
from mplsoccer.statsbomb import EVENT_SLUG, read_event, read_competition, read_match
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from highlight_text import fig_text

from mplsoccer import Bumpy, FontManager, add_image

creds = {"user":"m.feigean@servettefc.ch","passwd":"QzG3Kdlu"}
username = creds["user"]
password = creds["passwd"]

auth = requests.auth.HTTPBasicAuth(username, password)

URL = "https://data.statsbombservices.com/api/v4/competitions"
response = requests.get(URL, auth=auth)
df_compet = read_competition(response,warn=False)
df_compet = df_compet[(df_compet.competition_name == "Super League")]

# season id 2019/2020 : 42
# season id 2020/2021 : 90
# season id 2021/2022 : 108

URL = "https://data.statsbombservices.com/api/v4/competitions/80/seasons/235/matches"
response = requests.get(URL, auth=auth)
df_matches = read_match(response, warn=False)

def ranking_by_week(season_id) :

    URL = "https://data.statsbombservices.com/api/v4/competitions/80/seasons/%s/matches"%season_id
    response = requests.get(URL, auth=auth)
    df_matches = read_match(response, warn=False)
    df_matches = df_matches.dropna(subset=['home_score', 'away_score'])
    df_matches.sort_values(by=["match_week"],ascending = True,inplace=True)
    df_matches.reset_index(drop = True,inplace=True)

    teams = np.array(list(df_matches["home_team_name"].value_counts().index))
    points = {}
    goals_difference = {}
    goals = {}
    season_ranking = {}
    for team in teams :
        points[team] = 0
        goals_difference[team] = 0
        goals[team] = 0
        season_ranking[team] = []

    week = 1
    for ind in df_matches.index :
        team1 = df_matches['home_team_name'][ind]
        team2 = df_matches['away_team_name'][ind]
        diff = df_matches['home_score'][ind] - df_matches['away_score'][ind]
        goals_difference[team1] += diff
        goals_difference[team2] -= diff
        goals[team1] += df_matches['home_score'][ind]
        goals[team2] += df_matches['away_score'][ind]
        if diff > 0 :
            points[team1] += 3
        elif diff < 0 :
            points[team2] += 3
        else :
            points[team1] += 1
            points[team2] += 1
        if df_matches['match_week'][ind] != week :
            df_points = pd.DataFrame(list(points.items()), columns=['Team', 'Points'])
            df_goals_difference = pd.DataFrame(list(goals_difference.items()), columns=['Team', 'Goals Difference'])
            df_goals = pd.DataFrame(list(goals.items()), columns=['Team', 'Goals'])
            df_goals_difference.drop(['Team'], axis=1, inplace=True)
            df_goals.drop(['Team'], axis=1, inplace=True)
            df_classement = pd.concat([df_points, df_goals_difference, df_goals], axis=1)
            df_classement.sort_values(by=['Points', 'Goals Difference', 'Goals'], ascending=False, inplace=True)
            df_classement.reset_index(drop=True, inplace=True)
            for id in df_classement.index :
                team_name = df_classement['Team'][id]
                l = season_ranking[team_name]
                l.append(id + 1)
                season_ranking[team_name] = l
            week = df_matches['match_week'][ind]
    df_points = pd.DataFrame(list(points.items()), columns=['Team', 'Points'])
    df_goals_difference = pd.DataFrame(list(goals_difference.items()), columns=['Team', 'Goals Difference'])
    df_goals = pd.DataFrame(list(goals.items()), columns=['Team', 'Goals'])
    df_goals_difference.drop(['Team'], axis=1, inplace=True)
    df_goals.drop(['Team'], axis=1, inplace=True)
    df_classement = pd.concat([df_points, df_goals_difference, df_goals], axis=1)
    df_classement.sort_values(by=['Points', 'Goals Difference', 'Goals'], ascending=False, inplace=True)
    df_classement.reset_index(drop=True, inplace=True)
    for id in df_classement.index:
        team_name = df_classement['Team'][id]
        l = season_ranking[team_name]
        l.append(id + 1)
        season_ranking[team_name] = l
    return(season_ranking)

season_ranking = ranking_by_week(235)


font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/"
                           "static/Roboto-Regular.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/"
                         "static/Roboto-Medium.ttf?raw=true"))



# match-week
match_day = ["Week " + str(num) for num in range(1, 37)]

# highlight dict --> team to highlight and their corresponding colors

highlight_dict = {
    "Servette": "firebrick"
}
# highlight_dict = {
#     "BSC Young Boys": "gold",
#     "Basel": "orangered",
#     "Servette": "firebrick",
#     "Luzern" : "blue",
#     "Winterthur" : "white",
#     "Lugano" : "black",
#     "St. Gallen" : "limegreen",
#     "FC Zürich" : "deepskyblue",
#     "Grasshopper" : "coral",
#     "Sion" : "red"
# }

# #Spécifique team
# highlight_dict = {"Servette": "firebrick",}

# instantiate object
bumpy = Bumpy(
    background_color="white", scatter_color="lightgrey", line_color="lightgrey",  # scatter and line colors
    rotate_xticks=90,  # rotate x-ticks by 90 degrees
    ticklabel_size=25, label_size=25,  # ticklable and label font-size
    scatter_primary='o',  # marker to be used
    show_right=True,  # show position on the rightside
    plot_labels=True,  # plot the labels
    alignment_yvalue=0.5,  # y label alignment
    alignment_xvalue=0.065  # x label alignment
)

# plot bumpy chart
fig, ax = bumpy.plot(
    x_list=match_day,  # match-day or match-week
    y_list=np.linspace(1, 10, 10).astype(int),  # position value from 1 to 20
    values=season_ranking,  # values having positions for each team
    secondary_alpha=0.5,   # alpha value for non-shaded lines/markers
    highlight_dict=highlight_dict,  # team to be highlighted with their colors
    figsize=(45, 20),  # size of the figure
    x_label='Week', y_label='Position',  # label name
    ylim=(-0.1,11),  # y-axis limit
    lw=2.5,   # linewidth of the connecting lines
    fontproperties=font_normal.prop,   # fontproperties for ticklables/labels
)

# title and subtitle
TITLE = "Super League 2021/2022"
SUB_TITLE = "<YB>, <Basel>, <SFC>, <Luzern>, <Winterthur>, <Lugano>, <St. Gallen>, <FC Zürich>, <GC>, <Sion>"

# add title
fig.text(0.09, 0.95, TITLE, size=40, color="#F2F2F2", fontproperties=font_bold.prop)

# add subtitle
fig_text(
    0.09, 0.94, SUB_TITLE, color="#F2F2F2",
    highlight_textprops=[{"color": 'gold'}, {"color": 'orangered'}, {"color": 'firebrick'},
                         {"color": 'blue'}, {"color": 'grey'}, {"color": 'black'},
                         {"color": 'limegreen'}, {"color": 'deepskyblue'}, {"color": 'coral'},
                         {"color": 'red'}],
    size=40, fig=fig, fontproperties=font_bold.prop
)

