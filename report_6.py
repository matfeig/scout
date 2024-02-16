#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 10:43:45 2023

@author: matfeig
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.colors import Color
import os

#Variables
variables = ['pic', 'balltouch', 'event', 'obv', 'pressure', 'def', 'waffle']
players = ["Gaël Ondoua"]


# players = ["Alexandre Dias Patrício",
        
#           ]



team_1 = df2['team_name'].iloc[1]  # Adjust depending on df2's structure
team_2 = df2['team_name'].iloc[2]  # Adjust depending on df2's structure


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
        (735, 475, 80, 120),  # pic
        (20, 210, 200, 320), # balltouch
        (220, 210, 200, 320), # event
        (20, 20, 390, 190), # obv
        (640, 160, 200, 320), # pressure
        (420, 210, 210, 320),  # shot
        (415, 25, 230, 190)   # waffle
    ]
    return coordinates[idx]


# Loop through players and variables
for player in players:
    # Initialize a PDF for each player
    fileName = f'{player.replace(" ", "_")}.pdf'
    documentTitle = f'Report for {player} | {team_1} vs {team_2}'
    pdf = canvas.Canvas(fileName, pagesize=landscape(A4))
    pdf.setTitle(documentTitle)
    
    pdf.setFillColor(colors.white)
    pdf.rect(0,0,841,595,stroke=0, fill=1)
    pdf.setFillColor(colors.firebrick)
    pdf.rect(0,540,780,55,stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(colors.white)
    pdf.drawString(45, 562, f"{player} | {team_1} vs {team_2} (2)")   
    
    # # Retrieve player metrics from df2
    # player_data = df2[df2['player_name'] == player]
    # match_minutes = player_data['player_match_minutes'].sum()  # Adjust if different calculation needed
    # match_goals = player_data['player_match_goals'].sum()  # Adjust if different calculation needed
    # match_assists = player_data['player_match_assists'].sum()  # Adjust if different calculation needed

    # # Inserting metrics into the PDF as text
    # pdf.setFont("Helvetica", 12)
    # pdf.setFillColor(colors.white)
    
    # pdf.drawString(100, 500, f"Total Match Minutes: {match_minutes}")
    # pdf.drawString(100, 480, f"Total Match Goals: {match_goals}")
    # pdf.drawString(100, 460, f"Total Match Assists: {match_assists}")
        
    
    # Add a semi-transparent logo as the background
    draw_transparent_image(pdf, "servette.png", x=0, y=20, width=841, height=520)
    
    # Loop through variables
    
    # Loop through variables
    for idx, variable in enumerate(variables):
        # Construct file path
        image_path = f"{variable}_{player}.png"
        
        # Check if image exists
        if os.path.exists(image_path):
            # Define x, y, width, and height dynamically or set predefined layout for each variable
            x, y, width, height = get_image_coordinates(idx)  # Define this function according to your layout
            draw_transparent_image(pdf, image_path, x, y, width, height)
        else:
            print(f"Image not found: {image_path}")
            
      
    
    # Save the PDF
    pdf.save()
