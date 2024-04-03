#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:56:37 2023

@author: matfeig
"""

import pandas as pd
import streamlit as st
import spacy
from io import BytesIO


# Charger le modèle de langue française
nlp = spacy.load("fr_core_news_sm")

# User credentials (in a real app, consider a more secure approach!)
USER_CREDENTIALS = {
    "Scout": "ServetteFC1890!",
}

def check_credentials(username, password):
    """Check if the entered username and password match the stored credentials."""
    return USER_CREDENTIALS.get(username) == password

def show_login_page():
    """Display the login form and return True if the user successfully logs in, False otherwise."""
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if check_credentials(username, password):
            # On successful login, use session_state to indicate logged in status
            st.session_state["logged_in"] = True
            return True
        else:
            st.error("The username or password you have entered is incorrect.")
            return False
    return False

# Initialize session_state.logged_in if it doesn't exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Main app
if st.session_state["logged_in"]:
    
    # The main app content should only be displayed if logged in
    csv_file_path = 'database.csv'  # Assuming CSV is in the same directory
    df = pd.read_csv(csv_file_path)
    df = df[df["Contact"] == 'Scout SFC']

    # Preparing the DataFrame
    selected_columns = ['Submitted at', 'Nom du Scout', 'Prénom du joueur', 'Nom du joueur', 'Position', 'Pied', 'Aperçu', 'Commentaire / Overview']
    df_selected = df[selected_columns]
    df_selected = df_selected.loc[:, ~df_selected.columns.duplicated(keep='first')]
    df_selected = df_selected.rename(columns={'Prénom du joueur': 'Prenom', 'Nom du joueur': 'Nom', 'Commentaire / Overview': 'Commentaire'})
    df_selected = df_selected.sort_values('Nom', ascending=True)
    select_columns = ['Nom', 'Position', 'Pied', 'Aperçu', 'Commentaire']
    filtered_df = df_selected[select_columns].reset_index(drop=True)

    st.title('Scouting DataBase | Servette FC')
    
    # Filters
    position_options = st.multiselect('Filtrer par Position', options=filtered_df['Position'].unique())
    apercu_options = st.multiselect('Filtrer par Aperçu', options=filtered_df['Aperçu'].unique())
    joueur_options = st.multiselect('Filtrer par Joueur', options=filtered_df['Nom'].unique())

    # Apply filters
    if position_options:
       filtered_df = filtered_df[filtered_df['Position'].isin(position_options)]
    if apercu_options:
       filtered_df = filtered_df[filtered_df['Aperçu'].isin(apercu_options)]
    if joueur_options:
       filtered_df = filtered_df[filtered_df['Nom'].isin(joueur_options)]

# Fonction pour convertir le DataFrame en fichier Excel en mémoire
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        processed_data = output.getvalue()
        return processed_data

# Créer un objet Excel en mémoire avec le DataFrame
    excel_file = to_excel(filtered_df)

# Créer le bouton de téléchargement
    st.download_button(label='📥 Télécharger la base de donnée',
                   data=excel_file,
                   file_name='database_scout.xlsx',
                   mime='application/vnd.ms-excel')


    st.write("Liste des joueurs")
    st.table(filtered_df.head(15))
   

    # Input pour la demande de l'utilisateur
    description = st.text_input('Décrivez ce que vous cherchez chez un joueur :')

    def analyser_requete(requete):
        doc = nlp(requete)
        mots_cles = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'ADJ']]
        return mots_cles

    def chercher_joueurs_par_description(description):
        mots_cles = analyser_requete(description)
        condition = '|'.join(mots_cles)  # Créer une regex pour chercher tous les mots-clés
        resultats = filtered_df[filtered_df['Commentaire'].str.contains(condition, case=False, na=False)]
        return resultats

    # Bouton pour lancer la recherche
    if st.button('Chercher') and description:
        resultats = chercher_joueurs_par_description(description)
    
        if not resultats.empty:
            st.write('Résultats trouvés :')
            st.table(resultats)
        else:
            st.write('Aucun résultat trouvé pour votre recherche.')

else:
    # Show login page if not logged in
    if show_login_page():
        # If the user has just logged in successfully, reload the page to display the app content
        st.experimental_rerun()
    else:
        st.info("Please log in to access the app.")