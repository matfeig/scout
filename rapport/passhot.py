import pandas as pd
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
import matplotlib.patches as patches
import numpy as np
from mplsoccer.pitch import Pitch
import API

def getShotDF(df, team):
    list_df = []
    list_poss = []  # storing the possessions number to avoid to take the same shots multiple times
    for index, row in df.iterrows():
        if (row['possession'] in list_poss):
            continue
        if (row['type_name'] == 'Shot' and row['team_name'] == team):
            possession = row['possession']
            tmp_df = df.loc[
                (df['possession'] == possession) & (df['team_name'] == team) & (df['outcome_name'] != 'Incomplete')]
            list_poss.append(possession)
            list_df.append(tmp_df)
            print(list_poss)
    return list_df


def plotPassages(list_df_shots, shirt_color, nr_color,jersey_num):

    list_subdf = []
    i = 0
    for tmp_df in list_df_shots:
        ### Plotting ###
        df_shot = tmp_df
        df_shot['carry_length'] = np.sqrt(
            np.power((df['x'] - df['end_x']), 2) + np.power((df['y'] - df['end_y']),2))

        df_shot = df_shot.reset_index(drop=True)
        l = df_shot[(df_shot['sub_type_name'] == 'Recovery')].index.tolist()
        if (len(l) > 0):
            df_shot = df_shot[df_shot.index >= l[-1]]
        list_subdf.append(df_shot)
        l = df_shot[(df_shot['type_name'] == 'Ball Recovery')].index.tolist()
        if (len(l) > 0):
            df_shot = df_shot[df_shot.index >= l[-1]]
        df_shot = df_shot[(df_shot['type_name'] == "Pass") | (
                    (df_shot['type_name'] == "Carry") & (df_shot['carry_length'] > 3)) | (
                                      df_shot['type_name'] == "Shot")]

        last_line = df_shot.iloc[-1,:]
        last_event = last_line['type_name']

        if last_event == 'Shot' :

            pitch = Pitch(pitch_type='statsbomb', figsize=(8, 4))  # example plotting a sch
            fig, ax1 = pitch.draw()

            ax1.scatter(df_shot['x'], df_shot['y'], c=shirt_color, s=120, zorder=3)
            # ax1.set_facecolor('xkcd:green')

            df_shot = df_shot.reset_index(drop=True)

            for index, row in df_shot.iterrows():

                if (row['type_name'] == "Pass"):
                    if ((row['end_x'] == df_shot['x'].iloc[index + 1]) & (
                            row['end_y'] == df_shot['y'].iloc[index + 1])):
                        ax1.arrow(row['x'], row['y'], row['end_x'] - row['x'],
                                  row['end_y'] - row['y'], width=0.1, color="black", head_width=0.8)
                    else:
                        ax1.arrow(row['x'], row['y'],
                                  df_shot['x'].iloc[index + 1] - row['x'],
                                  df_shot['y'].iloc[index + 1] - row['y'], width=0.1, color="black",
                                  head_width=0.8)
                if (row['type_name'] == "Carry"):
                    if ((row['x'] == df_shot['x'].iloc[index + 1]) & (
                            row['end_y'] == df_shot['y'].iloc[index + 1])):
                        ax1.arrow(row['x'], row['y'], row['end_x'] - row['x'],
                                  row['end_y'] - row['y'], width=0.1, color="black", head_width=0.8,
                                  linestyle=":")
                    else:
                        ax1.arrow(row['x'], row['y'],
                                  df_shot['x'].iloc[index + 1] - row['x'],
                                  df_shot['y'].iloc[index + 1] - row['y'], width=0.1, color="black",
                                  head_width=0.8, linestyle=":")
                if (row['type_name'] == "Shot"):
                    ax1.arrow(row['x'], row['y'], row['end_x'] - row['x'],
                              row['end_y'] - row['y'], width=0.1, color="red", head_width=0.8,
                              linestyle=":")

                text = str(int(jersey_num[row['player_name']]))
                if (int(jersey_num[row['player_name']]) > 9):
                    ax1.annotate(text, (row['x'] - 1.8, row['y'] + 1.0), zorder=4, fontsize=8.5,
                                 color=nr_color, weight='bold')
                else:
                    ax1.annotate(text, (row['x'] - 1., row['y'] + 1.0), zorder=4, fontsize=8.5,
                                 color=nr_color, weight='bold')



            ax1.set_xlim(-1, 121)
            ax1.set_ylim(81, -1)
            # fig.savefig("Team_Shot_"+str(i)+'.pdf')
            i += 1

