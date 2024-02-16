#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 16:11:50 2023

@author: matfeig
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.colors import Color
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#Variables

df = pd.read_excel("/Users/matfeig/Library/CloudStorage/OneDrive-GENEVESPORTSA/Contingent/sfc_contingent.xlsx")

####Clean Data####
################Oui # Standardize the date format to 'YYYY-MM-DD'
df['Date naissance'] = pd.to_datetime(df['Date naissance']).dt.date
# Calculate the age of each individual
current_year = datetime.now().year
df['Age'] = current_year - df['Date naissance'].apply(lambda x: x.year)
# Display the updated dataframe with the new age column
df[['Nom', 'Prenom', 'Date naissance', 'Age']].head()


# Filtering the dataframe for 'Potentiel' = 3
players_df = df[df['Potentiel'] == 3]
players_df = players_df[players_df['Equipe'] == "Pro"]


variables = ['pic','trans']

# Function to draw transparent image
def draw_transparent_image(pdf, image_path, x, y, width, height):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img_transparent_path = os.path.splitext(image_path)[0] + '_transparent.png'
    img.save(img_transparent_path)
    pdf.drawImage(img_transparent_path, x, y, width=width, height=height, mask="auto")


# Coordinates for image placement
def get_image_coordinates(idx):
    coordinates = [
        (735, 475, 80, 120),
        (700, 200, 120, 80),# pic

    ]
    return coordinates[idx]    


# Loop through players and variables
#for player in players:
    
