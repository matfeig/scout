  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 10:44:31 2023

@author: matfeig
"""
from statsbombpy import sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
from highlight_text import fig_text
from mplsoccer import Pitch
from matplotlib.colors import TwoSlopeNorm

#use the same credentials that you use to login to IQ
user = "m.feigean@servettefc.ch"
password = "QzG3Kdlu"

# focus_team="Servette FC M-21" #choose the team that you want to analyse. the code will find their most recent fixture for this viz
# comp=1525
# season=281

focus_team="Servette" #choose the team that you want to analyse. the code will find their most recent fixture for this viz
comp=80
season=281

# focus_team="Servette" #choose the team that you want to analyse. the code will find their most recent fixture for this viz
# comp=35
# season=281

#set colours of your focus team, and opposition team, and other coloured areas on the data viz
bgcolor="white"
focus_color="#870E26"
oppo_color="grey"
bar_color="black"


#call the statsbomb API to get a list of games from the focus competition and season
matches = sb.matches(competition_id = comp, season_id = season,
                     creds={"user": user, "passwd": password})

#cut dataframe to get only games played by the focus team
matches = matches[(matches['home_team'] == focus_team)|(matches['away_team'] == focus_team)]
matches=matches.sort_values(by=['match_date'],ascending=False)
matches=matches[matches["match_status"]=="available"]

#identify the most recent game
list_matches=list(matches.match_id)
focus_match=list_matches[0]
#get match data for viz title
match_data=matches[matches["match_id"]==focus_match]
home_team=match_data.iloc[0]['home_team']
away_team=match_data.iloc[0]['away_team']
home_score=int(match_data.iloc[0]['home_score'])
away_score=int(match_data.iloc[0]['away_score'])
match_date=match_data.iloc[0]['match_date']

#get data for the game in focus
focus_df=sb.events(match_id = focus_match,
                             creds={"user": user, "passwd": password})

#identify the name of th eopposition
opposition=list(focus_df.team.unique())
opposition.remove(focus_team)
opposition=opposition[0]

#############################################################################################################################
#define function for calculating and plotting possession and OBV flow

def game_flow(data, period, ax):
    
    df = data[data["period"]==period].reset_index(drop=True)
    df = df.sort_values(by=['minute', 'second'])
    
    grouped_min = []
    for i in range(round(df.minute.min()), round(df.minute.max()+1), 5):
        for index, row in df.iterrows():
            if i <= row["minute"] < i+5:
                grouped_min.append(i+5)
            else:
                pass
    df["grouped_min"] = grouped_min
    
    poss = df[df["type"]=="Pass"]
    teamposs = poss[(poss["pass_outcome"].isnull()) & (poss["team"]==focus_team)]
    oppoposs = poss[(poss["pass_outcome"].isnull()) & (poss["team"]==opposition)]
    
    teamPOSSlist = teamposs.groupby(['grouped_min']).size().reset_index()
    teamPOSSlist.rename(columns={teamPOSSlist.columns[1]: "team_poss" }, inplace=True)
    oppoPOSSlist = oppoposs.groupby(['grouped_min']).size().reset_index()
    oppoPOSSlist.rename(columns={oppoPOSSlist.columns[1]: "oppo_poss" }, inplace=True)
    
    matchposs = pd.merge(teamPOSSlist, oppoPOSSlist, how="outer", on=["grouped_min"])
    matchposs = matchposs.fillna(0)
    
    timelist = matchposs["grouped_min"].tolist()
    teamPOSSlist = matchposs["team_poss"].tolist()
    teamPOSSlist = gaussian_filter1d(teamPOSSlist, sigma=1)
    oppoPOSSlist = matchposs["oppo_poss"].tolist()
    oppoPOSSlist = gaussian_filter1d(oppoPOSSlist, sigma=1)
    poss_difflist = [teamPOSSlist[i] - oppoPOSSlist[i] for i in range(len(matchposs))]
    
    obv = df.dropna(subset=['obv_total_net'])
    obv = obv[(obv["type"]=="Pass") | (obv["type"]=="Carry") | (obv["type"]=="Dribble")]
    teamobv = obv[obv['team'] == focus_team]
    oppoobv = obv[obv['team'] == opposition]

    teamOBVlist = teamobv.groupby(['grouped_min']).agg({'obv_total_net': ['sum']})
    teamOBVlist.columns = teamOBVlist.columns.droplevel()
    teamOBVlist = teamOBVlist.reset_index()
    oppoOBVlist = oppoobv.groupby(['grouped_min']).agg({'obv_total_net': ['sum']})
    oppoOBVlist.columns = oppoOBVlist.columns.droplevel()
    oppoOBVlist = oppoOBVlist.reset_index()
    
    matchobv = pd.merge(teamOBVlist, oppoOBVlist, how="outer", on=["grouped_min"])
    matchobv = matchobv.fillna(0)
    
    timelistOBV = matchobv["grouped_min"].tolist()
    teamOBVlist = matchobv["sum_x"].tolist()
    teamOBVlist = gaussian_filter1d(teamOBVlist, sigma=1)
    oppoOBVlist = matchobv["sum_y"].tolist()
    oppoOBVlist = gaussian_filter1d(oppoOBVlist, sigma=1)
    
    OBV_diff = [teamOBVlist[i] - oppoOBVlist[i] for i in range(len(matchobv))]
    OBV_diff = [i * 50 for i in OBV_diff]
    
    team_goals = df[(df["team"]==focus_team) & (df["shot_outcome"]=="Goal") | ((df['type']=="Own Goal For") & (df['team'] == focus_team))]
    oppo_goals = df[(df["team"]==opposition) & (df["shot_outcome"]=="Goal") | ((df['type']=="Own Goal For") & (df['team'] == opposition))]
    
    ax.scatter('minute', range(len(team_goals)), data=team_goals, color=focus_color, ec="white", lw=3, hatch="///", marker='o', s=750, zorder=12, label=f"{focus_team} goals")
    oppo_end = (len(oppo_goals)) * -1
    ax.scatter('minute', range(oppo_end, 0), data=oppo_goals, color=oppo_color, ec="black", lw=3, hatch="///", marker='o', s=750, zorder=12, label=f"{opposition} goals")
    ax.set_facecolor('white')
    ax.plot(timelist, poss_difflist, 'lightgrey')
    y1positive = (np.asarray(poss_difflist) + 1e-7) > 0
    y1negative = (np.asarray(poss_difflist) - 1e-7) < 0
    ax.set_yticklabels([])
    ax.yaxis.label.set_color("black")
    ax.tick_params(axis='y', colors="black")
    ax.fill_between(timelist, poss_difflist, where=y1positive, color=focus_color, alpha=0.95, interpolate=True, label=f"{focus_team} possession")
    ax.fill_between(timelist, poss_difflist, where=y1negative, color=oppo_color, alpha=0.95, interpolate=True, label=f"{opposition} possession")
    ax.bar(timelistOBV, OBV_diff, width=3, color=bar_color, alpha=0.95, zorder=10, label="Danger")
    ax.grid(True, color="grey", lw=1)
    if ax == ax1:
        ax.legend(fontsize=16, bbox_to_anchor=[0.95, -0.02], ncol=3)
        ax.set_ylabel("1st mi-temps", fontsize=20, color="black")
    else:
        pass
    
    ax.set_ylim(-30, 30)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    return teamobv['obv_total_net'].sum()

fig = plt.figure(figsize=(25, 12))
fig.set_facecolor("white")
gs = fig.add_gridspec(nrows=1, ncols=2)

ax1 = fig.add_subplot(gs[0])
total_net_obv_1 = game_flow(focus_df, 1, ax1)

ax2 = fig.add_subplot(gs[1])
total_net_obv_2 = game_flow(focus_df, 2, ax2)

total_net_obv = total_net_obv_1 + total_net_obv_2

fig.text(0.5, 0.92, "Domination par la possession et par le danger", ha='center', fontsize=30, fontweight="bold", color="black")
#fig.text(0.5, 0.87, f'Menace pour SFC: {total_net_obv:.2f} | KPI: 2.54', ha='center', fontsize=26, backgroundcolor='0.85')
fig.text(0.5, 0.87, "Menace pour SFC: 2.8 | KPI: 2.54", ha='center', fontsize=26, backgroundcolor='0.85')
ax2.set_ylabel("2nd mi-temps", fontsize=20, color="black")


##########################################################################################################################################################################################
#XG
def plot_xG(data, team_name, oppo_name, focus_color, oppo_color):
    events_shots = data[data["type"] == "Shot"]
    events_shots_team = events_shots[events_shots["team"] == team_name]
    events_shots_oppo = events_shots[events_shots["team"] == oppo_name]

    min_team = [0]
    min_oppo = [0]
    xG_team = [0]
    xG_oppo = [0]

    for ind, row in events_shots_team.iterrows():
        min_val = row["minute"] + row["second"] / 60
        min_team.append(min_val)
        xG_team.append(row["shot_statsbomb_xg"] + xG_team[-1])

    for ind, row in events_shots_oppo.iterrows():
        min_val = row["minute"] + row["second"] / 60
        min_oppo.append(min_val)
        xG_oppo.append(row["shot_statsbomb_xg"] + xG_oppo[-1])

    # Adjust the lists so that the edges (min_team and min_oppo) are one element longer than the values (xG_team and xG_oppo).
    max_time = max(data["minute"].max() + data["second"].max() / 60, 90)
    min_team.append(max_time)
    min_oppo.append(max_time)
   
    fig = plt.figure()
    plt.style.use('fivethirtyeight')
    fig,ax = plt.subplots(figsize = (16,9))
    plt.rcParams['axes.facecolor'] = "white"
    plt.stairs(xG_team,min_team,baseline = None,fill=False,linewidth=5,label = team_name,color = focus_color)
    plt.stairs(xG_oppo,min_oppo,baseline = None, fill=False,linewidth=5,label = oppo_name,color = oppo_color)
    #plt.axvline(45, 0, 1,linewidth=2, color = "k")
    plt.axhline(y=1.69, xmin=0.05, xmax=50, linewidth=2, color = '#870E26', ls='--')
    fig_text(0.13,0.61,"Target occasion créée", color = "#870E26",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
    plt.axhline(y=1.07, xmin=0.05, xmax=60, linewidth=2, color = 'Grey', ls='--')
    fig_text(0.13,0.35,"Target occasion concédée", color = "Grey",fontweight = "bold", fontsize = 12,backgroundcolor='0.85')
    plt.ylim(-0.02,max(xG_oppo[-1],xG_team[-1]) + 0.5)
    plt.yticks([0,0.7,1.4,2.1,2.8])
    plt.xticks([0,15,30,45,60,75,90])
    fig_text(0.13,0.80, s="Mi-temps 1\n", fontsize = 12, fontweight = "bold", color = "black")
    fig_text(0.51,0.80, s="Mi-temps 2\n", fontsize = 12 , fontweight = "bold", color = "black")
    plt.text(min_team[-1] + 1,xG_team[-1],str(round(xG_team[-1],2)),color = focus_color)
    plt.text(min_oppo[-1] + 1,xG_oppo[-1],str(round(xG_oppo[-1],2)),color = oppo_color)
    plt.xlabel("Minute de Jeu",fontsize = 20, fontweight = "bold", color = "black", labelpad=15)
    plt.ylabel("Valeur de xG",fontsize = 20, fontweight = "bold", color = "black")
    #plt.title("Expected Goals",fontsize = 30, fontweight = "bold", color = "black", pad=30)
    fig.text(0.5, 0.92, "Expected Goals", ha='center', fontsize=30, fontweight="bold", color="black")
    fig.text(0.5, 0.87, f'xG SFC: {xG_oppo[-1]:.2f} | KPI: 1.69', ha='center', fontsize=24, backgroundcolor='0.85')
    plt.legend(frameon = True,loc = 'upper right')

home_team = matches.iloc[0]["home_team"]
away_team = matches.iloc[0]["away_team"]

if home_team == focus_team:
    plot_xG(focus_df, home_team, away_team, focus_color, oppo_color)
else:
    plot_xG(focus_df, home_team, away_team, oppo_color, focus_color)

##########################################################################################################################################################################################
#Touch Ratio

def extract_location_x(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[0]
    return np.nan  # Return NaN for invalid or missing data

def extract_location_y(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[1]
    return np.nan  # Return NaN for invalid or missing data

# Extract x and y coordinates from the 'location' column
focus_df['location_x'] = focus_df['location'].apply(extract_location_x)
focus_df['location_y'] = focus_df['location'].apply(extract_location_y)


def plot_possession_and_danger(data, focus_team, opposition, focus_color, oppo_color):
    # No need to extract x and y coordinates here as it's done outside of the function
    
    pitch = Pitch(line_zorder=2, line_color='black')

    # Use 'team' column instead of 'team_name'
    arg_touch = data.loc[(data["type"].isin(["Pass", "Ball Receipt*"])) & (data.team == focus_team)]
    pol_touch = data.loc[(data["type"].isin(["Pass", "Ball Receipt*"])) & (data.team == opposition)]

    arg_hist = pitch.bin_statistic(arg_touch.location_x, arg_touch.location_y, statistic='count', bins=(6, 5), normalize=False)
    pol_hist = pitch.bin_statistic(pol_touch.location_x, pol_touch.location_y, statistic='count', bins=(6, 5), normalize=False)
    pol_hist["statistic"] = np.flip(pol_hist["statistic"])

    arg_ratio = arg_hist["statistic"] / (arg_hist["statistic"] + pol_hist["statistic"])
    pol_ratio = pol_hist["statistic"] / (arg_hist["statistic"] + pol_hist["statistic"])

    divnorm = TwoSlopeNorm(vmin=0, vcenter=0.5, vmax=1)
    arg_hist["statistic"] = arg_ratio

    fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,endnote_height=0.04, title_space=0, endnote_space=0)  
    pcm = pitch.heatmap(arg_hist, cmap='coolwarm', edgecolor='white', ax=ax['pitch'], norm=divnorm)
    plt.title("Zone de Contrôle",fontsize = 30, fontweight = "bold", color = "black", x=0.5, y=24)
    # Legend for our plot
    ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
    cbar = plt.colorbar(pcm, cax=ax_cbar)
    fig_text(0.07, 0.04, ">55% SFC (rouge) - 45% à 55% (blanc) - <45% SFC (bleu) ", color="Black", fontweight="bold", fontsize=12, backgroundcolor='0.85')
    fig.suptitle

plot_possession_and_danger(focus_df, focus_team, opposition, focus_color, oppo_color)


##########################################################################################################################################################################################
# Last third

def extract_location_x(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[0]
    return np.nan  # Return NaN for invalid or missing data

def extract_location_y(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[1]
    return np.nan  # Return NaN for invalid or missing data

def extract_end_location_pass_x(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[0]
    return np.nan  # Return NaN for invalid or missing data

def extract_end_location_pass_y(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[1]
    return np.nan  # Return NaN for invalid or missing data

def extract_end_location_carry_x(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[0]
    return np.nan  # Return NaN for invalid or missing data

def extract_end_location_carry_y(loc):
    if isinstance(loc, (list, tuple)) and len(loc) > 1:
        return loc[1]
    return np.nan  # Return NaN for invalid or missing data

# Extract x and y coordinates from the 'location' column
focus_df['location_x'] = focus_df['location'].apply(extract_location_x)
focus_df['location_y'] = focus_df['location'].apply(extract_location_y)
focus_df['end_location_x'] = focus_df['carry_end_location'].apply(extract_end_location_carry_x)
focus_df['end_location_y'] = focus_df['carry_end_location'].apply(extract_end_location_carry_y)
focus_df['end_location_x'] = focus_df['pass_end_location'].apply(extract_end_location_pass_x)
focus_df['end_location_y'] = focus_df['pass_end_location'].apply(extract_end_location_pass_y)

def passes_in_the_last_third(focus_df, home_team, away_team, team1_id, team2_id):
    
    # Assuming you've extracted the x and y location from the location column
    focus_df['x'] = focus_df['location'].apply(extract_location_x)
    
    df_passes = focus_df[(focus_df.type == "Pass")]
    df_good_passes = df_passes[(df_passes.pass_outcome != "Incomplete") & 
                               #(df_passes.outcome != "Injury Clearance") & 
                               (df_passes.pass_outcome != "Out") & 
                               (df_passes.pass_outcome != "Pass Offside") & 
                               (df_passes.pass_outcome != "Unknown")]
    df_carry = focus_df[(focus_df.type == "Carry")]
    
    minutes = ["5","10","15","20","25","30","35","40","45","50","55",
               "60","65","70","75","80","85","90",">90"]

    n = len(minutes)
    
    entrées_1 = np.zeros(n)
    passes_1 = np.zeros(n)
    entrées_2 = np.zeros(n)
    passes_2 = np.zeros(n)
    
    for i in df_good_passes.index :
        m = df_good_passes.at[i, "minute"] // 5
        m = min(18,m)
        if df_good_passes.at[i, "x"] <= 80:
            if df_good_passes.at[i, "team"] == home_team :
                entrées_1[m] += 1
            else :
                entrées_2[m] -= 1
        if df_good_passes.at[i, "x"] >= 80:
            if df_good_passes.at[i, "team"] == home_team:
                passes_1[m] += 1
            else:
                passes_2[m] -= 1

    for i in df_carry.index :
        m = df_carry.at[i, "minute"] // 5
        m = min(18,m)
        if df_carry.at[i, "x"] <= 80:
            if df_carry.at[i, "team"] == home_team :
                entrées_1[m] += 1
            else :
                entrées_2[m] -= 1

    
    # for i in df_good_passes.index :
    #     m = df_good_passes.at[i,"minute"] // 5
    #     m = min(18,m)
    #     if df_good_passes.at[i,"location_x"] <= 80 and df_good_passes.at[i,"end_location_x"] >= 80 :
    #         if df_good_passes.at[i, "team"] == home_team :
    #             entrées_1[m] += 1
    #         else :
    #             entrées_2[m] -= 1
    #     if df_good_passes["location_x"][i] >= 80 and df_good_passes["x_location"][i] >= 80:
    #         if df_good_passes["team_id"][i] == team1_id:
    #             passes_1[m] += 1
    #         else:
    #             passes_2[m] -= 1

    # for i in df_carry.index :
    #     m = df_carry.at[i,"minute"] // 5
    #     if df_carry.at[i,"x"] <= 80 and df_carry.at[i,"x"] >= 80 :
    #         if df_carry.at[i, "team"] == home_team :
    #             entrées_1[m] += 1
    #         else :
    #             entrées_2[m] -= 1
                
    diff_entrées = entrées_1 + entrées_2
    diff_passes = passes_1 + passes_2
    total_entrees_servette = np.sum(passes_1)/1.7
    
    with plt.ioff():
        fig, ax = plt.subplots(figsize=(16, 9))
        #plt.style.use('fivethirtyeight')
        plt.rcParams['axes.facecolor'] = "white"
        bs = ax.bar(range(n), passes_1, width=0.6, color=focus_color, alpha=0.8)
        bo = ax.bar(range(n), passes_2, width=0.6, color=oppo_color, alpha=0.8)
        bd = ax.bar(range(n), diff_passes, width=0.1, color=bgcolor, alpha=0.8)
        ax.set_xticks(range(n))
        ax.set_xticklabels(minutes)
        ax.set_xlabel("Temps du match", fontsize=20, fontweight="bold", labelpad=15)
        ax.set_ylabel("Nombre d'entrée", fontsize=20, fontweight="bold", labelpad=15)
        fig.text(0.38, 0.92, "Entrée Dernier Tier", fontsize=30, fontweight="bold")
        fig.text(0.5, 0.87, f'Deep progression SFC: {total_entrees_servette:.0f} | KPI: 53', ha='center', fontsize=20, backgroundcolor='0.85')
        ax.legend([bs, bo], [home_team, away_team])
        plt.show()

if home_team == focus_team:
    passes_in_the_last_third(focus_df, home_team, away_team, home_team, away_team)
else:
    passes_in_the_last_third(focus_df, away_team, home_team, away_team, home_team)

##########################################################################################################################################################################################
#Last third 