#### Servette ######

id = API.n_dernier_match(1,["Servette"])[0]
df = API.df_events(id)
df['type_name'] = df['type_name'].replace(np.nan, "")

list_df_shots = getShotDF(df, 'Servette')

jersey_num = {}
jersey_num['Jeremy Frick'] = '32'
jersey_num['Steven Deana'] = '1'
jersey_num['Edin Omeragic'] = '40'
jersey_num['Vincent Sasso'] = '23'
jersey_num['Vincent Julien Sasso'] = '23'
jersey_num['Nicolas Vouilloz'] = '33'
jersey_num['Steve Rouiller'] = '4'
jersey_num['Noah Henchoz'] = '30'
jersey_num['Diogo Monteiro'] = '35'
jersey_num['Roggerio Nyakossi'] = '34'
jersey_num['Yoan Severin'] = '19'
jersey_num['Gaël Clichy'] = '3'
jersey_num['Malik Sawadogo'] = '24'
jersey_num['Anthony Sauthier'] = '2'
jersey_num['Moussa Diallo'] = '7'
jersey_num['Nils Pedat'] = '21'
jersey_num['David Douline'] = '28'
jersey_num['Theo Valls'] = '15'
jersey_num['Timothé Cognat'] = '8'
jersey_num['Boris Cespedes'] = '5'
jersey_num['Ricardo Azevedo'] = '22'
jersey_num['Miroslav Stevanović'] = '9'
jersey_num['Kastriot Imeri'] = '17'
jersey_num['Alexis Antunes'] = '27'
jersey_num['Boubacar Fofana'] = '11'
jersey_num['Papu Mendes'] = '20'
jersey_num['Ronny Rodelin'] = '12'
jersey_num['Grejohn Kyei'] = '25'
jersey_num['Alex Schalk'] = '10'
jersey_num['Dimitri Joseph Oberlin Mfomo'] = '14'
jersey_num['Chris Vianney Bedia'] = '29'
jersey_num['Moritz Bauer'] = '26'

plotPassages(list_df_shots, "darkred", "white",jersey_num)


#### st. Gall ######

# id = API.n_dernier_match(1,["St. Gallen"])[0]
# df = API.df_events(id)
# df['type_name'] = df['type_name'].replace(np.nan, "")

# list_df_shots = getShotDF(df, 'St. Gallen')

# jersey_num = {}
# jersey_num['Alessio Besio'] = '31'
# jersey_num['Basil Stillhart'] = '6'
# jersey_num['Betim Fazliji'] = '23'
# jersey_num['Boris Babic'] = '34'
# jersey_num['Euclides Cabral'] = '2'
# jersey_num['Fabian Schubert'] = '33'
# jersey_num['Isaac Osa"s Schmidt'] = '4'
# jersey_num['Jeremy Bruno Guillemenot'] = '30'
# jersey_num['Kwadwo Duah'] = '35'
# jersey_num['Lawrence Ati-Zigi'] = '1'
# jersey_num['Leonidas Stergiou'] = '4'
# jersey_num['Lukas Görtler'] = '16'
# jersey_num['Michael Kempter'] = '24'
# jersey_num['Nicolas Lüchinger'] = '50'
# jersey_num['Ousmane Diakite'] = '8'
# jersey_num['Elie Youan'] = '20'
# jersey_num['Tim Staubli'] = '28'
# jersey_num['Víctor Ruiz Abril'] = '10'


# plotPassages(list_df_shots, "darkred", "white",jersey_num)



