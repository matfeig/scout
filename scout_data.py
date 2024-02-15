#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:06:43 2024

@author: matfeig
"""
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import matplotlib.pyplot as plt
from itertools import product
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import table
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.colors import Color
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.pyplot as plt
import calendar
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import calendar
import datetime
import pandas as pd
from matplotlib.patches import Wedge
import streamlit as st
import pandas as pd


# Chemin vers votre fichier JSON
SERVICE_ACCOUNT_FILE = '/Users/matfeig/Desktop/scoutdata-414316-46c71767cc99.json'

# Scopes requis par l'API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# ID de votre Google Sheet
SPREADSHEET_ID = '1dWg4c2nY_N4lwffI2aRtrQA4d59t41RiPc5pPjaitV0'

# Authentification
creds = None
creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Construire le serviPoce
service = build('sheets', 'v4', credentials=creds)

# Lire les données
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range="Feuille 1").execute()
values = result.get('values', [])

# Convertir en DataFrame
df = pd.DataFrame(values)
df.columns = df.iloc[0] # Définir la première ligne comme en-tête
df = df[1:] # Prendre les données en excluant l'en-tête

# Afficher le DataFrame
print(df)

# chemin = '/Users/matfeig/Desktop/df.csv'  # Pour Windows
# df.to_csv(chemin, index=False)  # `index=False` pour ne pas inclure l'index du DataFrame dans le fichier CSV

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

#df_selected.to_csv('file_name.csv')


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
