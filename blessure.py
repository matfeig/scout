#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:05:26 2024

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
from datetime import datetime


# Chemin vers votre fichier JSON
SERVICE_ACCOUNT_FILE = '/Users/matfeig/Desktop/medicaldata-406809-658cb2c8ddb4.json'

# Scopes requis par l'API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# ID de votre Google Sheet
SPREADSHEET_ID = '1pN_xz-oX4GZ6rN1-fo8cWliqjrfgJY0-lXmkTHz17Do'

# Authentification
creds = None
creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Construire le service
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

# Filter the dataframe based on the provided date range
start_date = "2024-01-0A"
end_date = "2024-02-14"
df= df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

#df= df[(df["Equipe"] == 'Pro')]

df= df[(df["Equipe"] != 'Pro')]
df = df.sort_values('Equipe')
df= df[(df["Motif consultation"] == 'Blessure')]

#########################################

# Selecting only the specified columns
selected_columns = ['Equipe', 'Nom', 'Arret', 'Type de journee', 'Contexte de blessure', 'Localisation', 'Recidive 60 jours', 'Mecanisme','Remarque']
df_selected = df[selected_columns]

df_selected  = df_selected.rename(columns={'Type de journee': 'Jour'})
df_selected  = df_selected.rename(columns={'Contexte de blessure': 'Contact'})
df_selected  = df_selected.rename(columns={'Recidive 60 jours': 'Recidive'})

# Constants for A4 size in inches (width, height)
A4_SIZE = (8.27,11.69 )


current_date = end_date
pdf_path = f'/Users/matfeig/Desktop/{current_date}_daily.pdf'
image_path = '/Users/matfeig/Documents/SFC/rapport/Servettelogo.png'

with PdfPages(pdf_path) as pdf:
    # Initialize a matplotlib figure with A4 size
    fig, ax = plt.subplots(figsize=A4_SIZE)
    ax.axis('off')  # Hide axes
    
    #report_date = "2024-01-17" 
   # Set the title with more control
    fig.text(0.5, 0.89, f"Rapport de Blessure | {end_date}", fontsize=12, weight='bold', ha='center', va='top')

    
    #Load the PNG image
    img = mpimg.imread(image_path)
# Create an inset_axes at the top right corner for the image
    ax_image = inset_axes(ax, width="10%", height="10%", loc='lower center', borderpad=1)
    ax_image.imshow(img)
    ax_image.axis('off')  # Hide axes of inset_axes

    # Define custom column widths
    col_widths = [0.05 if col in ['Equipe'] else 0.11 if col in ['Remarque', 'Localisation'] else 0.8 for col in df_selected.columns]

    # Create the table and add it to the figure
    table_data = ax.table(cellText=df_selected.values, colLabels=df_selected.columns, loc='upper center', cellLoc='center', colWidths=col_widths)
    table_data.auto_set_font_size(False)
    table_data.set_fontsize(8)
    table_data.scale(1, 1)  # Adjust table size

# Style the table
    table_data.auto_set_column_width(col=list(range(len(df_selected.columns))))
    for key, cell in table_data.get_celld().items():
        if key[0] == 0:  # Header row
            cell.set_fontsize(10)
            cell.set_facecolor('#40466e')
            cell.set_text_props(weight='bold', color='w')
        else:
            cell.set_facecolor('#f1f1f2')
            cell.set_edgecolor('w')
            cell.set_height(0.08)

    # Save the page
    pdf.savefig(fig, bbox_inches='tight')

pdf_path
