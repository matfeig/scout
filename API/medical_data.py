#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:56:37 2023

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
start_date = "2024-02-14"
end_date = "2024-02-14"
df= df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

#df= df[(df["Equipe"] == 'Pro')]

df= df[(df["Equipe"] != 'Pro')]
df = df.sort_values('Equipe')

#########################################
# Selecting only the specified columns
selected_columns = ['Equipe', 'Nom', 'Motif consultation', 'Localisation du soin', 'Niveau inquietude', 'Remarque']
df_selected = df[selected_columns]

df_selected  = df_selected.rename(columns={'Motif consultation': 'Motif'})
df_selected  = df_selected.rename(columns={'Localisation du soin': 'Localisation'})
df_selected  = df_selected.rename(columns={'Niveau inquietude': 'Niveau'})

df_selected['Niveau'] = df_selected['Niveau'].fillna(0)
df_selected['Niveau'] = df_selected['Niveau'].replace('',0)
df_selected['Niveau'] = pd.to_numeric(df_selected['Niveau'], errors='coerce')



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
    fig.text(0.5, 0.89, f"Daily Report | {end_date}", fontsize=12, weight='bold', ha='center', va='top')

    
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
        else:  # Data rows
            inquietude_col = df_selected.columns.get_loc('Niveau')
            inquietude_val = cell.get_text().get_text()
            if key[1] == inquietude_col:
                if inquietude_val == '1':
                    cell.set_facecolor('#ffffcc')  # yellow
                elif inquietude_val == '0':
                    cell.set_facecolor('white')  # orange
                elif inquietude_val == '2':
                    cell.set_facecolor('#ffcc99')  # orange
                elif inquietude_val == '3':
                    cell.set_facecolor('#ff6666')  # red
            else:
                cell.set_facecolor('#f1f1f2')
            cell.set_edgecolor('w')
            cell.set_height(0.08)

    # Save the page
    pdf.savefig(fig, bbox_inches='tight')

pdf_path


##############################################################################################################



# Convert 'Date' to datetime for easier filtering and filter the data for "Antunes"
df['Date'] = pd.to_datetime(df['Date'])
antunes_data = df[df['Nom'] == 'Antunes']

# Filter data for January
january_antunes = antunes_data[(antunes_data['Date'] >= '2024-01-01') & (antunes_data['Date'] <= '2024-01-31')]

# Correcting the creation of the date_motif_map dictionary
date_motif_map = {row['Date'].date(): row['Motif consultation'] for index, row in january_antunes.iterrows()}



# Revised function with enhanced visual design
def plot_calendar_circles_color(year, month, date_motif_map,game_days):
    # Define colors for the motifs (softer colors)
    colors = {'Soins': '#ffeb3b', 'Massage Recup': 'royalblue', 'Rehab': 'orange', 'Visite Médical': 'grey',
              'Blessure': 'red','Maladie': 'purple','Retour valide': 'green'
        
              
              }  # Light yellow and light blue
    background_color = '#f7f7f7'  # Soft background color for the calendar

    # Create a figure with daily subplots
    fig, axs = plt.subplots(7, 7, figsize=(14, 10), facecolor=background_color)

    # Days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Styling for days of the week
    for i, day in enumerate(days_of_week):
        axs[0, i].text(0.5, 0.5, day, ha='center', va='center', fontsize=12, fontweight='bold', color='#333333')
        axs[0, i].axis('off')

    # Hide all other axes initially
    for ax in axs[1:].flat:
        ax.axis('off')

    # Create a calendar month iterator
    cal = calendar.Calendar(firstweekday=0)
    month_days = list(cal.itermonthdays(year, month))
    start_day = datetime.date(year, month, 1).weekday()
    month_days = [0]*start_day + month_days
    
    last_day_of_month = max(month_days)  # Get the last day of the month


    # Design adjustments for the calendar days
    for day, ax in zip(month_days, axs[1:].flat):
        ax.axis('on')
        if day != 0 and day <= last_day_of_month:
            date_str = datetime.date(year, month, day)
            motif = date_motif_map.get(date_str, None)
            color = colors.get(motif, '#ffffff')  # White for days without specified consultations
            ax.add_patch(plt.Circle((0.5, 0.5), 0.25, color=color, edgecolor='#333333', linewidth=0.8))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 0.8)
            ax.text(0.5, 0.9, str(day), ha='center', va='center', fontsize=10, color='#333333')
            if date_str in game_days:
                ax.text(0.5, 0.1, "GAME DAY", ha='center', va='center', fontsize=10, color='Navy', fontweight='bold')
            ax.axis('off')
        else:
            ax.axis('off')  # Hide the subplot for days outside the month


    # Adding a legend for "Motif consultation"
    legend_patches = [mpatches.Patch(color=color, label=motif) for motif, color in colors.items()]
    plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5,-0.5), fancybox=True, shadow=True, ncol=2)

    plt.suptitle("Alexis Antunes | Janvier 2024", fontsize=16, fontweight='bold', color='#333333')
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    
    #Load the PNG image
    img = mpimg.imread(image_path)
# Create an inset_axes at the top right corner for the image
    ax_image = inset_axes(ax, width="100%", height="100%", loc='upper left', borderpad=1)
    ax_image.imshow(img)
    ax_image.axis('off')  # Hide axes of inset_axes
    
    
    plt.show()

# Plot the calendar for January 2024 with the revised function
game_days = [datetime.date(2024, 1, 23), datetime.date(2024, 1, 20),datetime.date(2024, 1, 27)]  # Example game days
plot_calendar_circles_color(2024, 1, date_motif_map, game_days)





