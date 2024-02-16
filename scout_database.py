#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:08:17 2024

@author: matfeig
"""
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

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


chemin = '/Users/matfeig/Library/CloudStorage/Dropbox/SFC/Database/recrutement/database.csv'  # Pour Windows
df.to_csv(chemin, index=False)  # `index=False` pour ne pas inclure l'index du DataFrame dans le fichier CSV