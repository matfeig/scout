# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 21:59:14 2020

@author: Feig
"""

import xml.etree.ElementTree as ET
import csv

#tree = ET.parse("D:/Documents/Stats/SFC/joueur_SFC_Zurich.xml")
tree = ET.parse("/Users/matfeig/Dropbox/SFC/Database/Dataevent/sfc_x.xml")
root = tree.getroot()

### Fichier joueur ###

#data = open('D:/Documents/Stats/SFC/joueur_sfc_zurich.csv','w', newline='')
data = open('/Users/matfeig/Dropbox/SFC/Database/Dataevent/sfc_x.csv','w', newline='')

csvwriter = csv.writer(data)
head = []

count = 0
for instance in range (len(root.findall('ALL_INSTANCES')[0])):
    instance_list = []
    label1 = []
    label2 = []
    label3 = []
    if count == 0:
        ID = root.findall('ALL_INSTANCES')[0][instance].find('ID').tag
        head.append(ID)
        start = root.findall('ALL_INSTANCES')[0][instance].find('start').tag
        head.append(start)
        end = root.findall('ALL_INSTANCES')[0][instance].find('end').tag
        head.append(end)
        code = root.findall('ALL_INSTANCES')[0][instance].find('code').tag
        head.append(code)
        label_1 = root.findall('ALL_INSTANCES')[0][instance][4].tag
        head.append('Team')
        label_2 = root.findall('ALL_INSTANCES')[0][instance][5].tag
        head.append('Action')
        label_3 = root.findall('ALL_INSTANCES')[0][instance][6].tag
        head.append('Half')
        x = root.findall('ALL_INSTANCES')[0][instance].find('pos_x').tag
        head.append(x)
        y = root.findall('ALL_INSTANCES')[0][instance].find('pos_y').tag
        head.append(y)  
        csvwriter.writerow(head)
        count = count + 1
    ID = root.findall('ALL_INSTANCES')[0][instance].find('ID').text
    instance_list.append(ID)
    start = root.findall('ALL_INSTANCES')[0][instance].find('start').text
    instance_list.append(start)
    end = root.findall('ALL_INSTANCES')[0][instance].find('end').text
    instance_list.append(end)
    code = root.findall('ALL_INSTANCES')[0][instance].find('code').text
    instance_list.append(code)
    if len(root.findall('ALL_INSTANCES')[0][instance])>4:
        group = root.findall('ALL_INSTANCES')[0][instance][4][0].text
        texte = root.findall('ALL_INSTANCES')[0][instance][4][1].text
        instance_list.append(str(texte))
    
        group = root.findall('ALL_INSTANCES')[0][instance][5][0].text
        texte = root.findall('ALL_INSTANCES')[0][instance][5][1].text
        instance_list.append(str(texte))
    
        group = root.findall('ALL_INSTANCES')[0][instance][6][0].text
        texte = root.findall('ALL_INSTANCES')[0][instance][6][1].text
        instance_list.append(str(texte))
    
        x = root.findall('ALL_INSTANCES')[0][instance].find('pos_x').text
        instance_list.append(x)
        y = root.findall('ALL_INSTANCES')[0][instance].find('pos_y').text
        instance_list.append(y)
    csvwriter.writerow(instance_list)
    
data.close()


#### Fichier équipe ###
#
#tree = ET.parse("C:/Users/monte/Desktop/Documents/Stats/SFC/equipe_SFC_Zurich.xml")
#root = tree.getroot()
#
#data = open('C:/Users/monte/Desktop/Documents/Stats/SFC/equipe_sfc_zurich.csv', 'w', newline='')
#
#csvwriter = csv.writer(data)
#head = []
#
#count = 0
#for instance in range (len(root.findall('ALL_INSTANCES')[0])):
#    instance_list = []
#    if count == 0:
#        ID = root.findall('ALL_INSTANCES')[0][instance].find('ID').tag
#        head.append(ID)
#        start = root.findall('ALL_INSTANCES')[0][instance].find('start').tag
#        head.append(start)
#        end = root.findall('ALL_INSTANCES')[0][instance].find('end').tag
#        head.append(end)
#        code = root.findall('ALL_INSTANCES')[0][instance].find('code').tag
#        head.append(code)
#          
#        csvwriter.writerow(head)
#        count = count + 1
#    ID = root.findall('ALL_INSTANCES')[0][instance].find('ID').text
#    instance_list.append(ID)
#    start = root.findall('ALL_INSTANCES')[0][instance].find('start').text
#    instance_list.append(start)
#    end = root.findall('ALL_INSTANCES')[0][instance].find('end').text
#    instance_list.append(end)
#    code = root.findall('ALL_INSTANCES')[0][instance].find('code').text
#    instance_list.append(code)
#
#    csvwriter.writerow(instance_list)
#    
#data.close()
