#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 12:53:10 2023

@author: matfeig
"""
from fpdf import FPDF

# File paths
files = [
    "/Users/matfeig/Desktop/Figure 2023-08-17 111557 (1).png",
    "/Users/matfeig/Desktop/Figure 2023-08-17 111557 (8).png",
    "/Users/matfeig/Desktop/Figure 2023-08-17 111557 (15).png",
    "/Users/matfeig/Desktop/Figure 2023-08-17 111557 (22).png",
    "/Users/matfeig/Desktop/Figure 2023-08-17 111557 (29).png",
    "/Users/matfeig/Desktop/Figure 2023-08-17 111557 (36).png",
    "/Users/matfeig/Desktop/Figure 2023-08-17 111557 (41).png",
    "/Users/matfeig/Desktop/SFC_Kutesa_00899.png"
]

pdf = FPDF()

# Add each image to the PDF
for file in files:
    pdf.add_page()
    pdf.image(file, x = 10, y = 20, w = 190)  # Adjusting the size and position to fit the page

# Save the PDF to a file
pdf_output = "/Users/matfeig/Desktop/report.pdf"
pdf.output(pdf_output)

pdf_output
