#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:06:43 2024

@author: matfeig
"""
import pandas as pd
import streamlit as st
import os

# Use an environment variable to specify the path

# csv_file_path = os.getenv('CSV_FILE_PATH', '/Users/matfeig/Desktop/scouting/database.csv')

# df = pd.read_csv(csv_file_path)

csv_file_path = os.getenv('database.csv')

df = pd.read_csv("database.csv")



##########################################################################################

df= df[(df["Contact"] == 'Scout SFC')]

#########################################
# Selecting only the specified columns
selected_columns = ['Submitted at', 'Nom du Scout', 'Prénom du joueur','Nom du joueur','Position','Pied','Aperçu', 'Commentaire / Overview']
df_selected = df[selected_columns]
df_selected = df_selected.loc[:, ~df_selected.columns.duplicated(keep='first')]

df_selected  = df_selected.rename(columns={'Prénom du joueur': 'Prenom'})
df_selected  = df_selected.rename(columns={'Nom du joueur': 'Nom'})
df_selected  = df_selected.rename(columns={'Commentaire / Overview': 'Commentaire'})


###########################################################################################

# Sélection des colonnes à afficher
select_columns = ['Nom','Position', 'Pied', 'Aperçu','Commentaire']  # Assurez-vous que les noms de colonnes correspondent exactement à ceux de votre fichier CSV

# Filtrer le DataFrame pour ne conserver que les colonnes sélectionnées
filtered_df = df_selected[select_columns]
filtered_df = filtered_df.reset_index(drop=True)
filtered_df = filtered_df.iloc[::-1].reset_index(drop=True)


# Créer l'interface utilisateur avec Streamlit
st.title('Scouting DataBase | Servette FC')

st.write("Liste des joueurs")
st.table(filtered_df)
