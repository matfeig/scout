#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:19:46 2021

@author: matfeig
"""
import pandas as pd
import numpy as np
import streamlit as st

# Data import & columns
df = pd.read_csv('df_final.csv')

positions = list(df['Pos'].drop_duplicates())
teams = list(df['Squad'].drop_duplicates())

# Sidebar - title & filters
st.sidebar.markdown('### Data Filters')
position_choice = st.sidebar.multiselect(
    'Choose position:', positions, default=positions)
teams_choice = st.sidebar.multiselect(
    "Teams:", teams, default=teams)
price_choice = st.sidebar.slider(
    'Age', min_value=15.0, max_value=40.0, step=.5, value=15.0)

df = df[df['Pos'].isin(position_choice)]
df = df[df['Squad'].isin(teams_choice)]
df = df[df['Age'] < price_choice]

st.title(f"Servette FC - Recrutement")

# Main - dataframes
st.markdown('### Player Dataframe')

st.dataframe(df.sort_values('Born',
             ascending=False).reset_index(drop=True))