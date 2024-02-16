# natif
import os, math
# structure
import pandas as pd
import numpy as np
# utils
from .constants import Cols
# viz
import plotly.graph_objects as go
from bokeh.models import (
    BoxAnnotation,
    Label
)
from bokeh.plotting import (
    figure,
    save
)
from bokeh.io import export_png
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from mplsoccer import PyPizza


class PDFViz:

    # trop de variabilité dans les viz pour initialiser des reglages dans le constructeur (a refacto après premiers retours)
    def __init__(self) -> None:
        pass

    @staticmethod
    def plotly_moyenne_mobile_collective(df, date_train):
        
        date_train = pd.to_datetime(date_train, format = '%Y-%m-%d')
        df[Cols.SES3[1]] = pd.to_datetime(df[Cols.SES3[1]], format="%d.%m.%Y")
        df = df[df[Cols.SES3[1]] <= date_train]
        df = pd.DataFrame(df, index=df.set_index(df[Cols.SES3[1]],inplace = True))
        # groupement par jour et remplacement des NaN en 0 pour seance récup important dans les moyennes mobiles
        df = df.groupby([pd.Grouper(freq='D')]).mean()
        df = df.fillna(value=0.0)

        # création des moyennes mobile
        mm7 = df[Cols.GLOBALLOAD[1]].rolling(window=7).mean()
        #mm14 = df[Cols.GLOBALLOAD].rolling(window=14).mean()
        mm28 = df[Cols.GLOBALLOAD[1]].rolling(window=28).mean()

        # création des mm exponentiel et calibrage de l'alpha (= 2/N+1)
        ewma7 = df[Cols.GLOBALLOAD].ewm(alpha=0.25).mean() # non utilisé
        ewma28 = df[Cols.GLOBALLOAD].ewm(alpha=0.068).mean() # non utilisé

        # création des colonnes dans le dataframe
        df[Cols.GLOBALLOAD[1] + "mm7"] = mm7
        df[Cols.GLOBALLOAD[1] + "mm28"] = mm28
        acute_chronique = mm7/mm28

        # création des series
        df.index = df.index.astype(str)
        x = list(df.index)
        y = list(df[Cols.GLOBALLOAD[1] + "mm7"])
        y3 = list(df[Cols.GLOBALLOAD[1] + "mm28"])
        acute_chronique = list(acute_chronique)

        fig = go.Figure()

        # création des tracés
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            name="mm7",
            text=y,
            yaxis="y",
            marker_color='SpringGreen'))

        fig.add_trace(go.Scatter(
            x=x,
            y=y3,
            name="mm28",
            text=y3,
            yaxis="y",
            marker_color='OrangeRed'
        ))

        fig.add_trace(go.Scatter(
            x=x,
            y=acute_chronique,
            name="ratio A|C",
            text=acute_chronique,
            yaxis="y2",
            marker_color='Khaki'
        ))

        # création du style des tracé
        fig.update_traces(
            hoverinfo="name+x+text",
            line={"width": 1},
            mode="lines+markers",
            showlegend=True,
            marker_size=4
        )

        # Axes
        fig.update_layout(
            xaxis=dict(
                anchor="x",
                autorange=True,
                range=["2022-01-01 00:00:00.0000", "2022-12-31 00:00:00.0000"],
                type="date",
                showgrid=False,
                side='top'
            ),
            yaxis=dict(
                anchor="x",
                autorange=True,
                domain=[0.2, 1],
                linecolor="#ffffff",
                mirror=False,
                range=[min(y), max(y)],
                showline=True,
                side="left",
                tickfont={"color": "black"},
                tickmode="auto",
                ticks="",
                titlefont={"color": "black"},
                type="linear",
                zeroline=False
            ),
            yaxis2=dict(
                anchor="x",
                autorange=False,
                domain=[0, 0.2],
                linecolor="Khaki",
                mirror=False,
                range=[0, 2],
                showline=True,
                side="left",
                tickfont={"color": "black"},
                tickmode="auto",
                ticks="",
                titlefont={"color": "black"},
                type="linear",
                zeroline=False
            )
        )

        # mise à jour générale
        fig.update_layout(
            #dragmode="zoom",
            hovermode="x",
            legend=dict(traceorder="reversed"),
            width=1200,
            height=650,
            template="plotly_white",
            margin=dict(
                t=80,
                b=80
                ),
            )
        
        fig.write_image(os.getcwd() + "/application/design/images/mm_pdf.png")
    
    @staticmethod
    def bar_plot_indicateurs(df_indicateurs, df_obj_joueur):
        dict_color = {
            'Accumulated Acceleration Load':'steelblue',
            'Distance (m)':'forestgreen',
            'Distance (speed | High) (m)': 'gold',
            'PlayerLoad':'lavender'
        }

        df_indicateurs = df_indicateurs.set_index('Name')
        indicateurs = list(df_indicateurs.columns)

        for num, i in enumerate(indicateurs):
            joueurs_seance = list(df_indicateurs.index)
            indic = list(df_indicateurs[i])
            mean = np.mean(indic)
            mean_obj = np.mean(df_obj_joueur[i])
            diff = str(abs(round(mean - mean_obj, 2)))

            # init figure
            p = figure(x_range=joueurs_seance, y_range = (0,(max(indic)*1.35)), height=300, width = 450, title=f"{i}",toolbar_location = None)
            p.vbar(x=joueurs_seance, top=indic, width=0.9, fill_color = dict_color[i], line_color = dict_color[i])
            p.line(x=joueurs_seance, y = mean, width = 2, color = 'black', legend_label = 'Moyenne séance')
            p.line(x=joueurs_seance, y = mean_obj, width = 2, color = 'black', line_dash = 'dashed', legend_label = 'Moyenne objectifs')
            
            if mean > mean_obj:
                p.add_layout(BoxAnnotation(top=mean, bottom = mean_obj, fill_alpha=0.1, fill_color='red'))
            elif mean < mean_obj:
                p.add_layout(BoxAnnotation(bottom=mean, top = mean_obj, fill_alpha=0.1, fill_color='red'))

            label = Label(
                x=0.2, 
                y=(max(indic)*1.1), 
                text='Difference Moyenne Objectif : ' + diff,
                text_font_size = '8pt',
                render_mode='css',
                background_fill_color='white', 
                background_fill_alpha=0,
            )

            p.add_layout(label)
            p.legend.location = ('top_right')
            p.legend.label_text_font_size = '8pt'
            p.legend.background_fill_alpha = 0
            p.legend.border_line_alpha = 0
            p.xgrid.grid_line_color = None
            p.xaxis.major_label_orientation = math.pi/6
            p.xaxis.major_label_text_font_size = '6pt'
            
            export_png(p, filename=os.getcwd()+f"/application/design/images/{num}.png")
        
    @staticmethod
    def bar_plot_indicateurs_plt(df_indicateurs,df_obj_joueurs):
        dict_color = {
            'Accumulated Acceleration Load':'steelblue',
            'Distance (m)':'forestgreen',
            'Distance (speed | High) (m)': 'gold',
            'PlayerLoad':'lavender'
        }
        df_indicateurs = df_indicateurs.set_index('Name')
        indicateurs = list(df_indicateurs.columns)

        for num, i in enumerate(indicateurs):
            joueurs_seance = list(df_indicateurs.index)
            obj = list(df_obj_joueurs[i])
            indic = list(df_indicateurs[i])
            mean = np.mean(indic)
            mean_obj = np.mean(df_obj_joueurs[i])
            diff = str(abs(round(mean - mean_obj, 2)))
            fig, ax = plt.subplots(figsize = (12,8))
            ax.set_title(label =i, fontdict = {'fontsize' : 20})
            ax.bar(joueurs_seance,df_indicateurs[i], color = dict_color[i])
            plt.xticks(joueurs_seance, rotation = 45, size = 20, ha ='right', rotation_mode = 'anchor')
            plt.ylim(0,max(indic)*1.3)
            nb_joueurs = len(joueurs_seance)
            ax.plot([-1, nb_joueurs],[mean, mean], '--', lw =2, color = 'black', label = 'Moyenne Seance')
            ax.plot([-1, nb_joueurs], [mean_obj, mean_obj], 'k-', lw=2, label = 'Moyenne Objectif')
            ax.annotate('Difference Moyenne Objectif : ' + diff,(-1,max(indic)*1.2), size =20)
            if mean < mean_obj:
                ax.add_patch(Rectangle((-1,mean), width = len(joueurs_seance)+1, height = abs(mean-mean_obj), edgecolor ='r', facecolor = 'r', alpha = 0.05))
            else : 
                ax.add_patch(Rectangle((-1,mean_obj), width = len(joueurs_seance)+1, height = abs(mean-mean_obj), edgecolor ='r', facecolor = 'r', alpha = 0.05))

            plt.legend(loc = 'upper right', prop = {'size':15})
            plt.savefig(os.getcwd() +f"/application/design/images/{num}.png",bbox_inches='tight')

    @staticmethod    
    def bar_plot_indicateurs_plt_brut(df_indicateurs):
        dict_color = {
            'Accumulated Acceleration Load':'steelblue',
            'Distance (m)':'forestgreen',
            'Distance (speed | High) (m)': 'gold',
            'PlayerLoad':'lavender'
        }
        df_indicateurs = df_indicateurs.set_index('Name')
        indicateurs = list(df_indicateurs.columns)

        for num, i in enumerate(indicateurs):
            joueurs_seance = list(df_indicateurs.index)
            indic = df_indicateurs[i]
            mean = np.mean(indic)
            fig, ax = plt.subplots(figsize = (12,8))
            ax.set_title(label =i, fontdict = {'fontsize' : 20})
            ax.bar(joueurs_seance,df_indicateurs[i], color = dict_color[i])
            plt.xticks(joueurs_seance, rotation = 45, size = 20, ha ='right', rotation_mode = 'anchor')
            plt.ylim(0,max(indic)*1.3)
            nb_joueurs = len(joueurs_seance)
            ax.plot([-1, nb_joueurs],[mean, mean], '--', lw =2, color = 'black', label = 'Moyenne Seance')
            plt.legend(loc = 'upper right', prop = {'size':15})
            plt.savefig(os.getcwd() +f"/application/design/images/{num}.png",bbox_inches='tight')

    @staticmethod  
    def tableau_wellness_seance(df, date_du_jour):
        df_seance = df[df['Date'] == date_du_jour]
        return df_seance
    
    @staticmethod
    def bar_longitudinal_individuel(df, date_train):

        date_train = pd.to_datetime(date_train, format = '%Y-%m-%d')
        df[Cols.SES3[1]] = pd.to_datetime(df[Cols.SES3[1]], format="%d.%m.%Y")
        df = df[df[Cols.SES3[1]] <= date_train]
        df_date = df.loc[df[Cols.SES3[1]] == date_train]
        liste_joueur = df_date['Name'].unique()

        for i, joueur in enumerate(liste_joueur):
            df1 = df[df['Name'] == joueur]
            df1 = pd.DataFrame(df1, index=df1.set_index(df1['Session begin date (Local timezone)'].sort_values(),inplace = True))

            df2 = df1.groupby([pd.Grouper(freq='D')]).mean()
            df2 = df2.fillna(value=0.0)

            val = df2['PlayerLoad'][-60:]
            mm7 = val.rolling(window=7).mean()
            mm28 = val.rolling(window=28).mean()
            ac = round(mm7[-1]/mm28[-1],2)
            date = df2.index[-60:]
            if ac > 1.30 or ac < 0.80:
                color_ratio = 'Red'
            else:
                color_ratio = 'ForestGreen'


            fig, ax = plt.subplots(figsize = (12,8))
            ax.set_title(label= "Suivi longitudinal Player Load" + joueur, fontdict = {'fontsize' : 20})

            plt.xticks(date, rotation = 45, size = 20, ha ='right', rotation_mode = 'anchor')
            plt.ylim(0,20)
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
            ax.bar(date[18:], val[18:], color = "bisque")
            ax.plot(date[18:], mm7[18:], 'go--', color= "Magenta", linewidth=2, markersize=3)
            ax.plot(date[18:], mm28[18:], 'go--', color= "Darkblue", linewidth=2, markersize=3)

            if len(date) > 1:
                ax.annotate('Ratio A/C : ' + str(ac), (date[-12],18.5), size =20, color=color_ratio)
                ax.annotate('mm7', (date[18],18.5), size =20, color="Magenta")
                ax.annotate('mm28', (date[22],18.5), size =20, color="Darkblue")

            plt.title(label =f'{joueur} au {str(date_train)[0:11]}', fontdict = {'fontsize': 20})
            plt.savefig(f'fig_{i}.png', bbox_inches='tight')      

    @staticmethod
    def wellness_longitudinal_individuel(df, date_train):

        date_train = pd.to_datetime(date_train, format = '%Y-%m-%d')
        df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
        df = df[df['Date'] <= date_train]
        df_date = df.loc[df['Date'] == date_train]
        liste_joueur = df_date['Name'].unique()
        
        for i, joueur in enumerate(liste_joueur):

            df1 = df[df['Name'] == joueur]
            df1 = pd.DataFrame(df1, index=df1.set_index(df1['Date'].sort_values(),inplace = True))

            df2 = df1.groupby([pd.Grouper(freq='D')]).mean()
            df2 = df2.fillna(value=0.0)

            fatigue = df2['Fatigue'][-30:]
            sommeil = df2['Sommeil'][-30:]

            mm7_fatigue = fatigue.rolling(window=7).mean()
            mm7_sommeil = sommeil.rolling(window=7).mean()
            date = df2.index[-30:]

            fig, ax = plt.subplots(figsize = (12,8))
            ax.set_title(label= "Suivi longitudinal Wellness" + joueur, fontdict = {'fontsize' : 20})

            plt.xticks(date, rotation = 45, size = 20, ha ='right', rotation_mode = 'anchor')
            plt.ylim(0,10)

        
            ax.plot(date, mm7_fatigue, 'go--', color= "orangered", linewidth=2, markersize=3, label = mm7_fatigue)
            ax.plot(date, mm7_sommeil, 'go--', color= "springgreen", linewidth=2, markersize=3, label = mm7_sommeil)
            
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
            ax.annotate('Fatigue', (date[5],9.5), size =20, color="orangered")
            ax.annotate('Sommeil', (date[5],9), size =20, color="springgreen")

            plt.title(label =f'{joueur} au {str(date_train)[0:11]}', fontdict = {'fontsize': 20})
            plt.savefig(f'wellness_{i}.png', bbox_inches='tight')

        return liste_joueur
    
    @staticmethod
    def graphique_radar_alt_pdf(df, date):

        date_train = pd.to_datetime(date, format = '%Y-%m-%d')
        df[Cols.SES3[1]] = pd.to_datetime(df[Cols.SES3[1]], format="%d.%m.%Y")
        df_date = df.loc[df[Cols.SES3[1]] == date_train]
        liste_joueur = df_date['Name'].unique()
        liste_indic = ['PlayerLoad', 'Distance (m)', "Jumps", "Distance (speed | High) (m)", "Accelerations", "Decelerations"]

        for i, joueur in enumerate(liste_joueur):

            df1 = df_date[(df_date[Cols.NAME[1]] == joueur)]
            df2 = df[(df[Cols.NAME[1]] == joueur)]
            params = liste_indic
            df1 = df[params]
            df2 = df2[params]

            df2 = df2.max()
            df1 = round((df1 / df2 * 100), 2)
            df2 = round((df2 / df2 * 100), 2)
            liste_val = list(df1.iloc[0])
            legend = list(df1.columns)

            slice_colors = (
                ["#B2FBC6"] + ["#4E9963"] + ["#18A727"] + ["#C35F00"] + ["#FB4A08"] + ["#FDE18F"]
            )  # Couleurs des plot pizza
            text_colors = ["#000000"] * 6  # Couleur du texte
            min_range = [0, 0, 0, 0, 0, 0]  # Axe des paramètres min (0%)
            max_range = [100, 100, 100, 100, 100, 100]  # Axe des paramètres max (100%)

            # réglage généraux du graphique pizza
            baker = PyPizza(
                params=liste_indic,  # Paramètres à calculer (indicateurs)
                min_range=min_range,  # Valeurs minimales axe (0%)
                max_range=max_range,  # Valeurs maximales axe (100%)
                background_color="white",  # Couleur arrière plan général (gris très clair)
                straight_line_color="#EBEBE9",  # Couleur ligne entre les plots pizza
                last_circle_color="#000000",  # Couleur de la ligne du grand cercle
                last_circle_lw=0,  # Epaisseur ligne du dernier cercle (grand cercle)
                other_circle_lw=0,  # Graduation cercle du graphique (pas de graduation)
                other_circle_color="#000000",  # Couleurs des graduations
                straight_line_lw=0,  # Epaisseur ligne entre les plots pizza (pas de ligne)
            )

            # affichage et réglages des plots pizza
            fig, ax = baker.make_pizza(
                liste_val,
                figsize=(
                    3,
                    3,
                ),
                color_blank_space="same",  # Arrière plan transparent en dessous des plots pizza (idem que la couleur)
                blank_alpha=0.2,  # Niveau de transparence
                param_location=120,  # Localisation ou la valeur en carré va être ajouté
                slice_colors=slice_colors,  # Couleur des plots individuels (même nombre que d'indicateur, dans l'ordre)
                value_colors=text_colors,  # Couleur du texte des valeurs (même nombre que d'indicateur, dans l'ordre)
                value_bck_colors=slice_colors,  # Couleur d'arrière plan des valeurs affichée
                kwargs_slices=dict(  # Valeurs utilisé pour les slices
                    facecolor="#D1D2D2",
                    edgecolor="#000000",
                    zorder=1,
                    linewidth=1
                ),
                kwargs_compare=dict(  # Valeurs utilisées pour les plots pizza comparaison (2ème plot= values2)
                    facecolor="#373737",
                    edgecolor="#222222",
                    zorder=3,
                    linewidth=1,
                ),
                kwargs_params=dict(  # Valeurs utilisé pour les paramètres
                    color="#000000",
                    fontsize=10,
                    zorder=2,
                    va="center"
                ),
                kwargs_values=dict(  # Valeurs utilisé pour les valeurs des paramètres
                    color="#000000",
                    fontsize=8,
                    zorder=3,
                    bbox=dict(
                        edgecolor="#000000",
                        facecolor="#D1D2D2",
                        boxstyle="round,pad=0.2",
                        lw=1,
                    ),
                ),
                kwargs_compare_values=dict(  # Valeurs utilisé pour les valeurs des parametres de comparaison
                    color="#000000",
                    fontsize=8,
                    zorder=3,
                    bbox=dict(
                        edgecolor="#000000",
                        facecolor="#373737",
                        boxstyle="round,pad=0.2",
                        lw=1,
                    ),
                ),
            )
            fig.text(
            0.515, 1, f"{joueur}", size=12,
            ha="center", color="#000000"
            )
            plt.savefig(f'radar_{i}.png', bbox_inches='tight')