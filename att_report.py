from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from PIL import Image
import os

# initializing variables with values
fileName = 'sample.pdf'
documentTitle = 'sample'
title = 'Player Name | '
subTitle = 'Yverdon Sport - SFC (1)'
textLines = []
image_path = 'image.png'

# function to remove white background and draw image on pdf
def draw_transparent_image(image_path, x, y, width, height):
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

# creating a pdf object
pdf = canvas.Canvas(fileName, pagesize=landscape(A4))

# setting the title of the document
pdf.setTitle(documentTitle)

# set the background color to red
pdf.setFillColor(colors.firebrick)
pdf.rect(0,0,841,595, fill=1)

# setting the size of the page
pdf.setPageSize(landscape(A4))

# creating the title by setting its font
# and putting it on the canvas
pdf.setFont("Helvetica-Bold", 20)
pdf.setFillColor(colors.white)
pdf.drawString(45, 555, title)

# creating the subtitle by setting its font,
# colour and putting it on the canvas
pdf.setFont("Helvetica-Bold", 20)
pdf.drawString(200, 555, subTitle)

# drawing a line
pdf.setFillColor(colors.black)
pdf.rect(30, 535, 781, 2, fill=1)

# setting the rest of the background to white
pdf.setFillColor(colors.white)
pdf.rect(0,0,841,535, fill=1)

# creating a multiline text using
# textline and for loop
text = pdf.beginText(40, 500)
text.setFont("Helvetica", 18)
text.setFillColor(colors.black)
for line in textLines:
    text.textLine(line)
pdf.drawText(text)

# drawing images at the specified (x,y) positions
draw_transparent_image(image_path, 775, 500, width=60, height=100)
draw_transparent_image("1.png", 20, 210, width=200, height=320)
draw_transparent_image("2.png", 220, 210, width=200, height=320)
draw_transparent_image("3.png", 420, 250, width=225, height=200)
draw_transparent_image("4.png", 640, 210, width=200, height=320)
draw_transparent_image("5.png", 30, 30, width=320, height=160)
draw_transparent_image("6.png", 420, 30, width=180, height=180)
draw_transparent_image("7.png", 640, 18, width=200, height=200)
# saving the pdf
pdf.save()
