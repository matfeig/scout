import os
import pandas as pd
import numpy as np
from fpdf import (
    XPos,
    YPos
)
from fpdf import FPDF
from .constants import (
    Cols,
    VariablesUtils
)
from .vizualisation_pdf import PDFViz


class PDF(FPDF):

    def __init__(self, orientation, unit, format, font_cache_dir,) -> None:
        super().__init__(orientation, unit, format, font_cache_dir)

    def header(self):
        self.image(name = os.getcwd() + "/application/design/images/logo.png", x= 18, y = 0.8, w = 1.5)
    
    def footer(self):
        self.set_y(-2.5)
        self.cell(w =0, h=0, border = True, new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.image(name = os.getcwd() + "/application/design/images/logo.png", x=1, y= 27.5, w= 1.5)
        self.set_font('helvetica','',10)
        self.cell(w=0, h=2.5, txt = 'SportDataLab', align = 'C')
        self.cell(w = 0, h=2.5, txt = f'Page {self.page_no()}/{{nb}}', align = 'R')
        self.cell(w =0, h=0, border = True)
    
    def texte_rapport_du_date(self, date):
        self.set_font('helvetica','B', 17)
        self.set_margins(left = 1, top = 1, right = 1)
        self.cell(w = 0, h =2, txt = 'Rapport du ' + str(date)[:10], new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.cell(w =0, h=0, border = True)
        self.ln(1)
    
    def texte_rapport_du_date_hebdo(self, date1, date2):
        self.set_font('helvetica','B', 17)
        self.set_margins(left = 1, top = 1, right = 1)
        self.cell(w = 0, h =2, txt = 'Rapport du ' + str(date1)[:10] + ' au ' + str(date2)[:10], new_x=XPos.LEFT, new_y=YPos.NEXT)
        self.cell(w =0, h=0, border = True)
        self.ln(1)

    def insert_df_page(self ,df):
        page_width = self.w - 2 * self.l_margin
        col_width = page_width/(df.shape[1])
        self.set_font(family='helvetica', style = 'B',size = 7)
        series = list(df.columns)
        for i in df.head(0):
            self.set_fill_color(217, 221, 223)
            self.cell(w=col_width, h=0.4, txt = i, align = 'C', border=True, fill=True)
        self.ln(0.4)
        for j in range(df.shape[0]):
            for i in range(df.shape[1]):
                self.cell(w=col_width, h=0.4, txt = str(df[series[i]][j]), align = 'C', border=True, fill=False)
            self.ln(0.4)
    
    def insert_df_page_objectif(self ,df):
        page_width = self.w - 2 * self.l_margin
        col_width = page_width/(df.shape[1])
        self.set_font(family='helvetica', style = 'B',size = 7)
        series = list(df.columns)

        for i in df.head(0):
            self.set_fill_color(217, 221, 223)
            self.cell(w=col_width, h=0.4, txt = i, align = 'C', border=True, fill=True)
        self.ln(0.4)
        
        for j in range(df.shape[0]):
            for i in range(df.shape[1]):
                try:
                    x = float(df[series[i]][j])
                    if x < 0.5:
                        self.set_fill_color(247, 149, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2) * 100)) + "%", border = True, fill=True, align ='C')
                    if x >= 0.5 and x <= 0.75:
                        self.set_fill_color(247, 230, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2) * 100)) + "%", border = True, fill=True, align ='C')
                    if x > 0.75:
                        self.set_fill_color(205, 247, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2) * 100)) +"%", border = True, fill=True, align ='C')

                except:
                    x = str(df[series[i]][j])
                    self.set_fill_color(255, 255, 255)
                    self.cell(w = col_width, h = 0.4, txt = x, border = True, fill=True)
                    
            self.ln(0.4)
    
    def insert_df_hebdo_somme_couleur_charge(self ,df):
        page_width = self.w - 2 * self.l_margin
        col_width = page_width/(df.shape[1])
        self.set_font(family='helvetica', style = 'B',size = 7)
        series = list(df.columns)

        for i in df.head(0):
            self.set_fill_color(217, 221, 223)
            self.cell(w=col_width, h=0.4, txt = i, align = 'C', border=True, fill=True)
        self.ln(0.4)
        
        for j in range(df.shape[0]):
            for i in range(df.shape[1]):
                try:
                    x = float(df[series[i]][j])
                    if x < np.mean(df[series[i]]):
                        self.set_fill_color(247, 149, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2))), border = True, fill=True, align ='C')
                    if x > np.mean(df[series[i]]) and x < max(df[series[i]]):
                        self.set_fill_color(247, 230, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2))), border = True, fill=True, align ='C')
                    if x >= max(df[series[i]]):
                        self.set_fill_color(205, 247, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2))), border = True, fill=True, align ='C')

                except:
                    x = str(df[series[i]][j])
                    self.set_fill_color(255, 255, 255)
                    self.cell(w = col_width, h = 0.4, txt = x, border = True, fill=True)
                    
            self.ln(0.4)


    def insert_df_wellness(self, df):
        page_width = self.w - 2 * self.l_margin
        col_width = page_width/(df.shape[1])
        self.set_font(family='helvetica', style = 'B',size = 7)
        series = list(df.columns[1:])

        for i in df[series].head(0):
            self.set_fill_color(217, 221, 223)
            self.cell(w=col_width, h=0.4, txt = i, align = 'C', border=True, fill=True)
        self.ln(0.4)

        for i in range(df[series].shape[0]):
            for j in range(df[series].shape[1]):
                try:
                    x = float(df[series].iloc[i,j])
                    if x >= 7:
                        self.set_fill_color(247, 149, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2))), border = True, fill=True, align ='C')
                    if x > 4 and x < 7:
                        self.set_fill_color(247, 230, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2))), border = True, fill=True, align ='C')
                    if x <= 4:
                        self.set_fill_color(205, 247, 149)
                        self.cell(w = col_width, h = 0.4, txt = str(int(round(x,2))), border = True, fill=True, align ='C')

                except:
                    x = str(df[series].iloc[i,j])
                    self.set_fill_color(255, 255, 255)
                    self.cell(w = col_width, h = 0.4, txt = x, border = True, fill=True)
                    
            self.ln(0.4)

        self.ln(0.4)
        self.set_font(family='helvetica', style = 'B', size = 16)
        self.ln(1)
        self.cell(w=0,h = 0.5, txt = "!! Alertes Wellness !!", align = 'L',new_x=XPos.LEFT, new_y=YPos.NEXT)

        cols_alerte = ['Name', 'Fatigue', 'Douleurs', 'Sommeil' ]
        alerte = []
        for i in range(df[cols_alerte].shape[0]):
            if float(df[cols_alerte].iloc[i,1]) >= 7 and float(df[cols_alerte].iloc[i,2]) >= 4 and float(df[cols_alerte].iloc[i,3]) >= 7:
                alerte.append(df[cols_alerte].iloc[i,0])

        self.ln(0.2)
        self.set_font(family='helvetica', style = 'B',size = 10)

        
        self.ln(1)
        for i in alerte[:4]:
            self.cell(w=5,h = 0.5, txt = i, align = 'L')
        self.ln(1)
        for i in alerte[4:8]:
            self.cell(w=5,h = 0.5, txt = i, align = 'L')
        self.ln(1)
        for i in alerte[8:12]:
            self.cell(w=5,h = 0.5, txt = i, align = 'L')
        self.ln(1)
        for i in alerte[12:16]:
            self.cell(w=5,h = 0.5, txt = i, align = 'L')
    
    @staticmethod
    def df_rapport_seance(database, train_day, last_match, monitoring):
        train_day = pd.to_datetime(train_day,format = '%Y-%m-%d')
        last_match = pd.to_datetime(last_match,format = '%Y-%m-%d')
        database[Cols.SES3[1]] = pd.to_datetime(database[Cols.SES3[1]], format = '%d.%m.%Y')

        delta = train_day - last_match
        if int(str(delta)[0]) < 5:
            delta = 'J+' + str(delta)[0]
        elif int(str(delta)[0]) >=5:
            delta = 'J-' + str((7-int(str(delta)[0])))


        df_date = database.loc[database[Cols.SES3[1]] == train_day]

        indicateurs = list(monitoring['Indicateurs'].unique())
        indicateurs.sort()

        df_indicateurs = df_date[indicateurs]
        df_indicateurs['Name'] = df_date['Name']

        df_indicateurs = df_indicateurs.set_index('Name')

        monitoring = monitoring[['Name','Indicateurs',delta]]
        monitoring = monitoring.sort_values('Indicateurs')

        list_obj = monitoring.groupby(['Name'])[delta].apply(list)
        list_obj

        joueurs_seance = df_indicateurs.index

        list_obj = list_obj[joueurs_seance]

        df_obj_joueur = pd.DataFrame(columns = indicateurs)
        for i in joueurs_seance:
            df_obj_joueur.loc[len(df_obj_joueur)] = list_obj[i]

        df_obj_joueur['Name'] = joueurs_seance
        df_obj_joueur = df_obj_joueur.set_index('Name')

        df_percent_obj = df_indicateurs / df_obj_joueur
        df_indicateurs = df_indicateurs.reset_index()
        df_percent_obj = df_percent_obj.reset_index()
        return (df_indicateurs, df_percent_obj, df_obj_joueur)

    @staticmethod
    def df_rapport_donnees_brut(database, train_day):

        train_day = pd.to_datetime(train_day,format = '%Y-%m-%d')
        database[Cols.SES3[1]] = pd.to_datetime(database[Cols.SES3[1]], format = '%d.%m.%Y')
        df_date = database.loc[database[Cols.SES3[1]] == train_day]

        indicateurs = VariablesUtils.INDICATEURS
        indicateurs.sort()

        df_indicateurs = df_date[indicateurs]
        df_indicateurs['Name'] = df_date['Name']

        df_indicateurs = df_indicateurs.set_index('Name')
        df_indicateurs = df_indicateurs.reset_index()

        return (df_indicateurs)
    
    @staticmethod
    def df_rapport_donnees_brut_hebdomadaire(database, debut_semaine, fin_semaine):

        debut_semaine = pd.to_datetime(debut_semaine,format = '%Y-%m-%d')
        fin_semaine = pd.to_datetime(fin_semaine,format = '%Y-%m-%d')
        database[Cols.SES3[1]] = pd.to_datetime(database[Cols.SES3[1]], format = '%d.%m.%Y')
        df_date = database[database[Cols.SES3[1]] >= debut_semaine]
        df_date = df_date[df_date[Cols.SES3[1]] <= fin_semaine]

        indicateurs = VariablesUtils.INDICATEURS
        indicateurs.sort()

        df_indicateurs = df_date[indicateurs]
        df_indicateurs['Name'] = df_date['Name']

        df_hebdo = df_indicateurs.groupby('Name').sum().reset_index()

        return df_hebdo.round(2)