for index, player_row in players_df.iterrows():
    player_name = player_row['Nom']
    player_first_name = player_row['Prenom']
    player_number = int(player_row['Maillot'])  # This gets the player's number   
    player_equipe = player_row['Equipe']  # Assuming this is the correct column name for "Contingent"
    player_profil = player_row['Profil']  # Assuming this is the correct column name for "Profil de joueur"
    player_class = player_row['Class']  # Assuming this is the correct column name for "Joueur référence"
    player_type = player_row['Type']
    
    # Initialize a PDF for each player
    fileName = f'{player_name.replace(" ", "_")}.pdf'
    documentTitle = f'Report for {player_name}'
    pdf = canvas.Canvas(fileName, pagesize=landscape(A4))
    pdf.setTitle(documentTitle)
    
    pdf.setFillColor(colors.white)
    pdf.rect(0,0,841,595,stroke=0, fill=1)
   
    pdf.setFillColorRGB(0.52734375,0.0546875,0.1484375)
    #pdf.setFillColor(colors.firebrick)
    pdf.rect(0,530,780,65,stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(colors.white)
    pdf.drawString(50, 550, f" #{player_number}. {player_first_name} {player_name} - Quartile 4 - 2023")
    
   
################################################################################################################ 
    
    pdf.setFillColor(colors.gray)
    pdf.rect(20,450, 120,50,stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColor(colors.white)
    pdf.drawString(45, 477, "Robustes")
    pdf.drawString(44, 463, "& Puissant")
    
    pdf.setFillColor(colors.gray)
    pdf.rect(18,400, 28,25,stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(21, 427, "Resistant")

    pdf.setFillColor(colors.gray)
    pdf.rect(50,400, 28,25,stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(56, 427, "Dispo.")    
    
    pdf.setFillColor(colors.gray)
    pdf.rect(82,400, 28,25,stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(90, 427, "BF%")  
    
    pdf.setFillColor(colors.gray)
    pdf.rect(114,400, 28,25,stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(119, 427, "Blessure")  
    
    ##################################################################
    
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.rect(160,450, 120,50,stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.drawString(195, 477, "Strong")
    pdf.drawString(190, 463, "Personality")
    
    pdf.setFillColor(colors.gray)
    pdf.rect(160,400, 28,25, stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(163, 427, "Leader")  # Replace with actual detail name
   
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(192,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(195, 427, "Focus")  # Replace with actual detail name
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(224,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(227, 427, "Resilience")  # Replace with actual detail name
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(256,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(257, 427, "Achievement")  # Replace with actual detail name
    
##################################################################################
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.rect(300,450, 120,50,stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.drawString(313, 475, "Technique")
    pdf.drawString(310, 460, "sous pression")

    pdf.setFillColor(colors.gray)
    pdf.rect(300,400, 28,25, stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(302, 427, "Controle")  # Replace with actual detail name
   
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(330,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(332, 427, "Execution")  # Replace with actual detail name

    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(360,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(362, 427, "Menace")  # Replace with actual detail name
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(390,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(392, 427, "Defensif")  # Replace with actual detail name

   

##################################################################################    
 
 
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.rect(440,450, 120,50,stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.drawString(450, 475, "Intensité Mentale")
    pdf.drawString(454, 460, "& Physique")
      
    pdf.setFillColor(colors.gray)
    pdf.rect(300,400, 28,25, stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(302, 427, "Vitesse")  # Replace with actual detail name
   
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(330,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(332, 427, "explosivite")  # Replace with actual detail name

    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(360,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(362, 427, "Fast learner")  # Replace with actual detail name
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(390,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(392, 427, "Engagement")  # Replace with actual detail name

    ################################################################################################## 
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.rect(580,450,120,50,stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.drawString(590, 475, "Compréhension")
    pdf.drawString(595, 460, "du jeu")
    
    pdf.setFillColor(colors.gray)
    pdf.rect(300,400, 28,25, stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(colors.black)
    pdf.drawString(302, 427, "Intention")  # Replace with actual detail name
   
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(330,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(332, 427, "Positionnement")  # Replace with actual detail name

    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(360,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(362, 427, "Decision")  # Replace with actual detail name
    
    pdf.setFillColor(colors.gray)
    pdf.setFont("Helvetica-Bold", 6)
    pdf.rect(390,400, 28,25, stroke=0, fill=1)
    pdf.setFillColor(colors.black)
    pdf.drawString(392, 427, "Defensif")  # Replace with actual detail name
    
    #####################################################################################################
    
    
    # Set the fill color to black for the new text
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 9)
    
    # Position for the upper right corner text
    right_margin = 730
    upper_margin = 574  # Adjust the margin as needed
    
    # Draw the strings in the upper right corner
    pdf.drawString(right_margin - pdf.stringWidth(f"Contingent: {player_equipe}"), upper_margin, f"Contingent: {player_equipe}")
    pdf.drawString(right_margin - pdf.stringWidth(f"Type de joueur: {player_type}"), upper_margin - 11, f"Type de joueur: {player_type}")
    pdf.drawString(right_margin - pdf.stringWidth(f"Profil de joueur: {player_profil}"), upper_margin - 22, f"Profil de joueur: {player_profil}")
    pdf.drawString(right_margin - pdf.stringWidth(f"Joueur référence: {player_class}"), upper_margin - 33, f"Joueur référence: {player_class}")
   
    # Coordinates just below the picture, adjust as necessary
    x_coord = 735
    y_coord = 450  # Start at a y-coordinate below the picture

    # Setting the fill color to black for the text
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 9)  # Set font to Helvetica-Bold size 12

    # Drawing each string below the picture, and moving up the y-coordinate after each
    pdf.drawString(x_coord, y_coord, f"Heure training: {player_row['Heure']}")
    y_coord -= 15  # Adjust the y-coordinate for the next line
    pdf.drawString(x_coord, y_coord, f"Minutes: {player_row['Minutes']}")
    y_coord -= 15
    pdf.drawString(x_coord, y_coord, f"Match joués: {player_row['Match']}")
    y_coord -= 15
    pdf.drawString(x_coord, y_coord, f"Non convocation: {player_row['Match_injured']}")
    y_coord -= 15
    pdf.drawString(x_coord, y_coord, f"Suspension: {player_row['Suspendu']}")
    y_coord -= 15
    pdf.drawString(x_coord, y_coord, f"% availability: {player_row['Attendance']}%")
    y_coord -= 15
    pdf.drawString(x_coord, y_coord, f"nb jour blessé: {player_row['Day_injured']}")

   
   # Add a semi-transparent logo as the background
    draw_transparent_image(pdf, "servette.png", x=-65, y=518, width=180, height=90)
    
   # Loop through variables
    
    # Loop through variables
    for idx, variable in enumerate(variables):
        # Construct file path
        image_path = f"{variable}_{player_name}.png"
        
        # Check if image exists
        if os.path.exists(image_path):
            # Define x, y, width, and height dynamically or set predefined layout for each variable
            x, y, width, height = get_image_coordinates(idx)  # Define this function according to your layout
            draw_transparent_image(pdf, image_path, x, y, width, height)
        else:
            print(f"Image not found: {image_path}")
            
      
    # Save the PDF
    pdf.save()