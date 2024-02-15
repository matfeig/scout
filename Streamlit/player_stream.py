import pandas as pd
import numpy as np
import streamlit as st

# Data import & columns
data = pd.read_csv('data_player.csv')
del data['Unnamed: 0']

# ##Ajout d'un variable 
# df['90s'] = df['minutes']/90


# ### Ajout de variable + Calcult pour chaque varaible) 
# calc_elements = ['goals', 'assists', 'points']

# for each in calc_elements:
#     df[f'{each}_p90'] = df[each] / df['90s']

#Creation d'une liste 
teams = list(data['Team'].drop_duplicates())

# App

# Sidebar - title & filters
st.sidebar.markdown('### Title')
teams_choice = st.sidebar.multiselect(
    "Teams :", teams, default=teams)
price_choice = st.sidebar.slider(
    'Time :', min_value=304.0, max_value=1608.0, step=.5, value=304.0)

data = data[data['Team'].isin(teams_choice)]
data = data[data['Minutes'] < price_choice]

# # Main
# st.title(f"Servette FC - Recrutement")

# # Main - dataframes
# st.markdown('### Player Dataframe')

# st.dataframe(df.sort_values('points',
#              ascending=False).reset_index(drop=True))

# # Main - charts
# st.markdown('### Cost vs 20/21 Points')

# st.vega_lite_chart(df, {
#     'mark': {'type': 'circle', 'tooltip': True},
#     'encoding': {
#         'x': {'field': 'cost', 'type': 'quantitative'},
#         'y': {'field': 'points', 'type': 'quantitative'},
#         'color': {'field': 'position', 'type': 'nominal'},
#         'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
#     },
#     'width': 700,
#     'height': 400,
# })

# st.markdown('### Goals p90 vs Assists p90')

# st.vega_lite_chart(df, {
#     'mark': {'type': 'circle', 'tooltip': True},
#     'encoding': {
#         'x': {'field': 'goals_p90', 'type': 'quantitative'},
#         'y': {'field': 'assists_p90', 'type': 'quantitative'},
#         'color': {'field': 'position', 'type': 'nominal'},
#         'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
#     },
#     'width': 700,
#     'height': 400,
# })
